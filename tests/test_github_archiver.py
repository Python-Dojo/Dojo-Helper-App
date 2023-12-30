# from github import Github, Auth
import unittest
from funcs.github_archiver import GithubArchiver
import os
from dotenv import load_dotenv
load_dotenv()


class Test(unittest.TestCase):

    def test_archiver_raise_error_if_target_folder_does_not_exist(self):
        archiver = GithubArchiver(
            project_name="directory_not_exist",
            github_access_token=os.environ['GITHUB_ACCESS_TOKEN']
        )
        with self.assertRaises(AssertionError) as ctx_manager:
            archiver.identify_target_files()
        self.assertEqual(str(ctx_manager.exception), "Target folder does not exist")

    def test_archiver_raise_error_if_target_folder_is_empty(self):
        archiver = GithubArchiver(
            project_name="empty_folder",
            github_access_token=os.environ['GITHUB_ACCESS_TOKEN']
        )
        with self.assertRaises(AssertionError) as ctx_manager:
            archiver.identify_target_files()
        self.assertEqual(str(ctx_manager.exception), "Target folder is empty")

    # def test_archiver_return_list_of_target_files(self):
    #     target_list = [
    #         "SlipperyGargantuanDebuggers/test-README.md",
    #         "SlipperyGargantuanDebuggers/road.jpg",
    #         "SlipperyGargantuanDebuggers/test.py",
    #         "SlipperyGargantuanDebuggers/main.py",
    #         "SlipperyGargantuanDebuggers/Group-1/test-1.txt",
    #         "SlipperyGargantuanDebuggers/Group-2/test-2.txt",
    #     ]

    #     archiver = GithubArchiver(
    #         project_name="SlipperyGargantuanDebuggers",
    #         xxwgithub_access_token=os.environ['GITHUB_ACCESS_TOKEN']
    #     )
    #     archiver.identify_target_files()
    #     # https://stackoverflow.com/questions/12813633/how-to-assert-two-list-contain-the-same-elements-in-python
    #     self.assertCountEqual(archiver.get_target_files(), target_list)

    # def test_archiver_raise_error_if_target_files_not_set(self):
    #     archiver = GithubArchiver(
    #         project_name="SlipperyGargantuanDebuggers",
    #         github_access_token=os.environ['GITHUB_ACCESS_TOKEN']
    #     )
    #     with self.assertRaises(AssertionError) as ctx_manager:
    #         archiver.commit_to_github()

    #     self.assertEqual(str(ctx_manager.exception), "Target files are not identified")

    # def test_archiver_upload_target_files_to_github(self):
    #     archiver = GithubArchiver(
    #         project_name="SlipperyGargantuanDebuggers",
    #         github_access_token=os.environ['GITHUB_ACCESS_TOKEN']
    #     )
    #     archiver.identify_target_files()
    #     archiver.commit_to_github()

    #     auth = Auth.Token(os.environ['GITHUB_ACCESS_TOKEN'])
    #     g = Github(auth=auth)
    #     repo = g.get_user().get_repo('The-Archive')
    #     commit = repo.get_commit(archiver.get_commit_sha())
    #     target_list = list()
    #     for file in commit.files:
    #         target_list.append(file.filename)
    #     g.close()

    #     self.assertCountEqual(archiver.get_target_files(), target_list)


if __name__ == "__main__":
    unittest.main()
