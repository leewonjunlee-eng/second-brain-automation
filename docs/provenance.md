# 출처와 기여 경계

기준일은 2026-10-04 (KST)다. 공개 문서는 private 조사 보고서의 source/test/Git-history 대조를 바탕으로 합성했다. 개인 note 본문, credential, auth 자료, raw log, 원본 저장소 주소와 commit hash는 공개하지 않는다.

## 소스에서 공개 예제로

- `capture.py`는 raw note 생성·slug·중복 파일명·YAML metadata 아이디어를 안전한 local-only 예제로 재작성했다. root를 요구하고 Git commit/push를 제거했다. 본문은 여러 줄을 허용하며 `strip()` 후의 문자열을 저장하므로 byte-for-byte 원문 보존이 아니라 정규화된 본문 보존이다. 동시성 안전하지 않고 metadata serializer도 일반 untrusted YAML parser가 아니다.
- 공개 capture의 area enum은 개인 맥락을 드러내지 않도록 AI·개발·커리어·재무 관련 synthetic 범위로 축소했으며, 원본 분류 체계의 완전한 복제가 아니다.
- 날짜·일정 유틸리티는 순수 함수와 synthetic date만 남겼다. 운영 화면·개인 일정·운영 origin은 복사하지 않았다.
- 문서·사례·카탈로그는 private 원문을 그대로 옮긴 것이 아니라 조사 결과를 공개용으로 합성했다.

## upstream과 라이선스

기술적 배경은 [Quartz](https://quartz.jzhao.xyz/), [Hermes](https://hermes-agent.nousresearch.com/docs), [Python](https://docs.python.org/3/), [Node.js](https://nodejs.org/docs/latest/api/), [Cloudflare Workers](https://developers.cloudflare.com/workers/)의 공개 문서를 참조한다. Quartz upstream은 MIT로 식별되지만 community plugin별 조건은 따로 확인해야 한다. 이 저장소는 사용자 작성물에 임의의 MIT/CC grant를 선언하지 않는다.

## 사람과 AI의 역할

사용자는 문제 정의, 원하는 통합 방향, 안전 경계, 운영 판단, 검증 기준을 지시했다. AI assistance는 조사 정리·문서 초안·안전한 예제 구현을 도왔다. 특정 줄을 전부 개인이 직접 작성했다거나 자동화가 live 운영 중이라고 주장하지 않는다.

## 현재 위험 상태

인증 경계 불일치, 배포 검증 우회 이력, live 연동 미검증, capture의 비동시성·정규화 한계는 2026-10-04 현재 공개한 제한이다. 이를 해결된 보안 보장으로 읽어서는 안 된다.
