#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from resource_stacks.custom_vpc import CustomVpcStack
from resource_stacks.custom_ec2 import CustomEc2Stack
from resource_stacks.sns import SnsTemplateStack
from resource_stacks.custom_lambda import CustomLambdaStack
from resource_stacks.dynamodb import DynamoDBStack

app = cdk.App()
vpc_stack = CustomVpcStack(app, "CustomVpcStack")
CustomEc2Stack(app, "CustomEc2Stack", vpc=vpc_stack.vpc)
snsTemplateStack = SnsTemplateStack(app, "SnsTemplateStack")
dynamoDBStack = DynamoDBStack(app, "DynamoDBStackapp")
CustomLambdaStack(app, "CustomLambdaStack", snsTemplateStack.custom_topic, dynamoDBStack.table)
app.synth()
