# Simple Python Selenium UI Automation Framework

This is a simple UI automation framework built with Python, pytest, and Selenium.
<br>
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/dmytro-berezovskyi/)



## Features

- Easy-to-use UI automation framework.
- Based on popular Python libraries: pytest and Selenium.
- Supports Chrome,Firefox and Remote browsers for UI testing.
- Provides utilities for setting up and managing WebDriver instances.

## Getting Started

### Prerequisites

- Python 3.8-3.11

### Usage locally

1. Clone this repository
2. Install required dependencies with
```pip install -r requirements.txt```
3. Create .env file and add 
```
DEV_URL = ""
STAG_URL = ""
```
### Latest chrome drivers
- #### [Drivers](https://googlechromelabs.github.io/chrome-for-testing/#stable)


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
 - Pay attention while running CI on your local git resources must contain proper chrome driver with x86_64 architecture
 - Go to repository settings -> secrets and variables -> actions -> variables and add DEV_URL, STAG_URL
 - Added CI configuration to run tests for ubuntu *run_test_ubuntu.yaml*
 