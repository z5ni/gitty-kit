from ai_client import generate_commit_message
from utils.git import git_commit


def main():
    commit_message = generate_commit_message()
    git_commit(commit_message)


if __name__ == "__main__":
    main()
