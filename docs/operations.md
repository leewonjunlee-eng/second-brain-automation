# 운영 계약

- Git 작업은 `flock`식 직렬화 경계를 두며 공개 예제는 Git을 건드리지 않는다.
- `processed/filed/archived/trashed/done` 상태와 queue 소비는 재처리를 줄이지만, 순차 파일명 생성은 동시성 안전하지 않다.
- queue 파일 삭제는 `git rm`으로 push 전에 stage하고 로컬 commit하며, push 성공 때만 원격에 반영됩니다. push가 실패하면 로컬 commit/working tree는 남아 재조정이 필요하고 rollback은 입증하지 않았습니다. 외부 Issue 종료는 push 성공 뒤에만 수행합니다. 이 수선은 2026-10-04 기준 로컬 미커밋·미배포 상태이며 분산 원자성은 보장하지 않습니다.
- purge/review에는 변경 없는 점검 경로가 있지만 파괴적 단계는 공개 예제 밖이다.
- 무변경 작업의 전달 억제는 설계된 동작이며 성공률 지표가 아니다.
- reminder ledger와 automation log는 계획 상태이며 파일이 확인되지 않았다.

이 문서는 관찰된 패턴이지 production runbook이나 배포 승인서가 아니다.
