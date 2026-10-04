# 사고 목록

기준일: 2026-10-04 (KST). ID는 공개본의 안정 식별자다. 상태는 증거 범위이지 현재 서비스 건강도나 영향 규모의 주장이 아니다.

| ID | 증상 | 원인 | 조치·상태 | 증거·검사 범위 |
|---|---|---|---|---|
| INC-01 | HTML이 코드처럼 보이고 가짜 일정이 섞임 | Markdown block 해석과 placeholder 데이터 | flush-left 카드·실데이터·empty state, 역사적 수정 | `dashboard-ui.test.mjs`, 새 캡처 없음 |
| INC-02 | KST 경계 날짜 어긋남 | 하드코딩·현지 timezone 이중 보정 | KST formatter와 UTC 산술, 역사적 수정 | `date.js`, `date.test.mjs` |
| INC-03 | source 대소문자와 public path 불일치 | Pages 경로 규칙 차이 | public path 정리, 배포 미확인 | 자산 경로 계약, live HTTP 없음 |
| INC-04 | inline script parse/load 실패 | 복잡한 inline 실행 경로 | module 분리, 역사적 수정 | 모듈 계약, browser replay 없음 |
| INC-05 | SPA 이동 후 초기화 누락 | body script 재실행 안 됨 | `nav` hook·idempotent guard | UI 계약, live SPA 없음 |
| INC-06 | Kanban 숨김·좁은 화면 겹침 | 렌더링/overflow/sidebar 배치 | 항상 표시·overflow 보호 | `projects-ui.test.mjs`, 새 시각 캡처 없음 |
| INC-07 | 과거 HMAC 설계와 현재 authorization boundary 불일치 | 정책/구현 경계 변화 | 보안 제품 템플릿으로 재사용하지 않음, 미해결 | pattern-level 문서만, route·exploit 미공개 |
| INC-08 | 401 유형 혼동·오래된 asset | 오류 분류와 cache 경로 | 오류 구분·cache-busting, live 미확인 | 역사적 UI 테스트 |
| INC-09 | daily script가 낡은 inline dashboard를 다시 씀 | runtime 모듈 이동 후 cron 잔여 책임 | metadata·review skeleton만 유지 | cron test 범위, live 미실행 |
| INC-10 | Git 동시 실행·push 전 소비 위험 | working tree 경쟁과 외부 종료 순서 | lock, pull 실패 중단, push 뒤 close; fail-closed 수선은 2026-10-04 기준 로컬 미커밋·미배포 상태이며 분산 원자성을 보장하지 않음 | `test_cron_git_sync.py`, E2E 원자성 없음 |
| INC-11 | 처리된 capture의 원문 보존 필요 | queue 소비와 note 생성의 경계 | note에 raw payload 보존 | `process_web_inbox.py`, private payload 없음 |
| INC-12 | verify 실패를 검증 실패 무시로 통과시킴 | 배포 gate 우회 | 해결 주장 안 함; 공개 CI는 실패 전파 | workflow 문서, 배포 실행 안 함 |
| INC-13 | opportunity merged row와 preference 처리 불일치 | 후보 통합·선호 상태 경계 | merged row 정규화, 역사적 테스트 | `competition_refresh.py`, private auth caveat |
| INC-14 | 사용할 수 없는 model slug로 404, delivery suppression 관찰 | 모델 가용성 변화 | 기록된 model404 incident; 정상 delivery 성공으로 확대 안 함 | 집계형 실행 기록, 원문 ID·수치 비공개 |
| INC-15 | gateway runtime과 disk version 불일치, 재시작 필요 | stale runtime, 도구가 in-process 재시작 거부 | 증상·재시작 필요 확인, 정상화 미확인 | 비공개 운영 관찰 기록, 복구 정상화 미확인 |
| INC-16 | evidence snapshot INSERT가 열 수와 값 수 불일치 | 14개 column에 13개 값 | 로컬 개발 브랜치에서 명시적 14-column INSERT, transaction rollback, cross-cluster fingerprint 회귀를 구현·테스트했지만 2026-10-04 기준 릴리스·배포되지 않음 | 비공개 테스트·수정 기록, 공개 예제에서는 SQL 오류 재현 제외 |

### 전달 억제와 model404는 다른 사건이다

INC-14는 model404다. 별도의 delivery suppression 관찰은 무변경/전달 정책을 model 장애로 오해한 진단 사례이며, 실패한 작업으로 합치지 않는다. 원문 prompt·job ID·연락처는 공개하지 않는다.

모든 사고는 공개 가능한 증거와 검사 범위를 함께 적었다. 실제 route 목록, 서버 origin, exploitation 절차, 개인 로그·자격증명은 기록하지 않는다.
