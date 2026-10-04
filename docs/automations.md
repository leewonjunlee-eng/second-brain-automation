# 자동화 목록

기준일: 2026-10-04 (KST). 상태는 소스·테스트·구성 증거의 범위이며 live 성공이나 현재 운영 보장을 뜻하지 않습니다. 아래 비공개 원본 근거 파일명은 이 저장소에 존재하거나 공개 실행 가능한 파일이라는 뜻이 아닙니다.

| ID | 범주와 입력 | 출력·발동 | 구현/구성/계획 상태 | 안전한 근거 파일·검사 |
|---|---|---|---|---|
| AUT-01 | 수동 CLI raw text | Inbox Markdown / 명령 실행 | 구현·검증 | 공개 파일: `examples/capture.py`, `tests/test_capture.py` |
| AUT-02 | Telegram 접두사·문장 | category/area/tag 추론 | 구현, Gateway 연결 미확인 | `telegram_capture.py`, `test_telegram_capture.py` |
| AUT-03 | 웹 입력 JSON | queue JSON / form event | 구현, 로컬 계약만 검증 | `content/static/app/dashboard.js`, Worker 진입 모듈(비공개) |
| AUT-04 | queue·web-inbox Issue | Inbox note와 원본 payload | 구현, fail-closed 수선은 2026-10-04 기준 로컬 미커밋·미배포 상태이며 분산 원자성을 보장하지 않음 | `process_web_inbox.py`, `test_cron_git_sync.py` |
| AUT-05 | 미처리 Inbox | 상태 분류·보관 | 구성된 hourly 자동화 흐름, live 재검증 안 함 | 비공개 Inbox 분류 래퍼, 상태 규칙 |
| AUT-06 | KST 날짜 | Dashboard metadata·주간 skeleton / 매일 | 소스 구현, scheduler 효과 미확인 | `update_daily_dashboard.py` |
| AUT-07 | Inbox·project·Git 이력 | weekly review Markdown / 일요일 | 구현·dry-run/no-commit | `weekly_review.py`, `test_weekly_review.py` |
| AUT-08 | 오래된 Trash note | 후보 목록 또는 삭제 / 주간 | 구현·dry-run, live 미실행 | `purge_trash.py` |
| AUT-09 | 일정 입력·events JSON | 월간 달력·schedule write | 구현·계약 테스트, live origin 미확인 | `calendar.js`, `schedule-utils.js`, `inbox-worker.test.mjs` |
| AUT-10 | project frontmatter | deterministic manifest·Kanban | 구현·테스트 | `build_projects_manifest.py`, `projects.js`, `projects-ui.test.mjs` |
| AUT-11 | 공식 공고·대학 source | JSON/Markdown opportunity library | 소스 구현·live 일정 미확인 | `daily_opportunity_refresh.py`, `fetch_university_opportunities.py`, `competition_refresh.py` |
| AUT-12 | AI 뉴스와 시장 자료 | 서로 다른 briefings·전달 결과 | 비공개 scheduler 구성 조사, 원문·prompt 제외 | 비공개 구성 증거(이 문서 자체는 근거 아님) |
| AUT-13 | 장학금·인턴·공모전·대외활동 | opportunity 후보·checked metadata | 구성된 조사 범주, 결과 live 주장 안 함 | `daily_opportunity_refresh.py`, `competition_refresh.py` |
| AUT-14 | 공식 AI 출처 | 승인된 editorial·asset manifest·로컬 carousel | 로컬 개발 브랜치에서 구현·테스트·dry-run·게시 전 준비 단계, 2026-10-04 기준 릴리스·배포되지 않음(자동 게시 없음) | 비공개 근거: `ingest.py`, `editorial.py`, `test_editorial.py`; [증거 파이프라인 사례](case-studies/evidence-pipeline.md)는 서술 링크이며 1차 근거가 아님 |
| AUT-15 | backup 대상·update check | 백업 후 검사 결과 | 구성, 실제 업그레이드 아님 | 비공개 백업·업데이트 검사 래퍼 |
| AUT-16 | 오래된 Chromium/프로세스 후보 | SIGTERM 대상 후보 | 구성, 소유권·실행 미확인 | 안전성 한계만 기록 |
| AUT-17 | private preference와 manifest | preference 정규화 / project archive / browser 완료 상태 | 서로 분리된 구현 | `normalize_competition_preferences.py`, `build_projects_manifest.py`, `schedule-checkboxes.js` |
| AUT-18 | legacy Notion 계획과 Obsidian 템플릿 | 수동 dashboard/schema 골격 | 역사적·수동/계획, 현행 실행 자동화 아님 | 비공개 계획·템플릿 관찰, 실행 코드 없음 |

### AI 읽을거리 파이프라인

AUT-14는 단순 dry-run wrapper가 아니다. `ingest.py`의 수집 → `dedupe.py` 중복 제거 → `rank.py` 랭킹/주제 제안 → `approvals.py` 감사 가능한 승인 → `editorial.py` evidence-bound editorial → `assets.py` asset manifest → `renderer.py` 결정적 로컬 carousel → daily dry-run → `workflows.py` 긴급 재제안 → `reports.py` 읽기 전용 stage report의 별도 파이프라인이다. 실제 Meta publishing/OAuth/live 계정 연동은 구현하지 않았다. 각 단계와 테스트는 [증거 파이프라인 사례](case-studies/evidence-pipeline.md)에 적었다.

### 구분해 읽을 것

legacy Notion 자동화 계획은 API schema/dashboard를 수동으로 재구축하는 계열이고, Obsidian은 템플릿·대시보드 골격일 뿐 실행 코드가 아니다. AI briefing과 market briefing은 서로 다른 구성 범주이며, opportunity도 장학금·인턴·공모전·대외활동을 한 행으로 합치지 않는다. localStorage 완료 상태와 preferences/manifest도 별도 데이터 경계다. 저장된 wrapper/job 정의가 있어도 scheduler가 현재 성공적으로 실행된다는 뜻은 아니다.

### 비공개 원본 근거 파일명

조사 보고서에서 관찰한 비공개 원본 근거 파일명은 다음의 비배타적 subset이다: `telegram_capture.py`, `process_web_inbox.py`, `weekly_review.py`, `purge_trash.py`, `update_daily_dashboard.py`, `daily_opportunity_refresh.py`, `fetch_university_opportunities.py`, `competition_refresh.py`, `build_projects_manifest.py`, `add_schedule_event.py`, `normalize_competition_preferences.py`, `ai-reading-time-daily-dry-run.py`, `automation-evidence.md`, `second-brain-evidence.md`. 이 목록은 관찰된 일부이며 전체 파일 수를 세거나 완전한 inventory를 주장하지 않는다. 표에 별도로 인용한 비공개 Python 테스트 파일과 AI Reading Time 단계 모듈(`ingest.py`, `dedupe.py`, `rank.py`, `approvals.py`, `editorial.py`, `assets.py`, `renderer.py`, `workflows.py`, `reports.py`)도 공개 파일이 아니다. 공개 재현 파일은 별도로 `examples/*`와 `tests/*`에만 표시한다. 래퍼와 JavaScript 계약 파일명은 이 목록과 별도이며, 래퍼 구성명은 비공개로 남긴다.
