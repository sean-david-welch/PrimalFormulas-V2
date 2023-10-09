import json
import pulumi
import pulumi_aws as aws

default_vpc = aws.ec2.DefaultVpc("default-vpc", tags={"Name": "Default VPC"})

default_az1 = aws.ec2.DefaultSubnet(
    "default-az-1",
    availability_zone="eu-west-1a",
    tags={
        "Name": "Default subnet for eu-west-1a",
    },
)

default_az2 = aws.ec2.DefaultSubnet(
    "default-az-2",
    availability_zone="eu-west-1b",
    tags={
        "Name": "Default subnet for eu-west-1b",
    },
)

default_az3 = aws.ec2.DefaultSubnet(
    "default-az-3",
    availability_zone="eu-west-1c",
    tags={
        "Name": "Default subnet for eu-west-1c",
    },
)

subnet_ids = pulumi.Output.all(default_az1.id, default_az2.id, default_az3.id).apply(
    lambda az: f"{az[0]},{az[1]},{az[2]}"
)

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
    solution_stack_name="64bit Amazon Linux 2023 v4.0.4 running Python 3.11",
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
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:ec2:vpc",
            name="VPCId",
            value=default_vpc.id,
        ),
        aws.elasticbeanstalk.EnvironmentSettingArgs(
            namespace="aws:ec2:vpc", name="Subnets", value=subnet_ids
        ),
    ],
)
