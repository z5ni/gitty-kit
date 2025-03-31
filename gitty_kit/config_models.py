from dataclasses import dataclass
from typing import Literal, Optional

from config import COMMIT_STYLES, OPENAI_MODEL, SERVER_CONFIG, SUPPORT_LANGUAGES


@dataclass
class ApiConfig:
    key: str
    model: str

    def __post_init__(self):
        if not self.key:
            raise ValueError("API가 설정되지 않았습니다.")

        if self.model not in OPENAI_MODEL["model"]:
            raise ValueError(
                f"유효하지 않은 model 설정입니다. 지원되는 모델: {', '.join(OPENAI_MODEL['model'])}"
            )


@dataclass
class FormatConfig:
    style: str
    max_length: int
    language: str

    def __post_init__(self):
        if self.style not in COMMIT_STYLES:
            raise ValueError(
                f"유효하지 않은 style 설정입니다. 지원되는 스타일: {', '.join(COMMIT_STYLES)}"
            )

        if not isinstance(self.max_length, int):
            try:
                self.max_length = int(self.max_length)
            except (ValueError, TypeError):
                raise ValueError(
                    f"max_length는 숫자여야 합니다. 현재 값: {self.max_length}"
                )

        if self.max_length < 10 or self.max_length > 100:
            raise ValueError(
                f"max_length는 10에서 100 사이여야 합니다. 현재 값: {self.max_length}"
            )

        if self.language not in SUPPORT_LANGUAGES:
            raise ValueError(
                f"유효하지 않은 language 설정입니다. 지원되는 언어: {', '.join(SUPPORT_LANGUAGES)}"
            )


@dataclass
class UiConfig:
    cat_mode: bool


@dataclass
class ServerConfig:
    mode: Literal["local", "lambda"] = "local"
    lambda_url: Optional[str] = None

    def __post_init__(self):
        if self.mode not in SERVER_CONFIG:
            raise ValueError("서버 모드가 'local' 또는 'lambda'여야 합니다.")

        if self.mode == "lambda" and not self.lambda_url:
            raise ValueError("Lambda 모드를 사용할 경우 lambda_url이 필요합니다.")


@dataclass
class AppConfig:
    api: ApiConfig
    format: FormatConfig
    ui: UiConfig
    server: Optional[ServerConfig] = None

    def __post_init__(self):
        if self.server is None:
            self.server = ServerConfig()
