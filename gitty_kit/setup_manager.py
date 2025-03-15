from config import (
    DEFAULT_CONFIG,
    CONFIG_DIR,
    CONFIG_FILE,
)
import os
import json


def ensure_user_config_exists():
    """
    설정 파일 존재 확인 후 없을 경우 생성
    """

    # 폴더 없을 경우 생성
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        print(f"설정 파일 생성: {CONFIG_FILE}")
        return False

    return True


def config_load():
    """
    설정 파일 읽기
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

        # 기본값 누락된 경우 추가
        for section in DEFAULT_CONFIG:
            if section not in config:
                config[section] = DEFAULT_CONFIG[section]
            elif isinstance(DEFAULT_CONFIG[section], dict):
                for key in DEFAULT_CONFIG[section]:
                    if key not in config[section]:
                        config[section][key] = DEFAULT_CONFIG[section][key]

        return config
    except Exception as e:
        print(f"설정 파일 읽기 오류: {str(e)}")
        print("기본 설정을 사용합니다.")
        return DEFAULT_CONFIG.copy()


def config_save(config):
    """
    설정 파일 저장
    """
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True

    except Exception as e:
        print(f"설정 파일 저장 오류: {str(e)}")
        return False


def setup_config():
    """
    설정 CLI
    """
    from config import OPENAI_MODEL, COMMIT_STYLES, SUPPORT_LANGUAGES

    config = config_load()

    print("\n Gitty-Kit 설정 마법사")

    # 1. API 설정
    print("🔑 API 설정")
    print("-----------------")

    api_key = input(f"API 키: ")

    models = OPENAI_MODEL["model"]
    model_options = ", ".join(models)
    model = input(f"사용할 모델 ({model_options}) [{models[0]}]: ") or models[0]

    # 2. 커밋 메시지 형식 설정
    print("\n커밋 메시지 형식 설정")
    style_options = ", ".join(COMMIT_STYLES)
    style = input(f"커밋 스타일 ({style_options}) [conventional]: ") or "conventional"

    # 3. 언어 설정
    lang_options = ", ".join(SUPPORT_LANGUAGES)
    language = input(f"\n기본 언어 ({lang_options}) [ko]: ") or "ko"

    # 4. 커밋 제목 최대 길이
    max_length = input(f"\n커밋 제목 최대 길이: ") or 75

    config["api"]["key"] = api_key
    config["api"]["model"] = model
    config["format"]["style"] = style
    config["format"]["max_length"] = max_length
    config["language"] = language

    if config_save(config):
        print("\n설정이 저장되었습니다")
        return True

    else:
        return False


def main():
    config_exists = ensure_user_config_exists()

    if not config_exists:
        print("초기 설정 시작")
        setup_config()

    config = config_load()

    # 메인 프로그램 실행 로직
    print("Gitty-Kit이 시작되었습니다.")
    print(f"현재 언어: {config['language']}")
    print(f"선택된 모델: {config['api']['model']}")
    print(f"커밋 스타일: {config['format']['style']}")
    print(f"커밋 제목 최대 길이: {config['format']['max_length']}")


if __name__ == "__main__":
    main()
