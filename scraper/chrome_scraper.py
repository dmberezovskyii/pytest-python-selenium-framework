import json
from typing import Dict

import requests
from bs4 import BeautifulSoup


class ChromePageScraper:
    URL_LATEST = 'https://googlechromelabs.github.io/chrome-for-testing/#stable'
    URL_ALL = "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"

    def __init__(self, url: str):
        self.URL = url

    def fetch(self, url: str) -> requests.Response:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception if status code is not 200
        return response

    def parse_latest(self) -> Dict[str, str]:
        elements_list = []
        drivers = {}
        page = self.fetch(self.URL)

        soup = BeautifulSoup(page.text, 'html.parser')
        element = soup.select_one('section#stable.status-not-ok div.table-wrapper table tbody tr.status-ok')

        if not element:
            raise Exception("Element not found in the HTML.")

        code_elements = element.find_all('code')

        for el in code_elements:
            text = el.text.strip()

            if text not in ['200', 'chrome', 'chromedriver']:
                elements_list.append(text)

        for i in range(0, len(elements_list), 2):
            os = elements_list[i]
            link = elements_list[i + 1]
            drivers[os] = link

        return drivers

    def get_latest_driver(self, os_name: str):
        drivers = self.parse_latest()
        if os_name in drivers:
            print(drivers[os_name])

    def get_chromedriver(self, milestone, platform, version=None):

        # Parse the JSON data
        parsed_data = json.loads(self.fetch(self.URL).text)
        milestones_data = parsed_data["milestones"]

        if milestone in milestones_data:
            milestone_data = milestones_data[milestone]
            if "chromedriver" in milestone_data["downloads"]:
                for chromedriver_info in milestone_data["downloads"]["chromedriver"]:
                    if (
                            chromedriver_info["platform"] == platform
                            and (version is None or milestone_data["version"] == version)
                    ):
                        return chromedriver_info


if __name__ == '__main__':
    scraper = ChromePageScraper(ChromePageScraper.URL_ALL)
    elements = scraper.get_chromedriver("116", "mac-arm64")
    print(elements)
