import os
import shutil
import zipfile

import requests


class FileDownloader:
    def __init__(self, destination_folder='resources'):
        self.destination_folder = destination_folder

    def destination(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '../src', '..', self.destination_folder))

    def create_destination_folder(self):
        path_to_file = self.destination()
        if not os.path.exists(path_to_file):
            try:
                os.makedirs(self.destination_folder)
            except OSError:
                raise Exception(f"Failed to create destination folder: {self.destination_folder}")

    def download_file(self, download_url, destination_file):
        try:
            response = requests.get(download_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to download file from {download_url}: {e}")

        with open(destination_file, "wb") as f:
            f.write(response.content)


class DriverManager:
    def __init__(self, destination_folder='resources'):
        self.destination_folder = destination_folder
        self.downloader = FileDownloader(self.destination_folder)
        self.os_checker = OSChecker()

    def extract_zip(self, zip_file, destination_folder):
        try:
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(destination_folder)
        except zipfile.BadZipFile:
            raise Exception("Failed to unzip chromedriver")

    def rename_chromedriver(self, chromedriver_path):
        source_path = os.path.join(self.destination_folder, "chromedriver-mac-arm64", "chromedriver")
        try:
            os.rename(source_path, chromedriver_path)
        except (OSError, FileNotFoundError):
            raise Exception("Failed to move chromedriver")

    def download_and_extract_chromedriver(self, download_url):
        self.downloader.create_destination_folder()

        zip_file = os.path.join(self.destination_folder, "chromedriver.zip")
        chromedriver_path = os.path.join(self.destination_folder, "chromedriver")
        self.downloader.download_file(download_url, zip_file)
        self.extract_zip(zip_file, self.downloader.destination())
        self.rename_chromedriver(chromedriver_path)

        try:
            shutil.rmtree(os.path.join(self.destination_folder, "chromedriver-mac-arm64"))
        except OSError:
            raise Exception("Failed to delete chromedriver-mac-arm64 folder")

        try:
            os.remove(zip_file)
        except OSError:
            raise Exception("Failed to delete ZIP file")

        self.os_checker.print_os_info()


class OSChecker:
    @staticmethod
    def check_os():
        os_name = os.uname().sysname
        arch = os.uname().machine
        return os_name, arch

    def print_os_info(self):
        os_name, arch = self.check_os()
        print(f"Operating System: {os_name}, arch={arch}")


if __name__ == "__main__":

    download_url = ""
    # Define the destination folder for the downloaded file
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    driver_path = os.path.join(project_dir, "resources")

    driver_manager = DriverManager(driver_path)

    if driver_manager.os_checker.check_os() == ("Darwin", "arm64"):
        print("Building for Apple M1")
        download_url = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/mac-arm64/chromedriver-mac-arm64.zip"
    else:
        print("Building for x86_64")
        download_url = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/mac-x64/chromedriver-mac-x64.zip"

    driver_manager.download_and_extract_chromedriver(download_url)
