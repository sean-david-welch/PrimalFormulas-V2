import json
import pulumi_aws as aws

instance_profile_role = aws.iam.Role(
    "eb-ec2-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Sid": "",
                    "Principal": {
                        "Service": "ec2.amazonaws.com",
                    },
                }
            ],
        }
    ),
)

eb_policy_attatch = aws.iam.RolePolicyAttachment(
    "eb-policy-attach",
    role=instance_profile_role.name,
    policy_arn="arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier",
)


instance_profile = aws.iam.InstanceProfile(
    "eb-ec2-instance-profile", role=instance_profile_role.name
)


eb_app = aws.elasticbeanstalk.Application(
    "primal-formulas", description="Fast API server running on uvicorn"
)

eb_env = aws.elasticbeanstalk.Environment(
    "primalformulas-env",
    application=eb_app.name,
    solution_stack_name="64bit Amazon Linux 2023 v4.0.1 running Docker",
    settings=[
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:elasticbeanstalk:environment:proxy",
            name="ProxyServer",
            value="nginx",
        ),
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:autoscaling:launchconfiguration",
            name="IamInstanceProfile",
            value=instance_profile.name,
        ),
    ],
)
