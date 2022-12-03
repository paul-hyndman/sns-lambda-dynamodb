#!/bin/bash

# Prep volume for JDK copy
sudo mkfs -t xfs /dev/sdb
sudo mkdir /java
sudo mount /dev/sdb /java

# Copy java jdk
sudo aws s3 cp s3://my-s3buckets-got-a-hole-in-it/jdk-19_linux-x64_bin.tar.gz /java/.
cd /java
sudo tar xvf /java/jdk-19_linux-x64_bin.tar.gz
export JAVA_HOME="/java/jdk-19.0.1"
export PATH="/java/jdk-19.0.1/bin:"$PATH

# Copy rest api
sudo aws s3 cp s3://my-s3buckets-got-a-hole-in-it/rest-api-fullstack-0.0.1-SNAPSHOT.jar /java/.
sudo chmod +x /java/rest-api-fullstack-0.0.1-SNAPSHOT.jar

# Launch app
java -jar /java/rest-api-fullstack-0.0.1-SNAPSHOT.jar org.example.restservice.RestServiceApplication
