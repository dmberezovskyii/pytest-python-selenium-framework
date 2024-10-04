import os
from dotenv import load_dotenv

from utils.error_handler import ErrorHandler, ErrorType


class Properties:
    _ENV_VARIABLES = {
        "dev": ("DEV_URL", "your_dev_url"),
        "stag": ("STAG_URL", "your_stag_url"),
        # Add more environments and their default URLs as needed
    }

    @classmethod
    def _get_base_url(cls, env_var, default_url=None):
        url = os.environ.get(env_var)
        if (
            url is not None and url.strip()
        ):  # Check if URL is not empty or whitespace
            return url
        else:
            raise ErrorHandler.raise_error(
                ErrorType.EMPTY_URL_ERROR, env_var
            )

    @classmethod
    def get_base_url(cls, environment):
        env_var, default_url = cls._ENV_VARIABLES.get(
            environment, (None, None)
        )
        if env_var:
            return cls._get_base_url(env_var, default_url)
        else:
            raise ErrorHandler.raise_error(ErrorType.ENV_ERROR, environment)


# Load environment variables from .env files
load_dotenv()
