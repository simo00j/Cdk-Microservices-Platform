from aws_cdk import (
    aws_ecs as ecs,
    aws_secretsmanager as secretsmanager
)

from .asg import setup_asg

def fill_defaults(deployment):
    # Define default values for missing keys
    default_values = {
        "ram": "2GB",
        "cpu": "1",
        "disk": "20GB",
        "type": "task"
    }

    # Fill in missing keys with default values
    for key, value in default_values.items():
        deployment.setdefault(key, value)

    return deployment
def setup_ecs(stack, vpc, project, sg, role):
    #

    cluster = ecs.Cluster(
        stack, f"{project['name']}-cluster",
        vpc=vpc
    )
    deployments = project.get('deployments', [])
    for deployment in deployments:
        deployment = fill_defaults(deployment)
        if deployment['type'] == 'task':
            if deployment.get('image', None):
                fargate_task_definition = ecs.FargateTaskDefinition(
                    stack,
                    f"{deployment['deployment_name']}-FargateTaskDef",
                    cpu= deployment['cpu'] * 1024,
                    memory_limit_mib=deployment['ram'] * 1024
                )
                container = fargate_task_definition.add_container(
                    f"{deployment['deployment_name']}-container",
                    image=ecs.ContainerImage.from_registry(deployment['image'])
                )
                for key, value in deployment.get('env_vars', {}).items():
                    container.add_environment(key, value)

                for key, secret_name in deployment.get('secrets', {}).items():
                    secret = secretsmanager.Secret.from_secret_name_v2(
                        scope=stack,
                        id="MySecret",
                        secret_name=secret_name)
                    container.add_secret(key, ecs.Secret.from_secrets_manager(secret, field=secret_name))


        elif deployment['type'] == 'service':
            asg = setup_asg(stack, deployment, vpc, sg, role, project['name'])
            cp_name = f"{deployment['deployment_name']}-CapacityProvider"
            capacity_provider = ecs.AsgCapacityProvider(stack, cp_name,
                                                        auto_scaling_group=asg,
                                                        enable_managed_scaling=True,
                                                        enable_managed_termination_protection=False,
                                                        )
            cluster.add_asg_capacity_provider(capacity_provider)
            ecs_task_definition = ecs.TaskDefinition(stack, deployment['deployment_name'],
                                                     compatibility=ecs.Compatibility.EC2,
                                                     cpu=str(deployment['cpu'] * 1024),  # Adjust as needed
                                                     memory_mib=str(deployment['cpu'] * 1024),
                                                     )
            ecs_task_definition.add_container(f"{deployment['deployment_name']}-container",
                                                          image=ecs.ContainerImage.from_registry(deployment['image'])
                                                      )
            ecs.Ec2Service(stack, "MyEcsService",
                           cluster=cluster,
                           task_definition=ecs_task_definition,
                           capacity_provider_strategies=[ecs.CapacityProviderStrategy(
                               capacity_provider=cp_name,
                               weight=1,
                           )]
                           )
