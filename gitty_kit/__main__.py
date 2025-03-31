import argparse
import sys

from ai_client import generate_commit_message
from setup_manager import config_load, ensure_user_config_exists, setup_config
from ui import UIManager
from utils.git import git_commit


def parse_arguments():
    """
    명령줄 인수 파싱
    """
    parser = argparse.ArgumentParser(description="Gitty-Kit: Git 커밋 메시지 생성기")
    parser.add_argument("--config", "-c", action="store_true", help="설정 마법사 실행")

    return parser.parse_args()


def main():
    # 0. 명령줄 인수 파싱
    args = parse_arguments()

    # 1. 임시 UI 매니저 생성
    temp_ui = UIManager(cat_mode=True)

    # 2. 설정 파일 확인
    config_exists = ensure_user_config_exists(temp_ui)

    # 3-1. 설정 파일이 없거나 --config(-c) 옵션이 전달된 경우 설정 마법사 실행
    if not config_exists:
        setup_success = setup_config(temp_ui, is_initial_setup=True)

        if not setup_success:
            temp_ui.print_cat("설정이 완료되지 않았습니다. 프로그램을 종료합니다.")
            sys.exit(1)

        temp_ui.print_cat("설정이 완료되었습니다. 다시 실행하여 커밋을 진행하세요.")
        return

    if args.config:
        setup_success = setup_config(temp_ui)

        if not setup_success:
            temp_ui.print_cat("설정이 완료되지 않았습니다. 프로그램을 종료합니다.")
            sys.exit(1)

        temp_ui.print_cat("설정이 완료되었습니다. 다시 실행하여 커밋을 진행하세요.")
        return

    # 3-2. 설정 로드
    app_config = config_load(temp_ui)

    # 4. 설정에서 cat_mode 가져와서 실제 사용할 UI 매니저 생성
    cat_mode = app_config.ui.cat_mode
    ui = UIManager(cat_mode=cat_mode)

    # 5. 커밋 처리
    ui.print_cat("Gitty-Kit이 시작되었습니다.")
    commit_message = generate_commit_message(app_config)

    if commit_message is None:
        ui.print_cat("변경사항이 없습니다.")
        return

    ui.print_commit_message(commit_message)

    choice = ui.get_user_choices()
    if choice == "y":
        git_commit(commit_message)
        ui.print_success("커밋 완료!")
    elif choice == "e":
        modified_message = ui.edit_commit_message(commit_message)

        if modified_message.strip():
            # 수정된 메시지 보여주기
            ui.print_cat("수정된 커밋 메시지:", "📝")
            ui.print_separator()
            print(modified_message)
            ui.print_separator()

            # 최종 확인
            confirm = ui.get_user_choices("이 메시지로 커밋할까요? (y: 예, n: 아니오) ")
            if confirm == "y":
                git_commit(modified_message)
                ui.print_success("수정된 메시지로 커밋 완료!")
            else:
                ui.print_cat("커밋이 취소되었습니다.")

        else:
            ui.print_cat("커밋이 취소되었습니다.")
    else:
        ui.print_cat("커밋이 취소되었습니다.")


if __name__ == "__main__":
    main()
