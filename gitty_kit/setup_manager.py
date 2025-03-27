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


def setup_config(ui, is_initial_setup=False):
    """
    설정 CLI
    """
    from config import COMMIT_STYLES, OPENAI_MODEL, SUPPORT_LANGUAGES

    config = config_load(ui)

    if is_initial_setup:
        config = DEFAULT_CONFIG.copy()
        ui.print_cat("Gitty-Kit 초기 설정 마법사 \n")
    else:
        config = config_load(ui)
        ui.print_cat("Gitty-Kit 설정 변경 마법사 \n")

    # 1. API 설정
    print("🔑 API 설정")
    ui.print_separator()

    api_key_display = (
        config["api"]["key"][:4] + "****" if config["api"]["key"] else "none"
    )
    api_key = input(f"API 키 [{api_key_display}]: ") or config["api"]["key"]

    # 1. 모델 선택
    models = OPENAI_MODEL["model"]
    model_options = ", ".join(models)
    model = (
        input(f"사용할 모델 ({model_options}) [{config['api']['model']}]: ")
        or config["api"]["model"]
    )

    print()
    # 2. 커밋 메시지 형식 설정
    ui.print_cat("커밋 메시지 형식 설정")
    ui.print_separator()
    style_options = ", ".join(COMMIT_STYLES)
    style = (
        input(f"커밋 스타일 ({style_options}) [{config['format']['style']}]: ")
        or config["format"]["style"]
    )

    # 3. 언어 설정
    lang_options = ", ".join(SUPPORT_LANGUAGES)
    language = (
        input(f"기본 언어 ({lang_options}) [{config['language']}]: ")
        or config["language"]
    )

    # 4. 커밋 제목 최대 길이
    max_length = (
        input(f"커밋 제목 최대 길이 [{config['format']['max_length']}]: ")
        or config["format"]["max_length"]
    )

    print()
    ui.print_cat("mode 설정")
    ui.print_separator()
    # 5. cat_mode 설정
    cat_mode_str = "y" if config["ui"]["cat_mode"] else "n"
    cat_mode_input = (
        input(f"고양이 이모지 UI 사용 (y/n) [{cat_mode_str}]: ") or cat_mode_str
    )
    cat_mode = cat_mode_input.lower() == "y"

    config["api"]["key"] = api_key
    config["api"]["model"] = model
    config["format"]["style"] = style
    config["format"]["max_length"] = max_length
    config["language"] = language
    config["ui"]["cat_mode"] = cat_mode

    if config_save(config, ui):
        print()
        return True

    else:
        return False
