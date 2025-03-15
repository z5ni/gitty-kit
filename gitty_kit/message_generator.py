def prepare_prompt(style, lang, max_length):
    if style == "conventional":
        prompt = f"""다음 Git 변경사항을 분석하고, Conventional Commits 형식으로 커밋 메시지를 작성해주세요:
        
            타입은 다음 중 하나를 사용하세요: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

            커밋 메시지 형식:
            <type>: <description>

            [body]

            [footer]

            간결하고 명확하게 작성해주세요.
            body의 경우에는 - 를 사용해 한 줄씩 입력해주세요.
            사용 언어: {lang}

            제목은 {max_length} 이내로 해주세요.

            코드 블럭을 사용하지 않고 커밋 메시지 내용만 입력해주세요.
            """

    else:
        prompt = f"""다음 Git 변경사항을 분석하고, 간결한 커밋 메시지를 작성해주세요:

            간결하고 명확하게 작성해주세요.
            사용 언어: {lang}

            제목은 {max_length} 이내로 해주세요.
            코드 블럭을 사용하지 않고 커밋 메시지 내용만 입력해주세요.
            """

    return prompt
