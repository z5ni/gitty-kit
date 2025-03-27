# Gitty-kit 🐱
AI를 활용한 Git 커밋 메시지 자동 생성 도구 <br>
Gitty-Kit은 변경된 코드를 분석하여 적절한 커밋 메시지를 자동으로 제안합니다!

## ✨ 특징
- 🤖 OpenAI API를 활용한 커밋 메시지 자동 생성
- 🖊️ 텍스트 에디터를 통한 커밋 메시지 수정 기능
- 😸 귀여운 고양이 UI (선택 가능)
- 🌐 한국어/영어 지원
- 📝 Conventional Commits 지원
- ⚙️ 커스터마이징 가능한 설정


## 🚀 설치 방법
```
# 저장소 클론
git clone https://github.com/z5ni/gitty-kit.git
cd gitty-kit

# 필요한 라이브러리 설치
pip install -r requirements.txt
```

## 📖 사용 방법
### 기본 사용법
```
# 변경사항 스테이징 후
git add .

# gitty-kit 실행
python3 gitty_kit
```

### 커밋 메시지 작성 옵션
- `y`: 자동 생성된 커밋 메시지 그대로 사용
- `e`: 텍스트 에디터로 커밋 메시지 수정 후 사용
- `n`: 커밋 취소

## ⚙️ 설정 마법사 
최초 실행 시 설정 마법사가 실행됩니다.

설정을 다시 실행하려면,
```
python3 gitty_kit --config
```

## 🛠️ 설정 옵션
설정 파일은 ~/.gitty-kit/config.json에 저장됩니다.

| 섹션 | 옵션 | 설명 | 기본값 | 가능한 값 |
|------|------|------|--------|-----------|
| api | model | 사용할 OpenAI 모델 | gpt-4o-mini | gpt-4o-mini, gpt-4o, o3-mini |
| api | key | OpenAI API 키 | config.ini에서 불러옴 | 사용자 API 키 |
| format | style | 커밋 메시지 스타일 | conventional | conventional, simple |
| format | max_length | 커밋 제목 최대 길이 | 75 | 숫자 값 |
| language | - | 언어 설정 | ko | ko, en |
| ui | cat_mode | 고양이 UI 사용 여부 | true | true, false |

## 💌 커밋 스타일

### Conventional Commits
```
<type>: <description>

[body]

[footer]
```

✨ 예시
```
feat: 사용자 인증 기능 추가

- 로그인 폼 컴포넌트 구현
- JWT 토큰 처리 로직 추가
- 세션 관리 기능 구현
```

### Simple
✨ 예시:
```
파일 업로드 버그 수정 및 성능 개선
```

## ⚠️ 주의사항
- OpenAI API 사용에 따른 비용이 발생할 수 있습니다.
- 민감한 코드 변경은 API로 전송되니 주의하세요.