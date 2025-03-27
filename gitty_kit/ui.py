import random

from config import CAT_EMOJIS


class UIManager:
    def __init__(self, cat_mode=True):
        """
        UI 관리자 클래스 초기화
        """
        self.cat_mode = cat_mode

    def print_cat(self, message, emoji=None):
        """
        고양이 이모지와 함께 메시지 출력
        """
        if not self.cat_mode:
            print(message)
            return

        if emoji is None:
            emoji = random.choice(CAT_EMOJIS)

        print(f"{emoji} {message}")

    def print_error(self, message, exit_code=None):
        """
        에러 메시지 출력 후 프로그램 종료
        """
        if not self.cat_mode:
            print(f"오류: {message}")
        else:
            self.print_cat(message, "😿")

        if exit_code is not None:
            exit(exit_code)

    def print_success(self, message):
        """
        성공 메시지 출력
        """
        if not self.cat_mode:
            print(f"성공: {message}")
        else:
            self.print_cat(message, "😻")

    def print_separator(self):
        """
        구분선 출력
        """
        print("-" * 50)

    def print_commit_message(self, commit_message):
        """
        커밋 메시지 출력
        """
        if not self.cat_mode:
            print("\n제안된 커밋 메시지:")
        else:
            self.print_cat("Gitty의 제안:", "🐾")

        self.print_separator()
        print(commit_message)
        self.print_separator()

    def get_user_choices(
        self, prompt="커밋 메시지를 바로 적용할까요? (y: yes, n: no) "
    ):
        """
        사용자 선택 입력
        """
        return input(f"\n{prompt}").lower()

    def print_info(self, message):
        """
        정보 메시지 출력
        """
        if not self.cat_mode:
            print(f"정보: {message}")
        else:
            self.print_cat(message, "🐱")

    def set_cat_mode(self, cat_mode):
        """
        고양이 모드 설정 변경
        """
        self.cat_mode = cat_mode
