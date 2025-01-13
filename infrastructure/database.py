from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds



def setup_database(stack, vpc,project,rds_sg):
    # Define the RDS instance
    subnet_name = f"{project['name'].lower().replace(' ', '-')}-subnet"
    database = project.get('database',{})
    
    if database : 
        db_name = database.get('name',f"{project['name']}").lower().replace(' ', '')
        db_size = database.get('storage',50)
        rds_instance = rds.DatabaseInstance(
            stack, 
            f"{db_name}Rds",
            instance_identifier=db_name,
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_13  
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM  # Choose the instance size
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_group_name=subnet_name  # Use the specified subnet group name
            ),
            security_groups=[rds_sg],
            multi_az=False,  # Set to True if you want a Multi-AZ deployment
            allocated_storage=db_size,  # Specify the allocated storage size in GB
            max_allocated_storage=db_size*2,  # Set the maximum storage size for autoscaling in GB
            database_name=db_name,
            credentials=rds.Credentials.from_generated_secret("sense4data"),  # Auto-generate a master username and password
            deletion_protection=True,
            port=5432,
            cloudwatch_logs_exports=["postgresql", "upgrade"],
            publicly_accessible=True
        )

        return rds_instance
    return None