# Project highlights how, using CDK, the following:
#   - Create AWS infrastructure using Python and CDK
#   - Expose an EC2-based public REST API via a non-standard HTTP port
#   - Load custom code via a user-data script
#   - From REST API, publish message to a topic
#   - Subscribed Python Lambda function puts message to a Dynamo Database

# Project creates AWS artifacts:
#  - VPC
#  - EC2
#  - SNS Topic
#  - Python Lambda function
#  - A sample Java-based REST API

# When deployed, issue a POST to URL:
#    http://<<Your public ALB DNS created in EC2 stack>>:1025/order

Requirements:
 - A command shell such as Git Bash
 - Python
 - CDK
 - Node JS/NPM for miscellaneous package installs
 - A linux JDK

Modify cdk.json with your account in the "envs" configuration

This is a modification of an earlier project which deployed a REST API 
See https://github.com/paul-hyndman/cdk-full-stack-ec2-rest-api for more info