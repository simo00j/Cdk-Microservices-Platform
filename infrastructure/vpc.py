from typing import Dict, List
from aws_cdk import aws_ec2 as ec2


VPC_CIDR = "172.31.100.0/16"
# Subnet size of the subnets in the Local Zone
SUBNET_SIZE = 24
        


def setup_vpc(stack,construct_id: str, projects: List[Dict[str, str]]):
    """
    Setup VPC
    :param construct_id: Construct ID
    :param projects: List of projects
    :return: None
    """
    subnet_configuration = [ ec2.SubnetConfiguration(
        name= f"{project['name'].lower().replace(' ', '-')}-subnet",
        subnet_type=ec2.SubnetType.PUBLIC,
        cidr_mask=SUBNET_SIZE
    ) for project in projects]

    vpc = ec2.Vpc(stack, construct_id,
                        max_azs=2,  # Specify the maximum number of Availability Zones
                        ip_addresses = ec2.IpAddresses.cidr(VPC_CIDR),
                        subnet_configuration=subnet_configuration
                        )
    return vpc