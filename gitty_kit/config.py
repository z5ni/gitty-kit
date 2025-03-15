import os
import configparser
from pathlib import Path


# 현재 스크립트 기준으로 상위 디렉토리의 config.ini 경로 찾기
BASE_DIR = Path(__file__).resolve().parent.parent
config_path = os.path.join(BASE_DIR, "config.ini")


# configparser 설정
config = configparser.ConfigParser()
config.read(config_path)

OPENAI_API_KEY = config.get("API", "OPENAI_API_KEY")
