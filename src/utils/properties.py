import os
from dotenv import load_dotenv


class EmptyURLError(Exception):
    def __init__(self, env_var):
        self.env_var = env_var
        super().__init__(f"Environment variable '{env_var}' is empty or not found.")


class Properties:
    _ENV_VARIABLES = {
        "dev": ("DEV_URL", ""),
        "stag": ("STAG_URL", ""),
        # Add more environments and their default URLs as needed
    }

    @classmethod
    def _get_base_url(cls, env_var, default_url=None):
        url = os.environ.get(env_var)
        if url is not None and url.strip():  # Check if URL is not empty or whitespace
            return url
        else:
            raise EmptyURLError(env_var)

    @classmethod
    def get_base_url(cls, environment):
        env_var, default_url = cls._ENV_VARIABLES.get(environment, (None, None))
        if env_var:
            return cls._get_base_url(env_var, default_url)
        else:
            raise ValueError(f"Unsupported environment: {environment}")


# Load environment variables from .env files
load_dotenv()
