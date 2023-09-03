# Simple Python Selenium UI Automation Framework

This is a simple UI automation framework built with:
- Python: 3.10, pytest 7.2.0, Selenium: 4.11.2 and GitHub Actions CI
<br>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/dmytro-berezovskyi/)



## Features

- Easy-to-use UI automation framework.
- Based on popular Python libraries: pytest and Selenium.
- Supports Chrome,Firefox and Remote browsers for UI testing.
- Provides utilities for setting up and managing WebDriver instances.
- Supports GitHub Actions CI workflow for Darwin(Mac) and Linux
- Supports different environments: dev, stage
- Supports pytest reports and custom logs

## Getting Started

### Prerequisites

- Python 3.8-3.11
- Note, if you are not using MacOS with arm64 architecture or Selenium version below 4.11.0, 
*upload the appropriate driver corresponding to your OS to the resources directory*

### Usage locally

1. Clone this repository
2. Install required dependencies with
```pip install -r requirements.txt```
3. Create .env file and add 
```
DEV_URL = "your-dev-project-url"
STAG_URL = "your-staging-project-url"
```
4. If you don't want to use environment variables, add your references to the properties file
```
class Properties:
     _ENV_VARIABLES = {
        "dev": ("DEV_URL", ""),
        "stag": ("STAG_URL", ""),
        # Add more environments and their default URLs as needed
    }
```

### Latest drivers
- #### [Chrome Drivers](https://googlechromelabs.github.io/chrome-for-testing/#stable)
- #### [Firefox Drivers](https://github.com/mozilla/geckodriver)
- It is possible to download the latest version of the driver for MacOS arch64 using chromedriver.sh located in the resources folder


### TODO

| Item                                                 | Status                                                   |
|------------------------------------------------------|----------------------------------------------------------|
| 1. drivers factory: local, remote, [chrome, firefox] | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 2. pytest.ini config: addopts, errors, markers       | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 3. environments: dev, stag, prod                     | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 4. secrets                                           | ![Status](https://img.shields.io/badge/TODO-yellow)      |
| 5. utilities: yaml_reader, logger                    | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 6. BasePage: wait strategy, base actions             | ![Status](https://img.shields.io/badge/DONE-brightgreen) |
| 7. Properties: make properties helper                | ![Status](https://img.shields.io/badge/DONE-brightgreen) |
| 8. CI: GitHub Actions: runs tests, publish reports   | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |

### CI: GitHub Actions
#### *Pay attention*
 - While running CI on your local, git resources must contain proper chrome driver with x86_64 architecture 
   - (unless you are using selenium version 4.11.0 and higher)
 - Go to repository settings -> secrets and variables -> actions -> variables and add DEV_URL, STAG_URL
 - Added CI configuration to run tests for ubuntu *run_test_ubuntu.yaml*
 