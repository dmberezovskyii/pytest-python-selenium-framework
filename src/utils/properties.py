import os


class Environment:
    BASE_URL = 'env.dev'
    BASE_STAGE_URL = 'env.stag'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Properties:
    _BASE_DEV_URL = "https://softjourn.com"
    _BASE_STAGE_URL = "https://softjourn.com/stand-with-ukraine"

    @staticmethod
    def _get_base_dev_url():
        return os.environ.get('env.dev', Properties._BASE_DEV_URL)

    @staticmethod
    def _get_base_stage_url():
        return os.environ.get('env.stag', Properties._BASE_STAGE_URL)

    @staticmethod
    def get_base_url(environment):
        url_mapping = {
            "dev": Properties._get_base_dev_url(),
            "stag": Properties._get_base_stage_url(),
            # Add more environment mappings as needed
        }

        if environment in url_mapping:
            return url_mapping[environment]
        else:
            raise ValueError(f"Unsupported environment: {environment}")
