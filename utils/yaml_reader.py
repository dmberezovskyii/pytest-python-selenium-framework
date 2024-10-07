import yaml
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Optional, Union, Dict


class YAMLReader:
    """
    Reads data from a YAML file and returns it in the specified format.

    :param filename (str): The name of the YAML file to read
    :param to_simple_namespace (bool): If True,
    converts the returned data to SimpleNamespace.
    :param is_secure (bool): If True,
    use safe loading of YAML and decrypts passwords.
    :param array_of_all_values (bool): If True,
     return all values in a flattened dictionary.
    :param separator (Optional[str]): String used to separate keys in the
    flattened dictionary.

    Returns:
        Union[SimpleNamespace, dict, list]: The parsed data from the YAML
        which can be a SimpleNamespace, dictionary, or list
    """

    @staticmethod
    def read(
        filename: str = "data.yaml",
        to_simple_namespace: bool = False,
        is_secure: bool = False,
        array_of_all_values: bool = False,
        separator: Optional[str] = None,
    ) -> Union[SimpleNamespace, dict, list]:
        resources_path = Path(__file__).resolve().parent.parent / "config"
        abs_path = resources_path / filename

        if not abs_path.exists():
            raise FileNotFoundError(f"The file {abs_path} does not exist.")

        try:
            with open(abs_path, "r", encoding="UTF-8") as stream:
                if is_secure:
                    data = yaml.safe_load(stream)
                    data = YAMLReader._decrypt_password(
                        data
                    )  # Decrypt passwords if necessary
                else:
                    data = yaml.load(stream, Loader=yaml.FullLoader)

        except yaml.YAMLError as e:
            raise ValueError(f"Error loading YAML file: {e}")

        # Convert to SimpleNamespace
        if to_simple_namespace:
            data = YAMLReader._convert_to_namespace(data)

        # If array_of_all_values is True, return all values in a dictionary
        if array_of_all_values:
            return YAMLReader._flatten_values(data, separator)

        return data

    @staticmethod
    def _decrypt_password(data: Any) -> Any:
        """
        Decrypts passwords in the data if they are encrypted.
        """
        pass
        for key, value in data.items():
            if key == "password":
                data[key] = YAMLReader._decrypt(value)
        #     else:
        #         data[key] = YAMLReader._decrypt_password(value)

    @staticmethod
    def _decrypt(encrypted_value: str) -> str:
        """
        Replace with your actual decryption logic.
        you could use a library like `cryptography` or `PyCryptodome`.
        """
        # Placeholder for decryption logic, modify as per your requirements
        return encrypted_value  # Replace with actual decrypted value

    @staticmethod
    def read_caps(
        browser: str = "chrome", filename: str = "data.yaml"
    ) -> Optional[Dict[str, Any]]:
        """Read browser capabilities from a YAML file."""
        try:
            resources_path = Path(__file__).resolve().parent.parent / "config"
            abs_path = resources_path / filename

            with open(abs_path, "r", encoding="UTF-8") as stream:
                data = yaml.safe_load(stream)
                return data.get(
                    browser
                )  # Return capabilities for the specified browser
        except (yaml.YAMLError, KeyError) as e:
            print(f"Error while reading '{filename}': {e}")
            return None

    @staticmethod
    def _convert_to_namespace(
        data: Any,
    ) -> Union[SimpleNamespace, list[SimpleNamespace], Any]:
        """Convert a dictionary to a SimpleNamespace."""
        if isinstance(data, dict):
            return SimpleNamespace(
                **{k: YAMLReader._convert_to_namespace(v) for k, v in data.items()}
            )
        elif isinstance(data, list):
            return [YAMLReader._convert_to_namespace(item) for item in data]
        return data

    @staticmethod
    def _flatten_values(
        data: Any, separator: Optional[str] = None, parent_key: str = ""
    ) -> Dict[str, Any]:
        """
        Flatten all values from a dictionary or list into a single dictionary
        """
        items = {}
        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{parent_key}{separator}{key}" if parent_key else key
                if isinstance(value, dict) or isinstance(value, list):
                    items.update(
                        YAMLReader._flatten_values(value, separator, new_key)
                    )
                else:
                    items[new_key] = value
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_key = (
                    f"{parent_key}{separator}{index}" if parent_key else str(index)
                )
                items.update(YAMLReader._flatten_values(item, separator, new_key))
        return items


# Example usage
# caps = YAMLReader.read_caps("chrome", "caps.yaml")
# Example usage simple namespace
# simple = YAMLReader.read("data.yaml", to_simple_namespace=True)
# print(simple.users.username1)
