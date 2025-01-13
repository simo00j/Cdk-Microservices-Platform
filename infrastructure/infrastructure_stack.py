from aws_cdk import Stack
from constructs import Construct

from .vpc import setup_vpc
from .ecs import setup_ecs
from .ecr import setup_ecr
from .iam import setup_role, setup_web_sg, setup_db_sg
from .database import setup_database
from .s3 import setup_s3


VPC_CIDR = "172.31.100.0/16"
# Subnet size of the subnets in the Local Zone
SUBNET_SIZE = 24


class InfrastructureStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, projects, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        vpc = setup_vpc(self, construct_id, projects)
        web_sg = setup_web_sg(self, vpc)
        db_sg = setup_db_sg(self, vpc)

        for project in projects:
            setup_database(self, vpc, project, db_sg)
            role = setup_role(self, project['name'])
            setup_ecr(self, project['name'])
            setup_ecs(self, vpc, project, web_sg, role)
            setup_s3(self, project, role)
