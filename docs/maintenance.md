# 유지보수 절차

1. private evidence를 다시 공개 파일에 복사하지 않고 source/test/history를 read-only로 대조한다.
2. 개인 데이터와 credential을 제외한 stable AUT/INC mapping을 갱신한다.
3. pure example와 synthetic test를 먼저 실행한다.
4. `python3 scripts/verify.py`, `python3 -m unittest discover -s tests -p 'test_*.py'`, `npm test`, `TZ=Asia/Seoul node --test tests/date.test.mjs` 결과를 기록한다.
5. 변경 snapshot을 별도의 독립 리뷰가 개인정보·출처·보안 관점에서 검토한 뒤에만 공개 여부를 결정한다.

private evidence, raw capture, build cache, log는 커밋하지 않는다. “파일 존재”, “테스트 통과”, “live 검증”을 한 문장에 섞지 않는다.
