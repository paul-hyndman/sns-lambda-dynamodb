from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_iam as _iam,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_autoscaling as _autoscaling
)


class CustomEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read bootstrap script to install Java and start app
        with open("user-data/install.sh", mode="r") as file:
            user_data = file.read()

        # Get latest ami
        amzn_linux_ami = _ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )

        # Create Load Balancer using VPC created earlier
        alb = _elbv2.ApplicationLoadBalancer(
            self,
            "albId",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="WebServerAlb"
        )

        # ALB allows internet traffic
        alb.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(1025),
            description="Allow internet access on ALB port 1025"
        )

        # Add ALB lister
        listener = alb.add_listener(
            id="listenerId",
            # Port 80 is blocked from VM by default; us non-standard port #
            port=1025,
            # protocol is required for non-standard port #
            protocol=_elbv2.ApplicationProtocol.HTTP,
            open=True)

        # Web Server IAM Role
        web_server_iam_role = _iam.Role(
            self,
            "webserverRoleId",
            assumed_by=_iam.ServicePrincipal(
                'ec2.amazonaws.com'),
            managed_policies=[
                # S3 access needed to copy .jar in user data, console access granted from SSMManaged policy
                _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ]
        )

        # Create Autoscaling Group with one EC2 instance
        web_server_asg = _autoscaling.AutoScalingGroup(
            self,
            "webServerAsgId",
            vpc=vpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PRIVATE
            ),
            instance_type=_ec2.InstanceType(
                instance_type_identifier="t2.micro"
            ),
            machine_image=amzn_linux_ami,
            role=web_server_iam_role,
            min_capacity=1,
            max_capacity=2,
            user_data=_ec2.UserData.custom(user_data),
            block_devices=[
                _autoscaling.BlockDevice(
                    device_name="/dev/sdb",
                    volume=_autoscaling.BlockDeviceVolume.ebs(
                        volume_size=50,
                        delete_on_termination=True,
                        encrypted=False,
                        volume_type=_autoscaling.EbsDeviceVolumeType.STANDARD)
                )
            ]
        )

        # Tell ASG security group to allow traffic from the ALB
        web_server_asg.connections.allow_from(
            alb,
            _ec2.Port.tcp(1025),
            description="ASG security group is allowed to receive traffic from ALB"
        )

        # Add AutoScaling Group Instances to ALB Target Group with health check URL
        listener.add_targets(
            "listenerId",
            port=1025,
            targets=[web_server_asg],
            # protocol is required for non-standard port #
            protocol=_elbv2.ApplicationProtocol.HTTP,
            health_check=_elbv2.HealthCheck(
                path="/actuator/health"
            )
        )

        # Echo Load Balancer URL in CloudFormation Output
        core.CfnOutput(
            self,
            "albDNS",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Web server ALB DNS-based URL"
        )
