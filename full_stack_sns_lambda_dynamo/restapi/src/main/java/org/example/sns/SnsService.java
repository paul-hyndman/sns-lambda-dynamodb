package org.example.sns;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.services.sns.AmazonSNS;
import com.amazonaws.services.sns.AmazonSNSClientBuilder;
import com.amazonaws.services.sns.model.PublishResult;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;

@Component
public class SnsService {
    @Value("${topic_arn}")
    private String snsTopicARN;

    @Value("${access_key}")
    private String awsAccessKey;

    @Value("${secret_access_key}")
    private String awsSecretKey;

    @Value("${aws_region}")
    private String awsRegion;

    private AmazonSNS amazonSNS;

    @PostConstruct
    private void postConstructor() {
        AWSCredentialsProvider awsCredentialsProvider = new AWSStaticCredentialsProvider(
                new BasicAWSCredentials(awsAccessKey, awsSecretKey)
        );

        this.amazonSNS = AmazonSNSClientBuilder.standard()
                .withCredentials(awsCredentialsProvider)
                .withRegion(awsRegion)
                .build();
    }

    public String publishMessage(String message) {
        PublishResult result = this.amazonSNS.publish(this.snsTopicARN, message);
        // A simple example of returning a conf #.  In production this could be
        // a persisted, unique tracking #
        return result.getMessageId();
    }
}
