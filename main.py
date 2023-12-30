from funcs.replit_scrapper import ReplitScrapper
from funcs.github_archiver import GithubArchiver
import os
import zipfile
from dotenv import load_dotenv
load_dotenv()

WDIR = os.path.abspath(os.path.dirname(__name__))

if __name__ == "__main__":
    test_url = "https://replit.com/@pythondojoarchi/SlipperyGargantuanDebuggers"
    project_name = "SlipperyGargantuanDebuggers"

    # Download repo files as zip
    scrapper = ReplitScrapper(login_name=os.environ['EMAIL'], login_password=os.environ['PASSWORD'])
    scrapper.set_replit_url(test_url)
    scrapper.run()

    # Unzip downloaded zip file
    download_folder_path = os.path.join(WDIR, "screen-shots")
    full_file_path = os.path.join(download_folder_path, project_name+".zip")
    extracted_folder_path = os.path.join(download_folder_path, project_name)
    zipfile.ZipFile(full_file_path).extractall(extracted_folder_path)

    # Commit target files to Github
    archiver = GithubArchiver(
        project_name=project_name,
        github_access_token=os.environ['GITHUB_ACCESS_TOKEN']
    )
    archiver.identify_target_files()
    archiver.commit_to_github()
