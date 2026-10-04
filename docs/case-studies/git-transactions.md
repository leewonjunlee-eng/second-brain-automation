# 사례: Git 동기화와 외부 상태의 경계

웹 queue와 Issue를 Inbox note로 바꾸는 작업은 여러 hourly/daily/weekly 작업이 같은 working tree를 만지는 환경에서 발생했다. 증상은 branch fast-forward 실패, stash/pull/apply 분기, push 실패 전에 queue나 Issue가 사라질 위험이었다. lock과 실패 경로를 같은 계약으로 다루지 않으면 입력을 잃을 수 있다.

queue 파일 삭제는 `git rm`으로 push 전에 stage하고 로컬 commit하며, push 성공 때만 원격에 반영됩니다. push가 실패하면 로컬 commit/working tree는 남아 재조정이 필요하고 rollback은 입증하지 않았습니다. 외부 Issue 종료는 push 성공 뒤에만 수행합니다. 이 수선은 2026-10-04 기준 로컬 미커밋·미배포 상태이며 분산 원자성은 보장하지 않습니다.

검증 범위는 pull 실패 시 source를 소비하지 않음, add/commit/push 실패 시 close하지 않음, push 뒤 여러 Issue를 계속 닫는 순서다. 공개 예제는 Git·네트워크를 호출하지 않고 임시 root에서 capture만 실행한다.

추가 한계도 있다. capture는 입력의 앞뒤 whitespace를 `.strip()`으로 제거하므로 “원문 보존”은 byte-for-byte 보존이 아니라 정규화된 본문 보존이다. 파일명·metadata 생성은 순차 실행 기준이며 동시성 안전한 queue가 아니다. 교훈은 내부 Git 단계와 외부 API 상태를 분리해 각각 재시도·관찰해야 한다는 것이다.
