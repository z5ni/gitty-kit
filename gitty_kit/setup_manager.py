import json
import os

from config import CONFIG_DIR, CONFIG_FILE, DEFAULT_CONFIG


def ensure_user_config_exists(ui):
    """
    설정 파일 존재 확인 후 없을 경우 생성
    """

    # 폴더 없을 경우 생성
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        ui.print_cat(f"설정 파일 생성: {CONFIG_FILE}")
        return False

    return True


def config_load(ui):
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
        ui.print_error(f"설정 파일 읽기 오류: {str(e)}")
        ui.print_cat("기본 설정을 사용합니다.")
        return DEFAULT_CONFIG.copy()


def config_save(config, ui):
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
        ui.print_error(f"설정 파일 저장 오류: {str(e)}")
        return False


def setup_config(ui):
    """
    설정 CLI
    """
    from config import COMMIT_STYLES, OPENAI_MODEL, SUPPORT_LANGUAGES

    config = config_load(ui)

    ui.print_cat("\n Gitty-Kit 설정 마법사")

    # 1. API 설정
    ui.print_cat("🔑 API 설정")
    ui.print_separator()

    api_key = input("API 키: ") or DEFAULT_CONFIG["api"]["key"]

    models = OPENAI_MODEL["model"]
    model_options = ", ".join(models)
    model = input(f"사용할 모델 ({model_options}) [{models[0]}]: ") or models[0]

    # 2. 커밋 메시지 형식 설정
    ui.print_cat("\n커밋 메시지 형식 설정")
    style_options = ", ".join(COMMIT_STYLES)
    style = input(f"커밋 스타일 ({style_options}) [conventional]: ") or "conventional"

    # 3. 언어 설정
    lang_options = ", ".join(SUPPORT_LANGUAGES)
    language = input(f"\n기본 언어 ({lang_options}) [ko]: ") or "ko"

    # 4. 커밋 제목 최대 길이
    max_length = input("\n커밋 제목 최대 길이: ") or 75

    # 5. cat_mode 설정
    cat_mode_input = input("고양이 이모지 UI 사용 (y/n) [y]: ") or "y"
    cat_mode = cat_mode_input.lower() == "y"

    config["api"]["key"] = api_key
    config["api"]["model"] = model
    config["format"]["style"] = style
    config["format"]["max_length"] = max_length
    config["language"] = language
    config["ui"]["cat_mode"] = cat_mode

    if config_save(config, ui):
        ui.print_cat("\n설정이 저장되었습니다")
        return True

    else:
        return False
