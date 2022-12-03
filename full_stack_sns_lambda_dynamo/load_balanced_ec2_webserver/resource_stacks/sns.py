import aws_cdk as cdk
from aws_cdk import aws_lambda as _lambda

from aws_cdk import (
    core,
    aws_sns as _sns,
    aws_sns_subscriptions as _subs
)

class SnsTemplateStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

            # Create topic
        self.custom_topic = _sns.Topic(
            self,
            "topcId",
            display_name="New Order Topic",
            topic_name="newOrderTopic"
        )
      
        # Add subscriptions
        self.custom_topic.add_subscription(
            _subs.EmailSubscription("paulhyndman@gmail.com")
        )

