import random
from config import CAT_EMOJIS


def print_cat(message, emoji=None):
    """
    print message with cat emoji
    """
    if emoji is None:
        emoji = random.choice(CAT_EMOJIS)

    print(f"{emoji} {message}")


def print_error(message, exit_code=None):
    """
    에러 메시지 출력 후 프로그램 종료
    """
    print_cat(message, "😿")


def print_success(message):
    """
    성공 메시지 출력
    """
    print_cat(message, "😻")


def print_separator():
    """
    구분선 출력
    """
    print("-" * 50)


def print_commit_message(commit_message):
    """
    커밋 메시지 출력
    """

    print_cat("Gitty의 제안:", "🐾")
    print_separator()
    print(commit_message)
    print_separator()


def get_user_choices(prompt="커밋 메시지를 바로 적용할까요? (y: yes, n: no, e: edit) "):
    """
    사용자 선택 입력
    """
    return input(f"\n{prompt}").lower()
