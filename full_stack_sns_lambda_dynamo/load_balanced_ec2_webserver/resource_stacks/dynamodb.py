from aws_cdk import core
from aws_cdk import aws_dynamodb as _dynomodb

class DynamoDBStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table = _dynomodb.Table(
            self,
            "tableId",
            table_name="ordersTable",
            partition_key=_dynomodb.Attribute(
                name="order_id",
                type=_dynomodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )
