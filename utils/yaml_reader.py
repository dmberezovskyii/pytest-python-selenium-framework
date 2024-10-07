import yaml
from pathlib import Path


class YamlReader:
    @staticmethod
    def read_caps(browser="chrome", filename="caps.yaml"):
        try:
            # Get the path to the resources folder from the script's directory
            resources_path = (
                Path(__file__).resolve().parent.parent.parent / "config"
            )
            abs_path = resources_path / filename

            with open(abs_path, "r", encoding="UTF-8") as stream:
                data = yaml.safe_load(stream)
                return data.get(browser)
        except (yaml.YAMLError, KeyError) as e:
            print(f"Error while reading '{filename}': {e}")
            return None
