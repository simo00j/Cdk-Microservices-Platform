from typing import Literal
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Configuration regarding behavior of strategy runner
    logging_level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    region: str = "us-west-1"
    CDK_DEFAULT_ACCOUNT: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    Namespace: str
    
    class Settings:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Allow variables to be defined in lower case inside the ode and
        # upper case on environment variables
        case_sensitive = False

