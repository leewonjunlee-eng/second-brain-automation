# 검증 방법

이 공개본의 기준일은 2026-10-04 (KST)다. `python3 scripts/verify.py`는 Python unittest, `TZ=UTC`와 `TZ=Asia/Seoul` 각각의 Node 테스트, release scanner, SVG XML parse, required `--root` CLI 임시 실행을 연속으로 수행하며 각 Node 환경을 출력한다.

검증 항목은 두 번의 순차 capture와 정규화된 본문 보존, 여러 줄 본문 보존, KST 자정 직전·직후, UTC/`Asia/Seoul` 독립성, 일요일·연말·윤년, valid/invalid time·day·range, occurrence 범위 안팎, Markdown 상대 경로·anchor, stable ID, 금지 파일명·secret·내부 경로 heuristic이다. `scripts/verify.py`가 `python3 -m unittest discover -s tests -p 'test_*.py'`를 실제로 한 번 실행한다.

검증하지 않는 항목은 production endpoint/API, scheduler, credential, live message, deployment, browser screenshot, original repository mutation이다. scanner는 모든 secret을 보장하지 않으며 별도의 secret scan과 독립 review가 추가 공개 전 gate다.
