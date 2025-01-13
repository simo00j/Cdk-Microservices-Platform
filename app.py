#!/usr/bin/env python3
import aws_cdk as cdk

from infrastructure.infrastructure_stack import InfrastructureStack
from configs import load_config
from settings import Settings


def main():

    app = cdk.App()
    projects = load_config()
    settings = Settings()

    InfrastructureStack(app,settings.Namespace,projects,env=cdk.Environment(account=settings.CDK_DEFAULT_ACCOUNT, region=settings.region))
    app.synth()


if __name__ == "__main__":
    main()
