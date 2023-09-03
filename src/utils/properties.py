import os

from dotenv import load_dotenv


class EmptyURLError(Exception):
    def __init__(self, env_var):
        self.env_var = env_var
        super().__init__(f"Environment variable '{env_var}' is empty or not found.")


class Properties:
    _BASE_DEV_URL = ""  # set dev url if you don't want to use .env file
    _BASE_STAGE_URL = ""  # set staging url if you don't want to use .env file

    @classmethod
    def _get_base_url(cls, env_var, default_url=None):
        url = os.environ.get(env_var)
        if url is not None and url.strip():  # Check if URL is not empty or whitespace
            return url
        else:
            raise EmptyURLError(env_var)

    @classmethod
    def get_base_dev_url(cls):
        return cls._get_base_url('DEV_URL', Properties._BASE_DEV_URL)

    @classmethod
    def get_base_stage_url(cls):
        return cls._get_base_url('STAG_URL', Properties._BASE_STAGE_URL)

    @classmethod
    def get_base_url(cls, environment):
        url_mapping = {
            "dev": cls.get_base_dev_url(),
            "stag": cls.get_base_stage_url(),
            # Add more environment mappings as needed
        }

        if environment in url_mapping:
            return url_mapping[environment]
        else:
            raise ValueError(f"Unsupported environment: {environment}")


# Load environment variables from .env files
load_dotenv()
