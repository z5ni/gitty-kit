import os
import configparser
from pathlib import Path


# 현재 스크립트 기준으로 상위 디렉토리의 config.ini 경로 찾기
BASE_DIR = Path(__file__).resolve().parent.parent
config_path = os.path.join(BASE_DIR, "config.ini")


# configparser 설정
config = configparser.ConfigParser()
config.read(config_path)

# 기본 설정
DEFAULT_CONFIG = {
    "api": {"model": "gpt-4o-mini", "key": config.get("API", "OPENAI_API_KEY")},
    "format": {
        "style": "conventional",
    },
    "language": "ko",
}

# 언어 설정
SUPPORT_LANGUAGES = ["ko", "en"]

# 커밋 메시지 스타일 설정
COMMIT_STYLES = ["conventional", "simple"]
