from ai_client import generate_commit_message
from utils.git import git_commit
from setup_manager import ensure_user_config_exists, setup_config, config_load
from ui import UIManager


def main():
    ui = UIManager(cat_mode=True)
    config_exists = ensure_user_config_exists(ui)

    if not config_exists:
        ui.print_cat("초기 설정을 시작합니다.")
        setup_config(ui)

    config = config_load(ui)
    commit_message = generate_commit_message(config)
    ui.print_commit_message(commit_message)
    git_commit(commit_message)


if __name__ == "__main__":
    main()
