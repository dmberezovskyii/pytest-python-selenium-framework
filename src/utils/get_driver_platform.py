import platform


def _get_driver_type(dr_type=None):
    os_arch_mapping = {
        "arm64": "chrome_arm64",
        "x86_64": "chrome_x86_64",
        "ubuntu": "ubuntu",  # Add additional mappings as needed
    }

    default_driver_type = dr_type
    os_arch = platform.machine()
    os_name = platform.system().lower()

    driver_type = os_arch_mapping.get(os_arch, default_driver_type)
    if os_name in os_arch_mapping:
        driver_type = os_arch_mapping[os_name]

    return driver_type
