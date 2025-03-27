import os
import random
import subprocess
import tempfile

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

    def get_editor(self):
        """
        사용자 시스템의 기본 에디터 가져오기
        """
        editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")

        # 기본 에디터가 설정되어 있지 않은 경우
        if not editor:
            if os.name == "nt":  # windows
                editor = "notepad"
            else:  # linux/Unix/Mac
                for possible_editor in ["vi", "vim", "nano"]:
                    try:
                        if subprocess.call(
                            ["which", possible_editor],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE == 0,
                        ):
                            editor = possible_editor
                    except Exception as e:
                        print(str(e))
                        continue

            # 아무 에디터도 찾지 못한 경우
            if not editor:
                editor = "vi"
        return editor

    def edit_commit_message(self, commit_message):
        """
        에디터를 통해 커밋 메시지 수정
        """
        editor = self.get_editor()

        # 임시 파일 생성성
        with tempfile.NamedTemporaryFile(
            suffix=".tmp", mode="+w", delete=False
        ) as temp:
            temp_filename = temp.name
            temp.write(commit_message)
            temp.write("\n\n# 이 줄 위에 커밋 메시지를 작성하세요.")
            temp.write("\n# '#'으로 시작하는 줄은 무시됩니다.")
            temp.flush()

        try:
            subprocess.call([editor, temp_filename])

            # 수정된 내용 읽기
            with open(temp_filename, "r") as temp:
                modified_message_lines = []

                # 주석 처리된 라인 제외외
                for line in temp:
                    if not line.strip().startswith("#"):
                        modified_message_lines.append(line)

                modified_message = "".join(modified_message_lines).strip()
                return modified_message

        finally:
            # 임시 파일 삭제
            os.unlink(temp_filename)

    def get_user_choices(
        self,
        prompt="커밋 메시지를 바로 적용할까요? (y: 바로 적용, e: 수정 후 적용, n: 취소) ",
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
