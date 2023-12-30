from abc import ABC, abstractmethod
import os
from github import Github, Auth, InputGitTreeElement
import base64


class GithubArchiverInterface(ABC):
    @abstractmethod
    def identify_target_files():
        """
        Read list of target files to be pushed to github, excluding replit's system files.
        Raise error if target folder does not exist or is empty.
        """
        pass

    @abstractmethod
    def commit_to_github():
        """
        Commit target files to github.
        """
        pass


class GithubArchiver(GithubArchiverInterface):

    def __init__(self, project_name, github_access_token, commit_message="Auto-archive") -> None:
        self._project_name = project_name
        self._file_paths = dict()
        self._file_list = list()
        self._commit_sha = ""
        self.__github_access_token = github_access_token
        self._commit_message = commit_message

    def get_project_name(self) -> str:
        return self._project_name

    def identify_target_files(self) -> None:
        print("GithubArchiver: Begin to parse target files...")
        download_folder_path = "./screen-shots"
        extracted_folder_path = os.path.join(download_folder_path, self.get_project_name())
        assert os.path.isdir(extracted_folder_path) is True, "Target folder does not exist"
        assert len(os.listdir(extracted_folder_path)) != 0, "Target folder is empty"

        replit_junk = [
            '.cache',
            '.upm',
            '.replit',
            'poetry.lock',
            'pyproject.toml',
            'replit_zip_error_log.txt',
            'replit.nix',
        ]

        # Walk through the directory and its subdirectories
        for root, dirs, files in os.walk(extracted_folder_path):
            for file in files:
                file_full_path = os.path.join(root, file)
                file_relative_path = file_full_path.replace(extracted_folder_path, self.get_project_name())
                if not any(excluded in file_relative_path for excluded in replit_junk):
                    self._file_paths[file_relative_path] = file_full_path
                    self._file_list.append(file_relative_path)

        print("GithubArchiver: Target files are parsed")

    def get_target_files(self) -> list:
        return self._file_list

    def commit_to_github(self) -> None:
        print("GithubArchiver: Begin to upload files to Github...")
        assert len(self._file_list) != 0, "Target files are not identified"
        auth = Auth.Token(self.__github_access_token)
        g = Github(auth=auth)
        repo = g.get_user().get_repo('The-Archive')
        main_branch = repo.get_branch("main")
        main_tree = repo.get_git_tree(sha=main_branch.commit.sha)

        tree = list()
        for file_relative_path, file_full_path in self._file_paths.items():

            with open(file_full_path, "rb") as file:
                file_content = file.read()

            file_content_based64 = base64.b64encode(file_content)

            blob = repo.create_git_blob(
                    content=file_content_based64.decode('utf-8'),
                    encoding="base64"
                )

            tree.append(
                InputGitTreeElement(
                    path=file_relative_path,
                    mode="100644",
                    type="blob",
                    sha=blob.sha,
                )
            )

        new_tree = repo.create_git_tree(
            tree=tree,
            base_tree=main_tree
        )

        commit = repo.create_git_commit(
            message=self._commit_message,
            tree=repo.get_git_tree(sha=new_tree.sha),
            parents=[repo.get_git_commit(main_branch.commit.sha)],
        )

        archive_ref = repo.get_git_ref(ref='heads/main')
        print(f"GithubArchiver: Archive_ref is {archive_ref}")
        self._commit_sha = commit.sha

        # Commit to Github
        archive_ref.edit(sha=commit.sha)
        print("GithubArchiver: Upload complete")

        g.close()

    def get_commit_sha(self) -> str:
        return self._commit_sha
