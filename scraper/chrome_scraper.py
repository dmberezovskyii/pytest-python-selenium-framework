from typing import List, Dict

import requests
from bs4 import BeautifulSoup


class ChromePageScraper:
    def __init__(self, url: str):
        self.URL = url

    def fetch(self) -> requests.Response:
        response = requests.get(self.URL)
        response.raise_for_status()  # Raises an exception if status code is not 200
        return response

    def parse(self) -> Dict[str, str]:
        elements_list = []
        drivers = {}
        page = self.fetch()

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


if __name__ == '__main__':
    scraper = ChromePageScraper('https://googlechromelabs.github.io/chrome-for-testing/#stable')
    elements = scraper.parse()
    print(elements)
