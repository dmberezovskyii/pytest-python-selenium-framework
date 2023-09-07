import json
from typing import Dict

import requests
from bs4 import BeautifulSoup

from scraper.os_checker import OSChecker


class ChromePageScraper:
    URL_LATEST = 'https://googlechromelabs.github.io/chrome-for-testing/#stable'
    URL_ALL = "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"

    @staticmethod
    def __fetch(url: str) -> requests.Response:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception if status code is not 200
        return response

    @staticmethod
    def parse_latest() -> Dict[str, str]:
        # returns a latest stable chrome driver
        elements_list = []
        drivers = {}
        page = ChromePageScraper.__fetch(ChromePageScraper.URL_LATEST)

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

    @staticmethod
    def get_chromedriver(platform=None, version=None, milestone=None):
        """

        :param platform: os_name and architecture
        :param version: your chrome browser version
        :param milestone: first 3 digit of browser version: 116 or 115
        :return:
        """
        if version is None and milestone is None:
            raise ValueError(f"You must specify version or milestone: version {version}, milestone {milestone}")
        if platform is None:
            platform = OSChecker.check_os()

        # Parse the JSON data
        parsed_data = json.loads(ChromePageScraper.__fetch(ChromePageScraper.URL_ALL).text)
        milestones_data = parsed_data["milestones"]

        for milestone_key, milestone_data in milestones_data.items():
            if (
                    (milestone is None or milestone_key == milestone)
                    and (version is None or milestone_data["version"] == version)
            ):
                if "chromedriver" in milestone_data["downloads"]:
                    for chromedriver_info in milestone_data["downloads"]["chromedriver"]:
                        if platform is None or chromedriver_info["platform"] == platform:
                            return chromedriver_info


if __name__ == '__main__':
    print(ChromePageScraper.get_chromedriver(milestone='116'))