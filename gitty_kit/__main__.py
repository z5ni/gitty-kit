from ai_client import generate_commit_message
from utils.git import git_commit
from setup_manager import ensure_user_config_exists, setup_config, config_load


def main():
    config_exists = ensure_user_config_exists()

    if not config_exists:
        print("초기 설정을 시작합니다.")
        setup_config()

    config = config_load()
    commit_message = generate_commit_message(config)
    git_commit(commit_message)


if __name__ == "__main__":
    main()
