import os
import random

import pulumi
import pulumi_aws

num_instances = 2

config = pulumi.Config()
aws_region = config.get("aws_region")
instance_type = config.get("instance-type")
key_pair_name = config.get("keyPairName")
default_user = config.get("default_user")
os_type = "ubuntu"

teacher_pbkey = config.get("teacher-pbkey")
my_pbkey = config.get("my-pbkey")

ami_mapping = {
    "amazon-linux-2": "ami-0c94855ba95c71c99",
    "ubuntu": "ami-0c8b488faf8febeaf",
}
ami_id = ami_mapping.get(os_type, ami_mapping["amazon-linux-2"])


user_data_file = "user-data.sh"
if os.path.exists(user_data_file):
    with open(user_data_file, "r") as f:
        user_data_raw = f.read()
    user_data = (
        user_data_raw.replace("${DEFAULT_USER}", default_user)
        .replace("${YOUR_PUBLIC_KEY}", teacher_pbkey)
        .replace("${MY_PUBLIC_KEY}", my_pbkey)
    )
else:
    user_data = ""

sg = pulumi_aws.ec2.SecurityGroup(
    "custom-sg",
    description="Security group with custom firewall rules",
    ingress=[
        pulumi_aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp", from_port=22, to_port=22, cidr_blocks=["0.0.0.0/0"]
        ),
        pulumi_aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp", from_port=5432, to_port=5435, self=True
        ),
    ],
    egress=[
        pulumi_aws.ec2.SecurityGroupEgressArgs(
            protocol="-1", from_port=0, to_port=0, cidr_blocks=["0.0.0.0/0"]
        )
    ],
)


def create_instance(name: str) -> pulumi_aws.ec2.Instance:
    instance = pulumi_aws.ec2.Instance(
        name,
        instance_type=instance_type,
        ami=ami_id,
        key_name=key_pair_name,
        vpc_security_group_ids=[sg.id],
        user_data=user_data,
        tags={"Name": name},
    )
    pulumi.export(f"{name}_id", instance.id)
    return instance


def main(num_instances):
    instances = []
    for i in range(1, num_instances + 1):
        ran_id = random.randint(0, 10000)
        instance_name = f"instance-{ran_id}-{i}"
        instances.append(create_instance(instance_name))


main(num_instances)
