from ai_client import generate_commit_message
from utils.git import git_commit
from setup_manager import ensure_user_config_exists, setup_config, config_load
from ui import UIManager


def main():
    # 1. 설정 파일이 없으면 기본 UI로 초기 설정 진행
    temp_ui = UIManager(cat_mode=True)
    config_exists = ensure_user_config_exists(temp_ui)

    if not config_exists:
        temp_ui.print_cat("초기 설정을 시작합니다.")
        setup_config(temp_ui)

    # 2. 설정 로드
    config = config_load(temp_ui)

    # 3. 설정에서 cat_mode 가져와서 실제 사용할 UI 매니저 생성
    cat_mode = config.get("ui", {}).get("cat_mode", True)
    ui = UIManager(cat_mode=cat_mode)

    # 4. 커밋 처리
    ui.print_cat("Gitty-Kit이 시작되었습니다.")
    commit_message = generate_commit_message(config)

    if commit_message is None:
        ui.print_cat("변경사항이 없습니다.")
        return

    ui.print_commit_message(commit_message)

    choice = ui.get_user_choices()
    if choice == "y":
        git_commit(commit_message)
        ui.print_success("커밋 완료!")
    else:
        ui.print_cat("커밋이 취소되었습니다.")


if __name__ == "__main__":
    main()
