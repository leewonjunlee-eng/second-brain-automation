# 사례: AI 읽을거리의 근거 파이프라인

## 배경

AI·개발 자료를 모아 읽고 공유하려는 흐름은 단순한 daily wrapper만으로는 부족했다. 후보를 수집한 뒤 이미 다룬 사건을 다시 추천하지 않고, 왜 이 주제를 선택했는지 추적하며, 승인된 근거만 editorial과 이미지에 연결해야 했다. 그래서 게시 전 준비 파이프라인을 별도 경계로 구현했다.

## 증상과 원인

초기 위험은 source collection, ranking, 승인, 렌더링, 보고가 서로 다른 상태를 볼 수 있다는 점이었다. evidence snapshot 저장 과정에서는 `evidence_snapshots`가 14개 열인데 13개 값만 전달되는 SQL 오류도 기록됐다. 이는 “대충 INSERT”한 경로와 schema의 결합이 만든 명시적 결함이었다.

## 변경

`ingest.py`가 RSS/GitHub release fixture를 안전하게 수집하고, `dedupe.py`가 canonical event를 결정적으로 묶는다. `rank.py`가 미게시 후보를 점수화하고, `approvals.py`가 actor/request ID·revision·stale version·idempotency를 검사한다. `editorial.py`는 승인된 source member만 EvidencePacket으로 만들고 claim을 evidence ID에 묶는다. `assets.py`는 MIME·크기·hash·경로 탈출·SSRF 경계를 확인하고, `renderer.py`는 canonical JSON과 local font로 결정적 carousel을 만든다. 이후 daily dry-run, `workflows.py`의 긴급/지연 후보 재제안, `reports.py`의 읽기 전용 stage report가 이어진다.

SQL 결함은 열 이름을 14개 모두 명시한 INSERT로 고쳤다. commit 실패 시 transaction rollback을 수행하고, replay fingerprint와 cross-cluster source ID가 섞이지 않는 회귀 경계를 추가했다.

2026-10-04 기준 이 구현과 테스트는 로컬 개발 브랜치에만 있으며 릴리스·배포되지 않았다.

## 확인과 한계

근거 파일은 `ingest.py`, `dedupe.py`, `rank.py`, `approvals.py`, `editorial.py`, `assets.py`, `renderer.py`, `workflows.py`, `reports.py`와 각각의 unit/integration test다. 공개본에 적은 상태는 private evidence report에서 확인한 구현·문서·테스트 범위다. 실제 Meta Graph API publisher, OAuth, live account, carousel publish는 구현되지 않았다. 따라서 결과는 “게시 전 안전한 준비·승인·dry-run·보고”이며 자동 게시가 아니다.
