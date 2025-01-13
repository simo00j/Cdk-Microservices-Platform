from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam


def setup_role(stack, project_name: str):
    project_name = project_name.lower().replace(' ', '-')
    role = iam.Role(
        stack, f"{project_name}-manager-role",
        assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryReadOnly")])
    return role


def setup_web_sg(stack, vpc):
    sg = ec2.SecurityGroup(stack, "WebSecurityGroup",
                            vpc=vpc,
                            description="Allow access on ports 443, 80, and 22",
                            allow_all_outbound=True  # Default is True, which allows all outbound traffic
                            )

    # Add ingress rules to the security group
    sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(443), description="Allow HTTPS")
    sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(80), description="Allow HTTP")
    sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(22), description="Allow SSH")
    return sg

def setup_db_sg(stack, vpc):
    rds_security_group = ec2.SecurityGroup(
        stack, "RDSSecurityGroup",
        vpc=vpc,
        description="Security group for RDS PostgreSQL instance"
    )
    
    # Allow inbound traffic on port 5432 for PostgreSQL
    rds_security_group.add_ingress_rule(
        ec2.Peer.any_ipv4(),
        ec2.Port.tcp(5432),
        "Allow PostgreSQL access"
    )
    return rds_security_group