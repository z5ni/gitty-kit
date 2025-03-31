import json
import os

from config import (
    COMMIT_STYLES,
    CONFIG_DIR,
    CONFIG_FILE,
    DEFAULT_CONFIG,
    OPENAI_MODEL,
    SERVER_CONFIG,
    SUPPORT_LANGUAGES,
)
from config_models import ApiConfig, AppConfig, UiConfig, FormatConfig, ServerConfig


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


def config_to_dataclass(config_dict):
    """
    설정 딕셔너리를 데이터클래스 객체로 변환
    """
    try:
        api_config = ApiConfig(
            key=config_dict["api"]["key"], model=config_dict["api"]["model"]
        )

        format_config = FormatConfig(
            style=config_dict["format"]["style"],
            max_length=int(config_dict["format"]["max_length"]),
            language=config_dict["language"],
        )

        ui_config = UiConfig(cat_mode=config_dict["ui"]["cat_mode"])

        server_config = None
        if "server" in config_dict:
            server_config = ServerConfig(
                mode=config_dict["server"].get("mode", "local"),
                lambda_url=config_dict["server"].get("lambda_url"),
            )

        return AppConfig(
            api=api_config, format=format_config, ui=ui_config, server=server_config
        )

    except Exception as e:
        raise ValueError(f"설정 변환 오류: {str(e)}")


def dataclass_to_config(app_config):
    """
    데이터클래스 객체를 설정 딕셔너리로 변환
    """
    config = {
        "api": {
            "key": app_config.api.key,
            "model": app_config.api.model,
        },
        "format": {
            "style": app_config.format.style,
            "max_length": str(app_config.format.max_length),
        },
        "language": app_config.format.language,
        "ui": {
            "cat_mode": app_config.ui.cat_mode,
        },
    }

    if app_config.server:
        config["server"] = {
            "mode": app_config.server.mode,
        }
        if app_config.server.lambda_url:
            config["server"]["lambda_url"] = app_config.server.lambda_url

    return config


def config_load(ui):
    """
    설정 파일 읽기 및 데이터클래스로 변환
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            config_dict = json.load(f)

        # 기본값 누락된 경우 추가
        for section in DEFAULT_CONFIG:
            if section not in config_dict:
                config_dict[section] = DEFAULT_CONFIG[section]
            elif isinstance(DEFAULT_CONFIG[section], dict):
                for key in DEFAULT_CONFIG[section]:
                    if key not in config_dict[section]:
                        config_dict[section][key] = DEFAULT_CONFIG[section][key]

        return config_to_dataclass(config_dict)
    except Exception as e:
        ui.print_error(f"설정 파일 읽기 오류: {str(e)}")
        ui.print_cat("기본 설정을 사용합니다.")
        return config_to_dataclass(DEFAULT_CONFIG.copy())


def config_save(app_config, ui):
    """
    데이터클래스 설정을 파일로 저장
    """
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    try:
        # dataclass to dictionary
        config_dict = dataclass_to_config(app_config)

        with open(CONFIG_FILE, "w") as f:
            json.dump(config_dict, f, indent=2)
        return True
    except Exception as e:
        ui.print_error(f"설정 파일 저장 오류: {str(e)}")
        return False


def setup_config(ui, is_initial_setup=False):
    """
    설정 CLI
    """

    if is_initial_setup:
        app_config = config_to_dataclass(DEFAULT_CONFIG.copy())
        ui.print_cat("Gitty-Kit 초기 설정 마법사 \n")
    else:
        app_config = config_load(ui)
        ui.print_cat("Gitty-Kit 설정 변경 마법사 \n")

    # 0. 서버 설정
    print("🖥️ 서버 설정")
    ui.print_separator()

    server_mode_options = ", ".join(SERVER_CONFIG)
    current_server_mode = app_config.server.mode if app_config.server else "local"
    server_mode = (
        input(f"서버 모드 ({server_mode_options}) [{current_server_mode}]: ")
        or current_server_mode
    )

    # lambda URL 설정(서버 모드가 lambda인 경우) -> TODO: lambda 사용 시 lambda에서 url 전달받도록 변경
    lambda_url = None
    if server_mode == "lambda":
        current_lambda_url = (
            app_config.server.lambda_url
            if (app_config.server and app_config.server.lambda_url)
            else ""
        )
        lambda_url = input(f"Lambda URL [{current_lambda_url}]: ") or current_lambda_url
        if not lambda_url:
            ui.print_error("Lambda 모드를 사용할 경우 Lambda URL이 필요합니다.")
            return False

    print()

    # 1. API/모델 설정 - lambda 모드가 아닐 경우에만
    api_key = app_config.api.key
    model = app_config.api.model

    # TODO: lambda 코드 안에서 api_key, model 값 전달받을 경우 아래 코드 주석 해제 필요
    # if server_mode == "local":
    print("🔑 API 설정")
    ui.print_separator()

    api_key_display = app_config.api.key[:4] + "****" if app_config.api.key else "none"
    api_key = input(f"API 키 [{api_key_display}]: ") or app_config.api.key

    models = OPENAI_MODEL["model"]
    model_options = ", ".join(models)
    model = (
        input(f"사용할 모델 ({model_options}) [{app_config.api.model}]: ")
        or app_config.api.model
    )

    print()

    # 2. 커밋 메시지 형식 설정
    ui.print_cat("커밋 메시지 형식 설정")
    ui.print_separator()
    style_options = ", ".join(COMMIT_STYLES)
    style = (
        input(f"커밋 스타일 ({style_options}) [{app_config.format.style}]: ")
        or app_config.format.style
    )

    # 3. 언어 설정
    lang_options = ", ".join(SUPPORT_LANGUAGES)
    language = (
        input(f"기본 언어 ({lang_options}) [{app_config.format.language}]: ")
        or app_config.format.language
    )

    # 4. 커밋 제목 최대 길이
    max_length = (
        input(f"커밋 제목 최대 길이 [{app_config.format.max_length}]: ")
        or app_config.format.max_length
    )

    print()
    ui.print_cat("mode 설정")
    ui.print_separator()

    # 5. cat_mode 설정
    cat_mode_str = "y" if app_config.ui.cat_mode else "y"
    cat_mode_input = (
        input(f"고양이 이모지 UI 사용 (y/n) [{cat_mode_str}]: ") or cat_mode_str
    )
    cat_mode = cat_mode_input.lower() == "y"

    # 데이터클래스 객체 업데이트
    try:
        new_api_config = ApiConfig(key=api_key, model=model)

        new_format_config = FormatConfig(
            style=style,
            max_length=int(max_length) if isinstance(max_length, str) else max_length,
            language=language,
        )

        new_ui_config = UiConfig(cat_mode=cat_mode)

        # TODO: lambda_url 설정 지우기
        new_server_config = ServerConfig(mode=server_mode, lambda_url=lambda_url)

        new_app_config = AppConfig(
            api=new_api_config,
            format=new_format_config,
            ui=new_ui_config,
            server=new_server_config,
        )

        if config_save(new_app_config, ui):
            print()
            return True
        else:
            return False

    except ValueError as e:
        ui.print_error(f"설정 업데이트 오류: {str(e)}")
        return False
