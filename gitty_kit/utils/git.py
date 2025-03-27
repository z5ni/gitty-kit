import subprocess

# subprocess.run 함수
# 첫 번째 위치 인자 (필수)
# cwd (선택): 명령어를 실행할 작업 디렉토리
# capture_output (선택): True로 설정하면 표준 출력(stdout)과 표준 오류(stderr)를 캡처
# check (선택): True로 설정하면 명령어가 실패할 경우 subprocess.CalledProcessError 예외를 발생
# text (선택): True로 설정하면 입출력을 문자열(string)로 처리


def git_init(directory="."):
    """
    git init
    """
    try:
        result = subprocess.run(
            ["git", "init"], cwd=directory, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"git init 명령 실패: {e.stderr}")
        return False


def git_add(paths=".", directory="."):
    """
    git add
    """
    if isinstance(paths, str):
        paths = [paths]

    cmd = ["git", "add"] + paths
    try:
        result = subprocess.run(
            cmd, cwd=directory, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"error: {e.stderr}")
        return False


def git_commit(message, directory="."):
    """
    git commit
    """
    try:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=directory,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in e.stderr:
            print(e.stdout)
            print(f"info: {e.stderr}")
            return False
        else:
            print(f"error: {e.stderr}")
            return False


def git_diff(path=None, staged=True, directory="."):
    """
    git diff
    """
    cmd = ["git", "diff"]

    if staged:
        cmd.append("--staged")

    if path:
        cmd.append(path)

    try:
        result = subprocess.run(
            cmd, cwd=directory, check=True, capture_output=True, text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"오류: {e.stderr}")
        return None


if __name__ == "__main__":
    # exit(1)을 사용하여 프로그램을 종료
    try:
        if git_init():
            print("✅ git 저장소 초기화 완료")
        else:
            print("❌ git 저장소 초기화 실패")
            exit(1)

        if git_add():
            print("✅ 모든 파일을 스테이징 영역에 추가")
        else:
            print("❌ 파일 스테이징 실패")
            exit(1)

        # # 특정 파일만 추가하려면 아래 코드 사용
        # if git_add(['test1.txt', 'test2.txt']):
        #     print("✅ 지정된 파일들을 스테이징 영역에 추가")
        # else:
        #     print("❌ 지정된 파일 스테이징 실패")
        #     exit(1)

        if git_commit("커밋 생성하기"):
            print("✅ 변경 사항 커밋 완료")
        else:
            print("❌ 커밋 실패")
            exit(1)

        print("🎉 모든 Git 작업이 성공적으로 완료되었습니다!")

    except KeyboardInterrupt:
        print("\n❗ 사용자에 의해 프로그램이 중단되었습니다.")
        exit(1)
    except Exception as e:
        print(f"❗ 예상치 못한 오류 발생: {str(e)}")
        exit(1)
