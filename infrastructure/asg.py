from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_autoscaling as autoscaling

# Function to select instance type based on RAM and CPU requirements
def select_instance_type(ram: str, cpu: str) -> ec2.InstanceType:
    # Mapping of RAM and CPU to instance types
    instance_type_mapping = {
        "2GB_1": "t2.small",
        "4GB_2": "t2.medium",
        "8GB_2": "t2.large",
        }

    # Default instance type
    default_instance_type = "t2.medium"

    # Create the key for looking up in the mapping
    key = f"{ram}_{cpu}"

    # Return the instance type from the mapping or the default if not found
    return ec2.InstanceType(instance_type_mapping.get(key, default_instance_type))


def setup_asg(stack,deployment, vpc: ec2.Vpc,sg,role,project_name):
    # Create the Auto Scaling Group
    subnet_name = f"{project_name.lower().replace(' ', '-')}-subnet"
    asg = autoscaling.AutoScalingGroup(
        stack,
        f"{deployment['deployment_name']}-asg",
        vpc=vpc,
        instance_type=select_instance_type(deployment['ram'], deployment['cpu']),
        machine_image=ec2.AmazonLinuxImage(),
        min_capacity=0 if deployment['type'] == 'task' else 1,
        max_capacity=2,
        desired_capacity=1,
        role=role,
        security_group=sg,
        vpc_subnets=ec2.SubnetSelection(subnet_group_name=subnet_name),
        spot_price="0.04",
        block_devices=[autoscaling.BlockDevice(
                device_name="/dev/sdh",
                volume=autoscaling.BlockDeviceVolume.ebs(
                    volume_size=deployment['disk'],  # Set the disk size from deployment config
                    volume_type=autoscaling.EbsDeviceVolumeType.GP3    # Use GP3 for general-purpose SSD
                )
            )]
    )
    return asg