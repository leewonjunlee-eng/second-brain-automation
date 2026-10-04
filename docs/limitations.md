# 현재 한계

- live Pages/Telegram Gateway/Quartz 배포를 검증하지 않았다.
- scheduler enabled metadata와 현재 실행 성공은 다르다.
- 순차 파일명 고유성은 concurrent-safe하지 않다.
- capture serializer는 제한된 YAML 출력기이며 일반 untrusted YAML parser가 아니다.
- localStorage checkbox는 브라우저별 상태다.
- Git transaction fail-closed 수선은 2026-10-04 기준 로컬 미커밋·미배포 상태이며 분산 원자성을 보장하지 않는다.
- 배포 verify bypass 위험은 미해결이다.
- opportunity source 사실과 개인 preference/auth는 분리해야 한다.
- scanner는 heuristic이고 별도의 전체 scan/review를 대체하지 않는다.
- AI 읽을거리 파이프라인은 게시 전 준비 단계이며 Meta publisher/OAuth/live 게시가 없다.
