import os

from dotenv import load_dotenv


class Properties:
    _BASE_DEV_URL = "https://softjourn.com"
    _BASE_STAGE_URL = "https://softjourn.com/stand-with-ukraine"

    @classmethod
    def _get_base_url(cls, env_var, default_url=None):
        return os.environ.get(env_var, default_url)

    @classmethod
    def get_base_dev_url(cls):
        return cls._get_base_url('DEV_URL')

    @classmethod
    def get_base_stage_url(cls):
        return cls._get_base_url('STAG_URL')

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

if __name__ == '__main__':
    print(Properties.get_base_url("dev"))
