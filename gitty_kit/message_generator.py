def prepare_prompt(style, lang):
    if style == "conventional":
        prompt = f"""다음 Git 변경사항을 분석하고, Conventional Commits 형식으로 커밋 메시지를 작성해주세요:
        
            타입은 다음 중 하나를 사용하세요: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

            커밋 메시지 형식:
            <type>: <description>

            [body]

            [footer]

            간결하고 명확하게 작성해주세요. 
            사용 언어: {lang}
            """

    else:
        prompt = f"""다음 Git 변경사항을 분석하고, 간결한 커밋 메시지를 작성해주세요:

            간결하고 명확하게 작성해주세요.
            사용 언어: {lang}
            """

    return prompt
