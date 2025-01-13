from aws_cdk import aws_ecr as ecr


def setup_ecr(stack, project_name: str) :
    normalized_project_name = project_name.lower().replace(' ', '-')
    repository = ecr.Repository(
            stack,
            f"{normalized_project_name}-repository",
            repository_name=f"{normalized_project_name}-repository" 
        )
    return repository