# 사례: 검증 gate와 보안 경계

2026-10-04 기준 원래 운영 배포 workflow는 현재도 `npm run verify || true`로 검증 실패를 무시하며, 이는 미해결 품질 위험이다. 이 공개본의 예제 CI만 실패를 전파하므로, build artifact가 만들어졌다는 사실과 test green을 혼동하지 않도록 구분했다. 별도로 과거 HMAC vault 설계와 현재 authorization boundary가 일치하지 않는 상태가 관찰됐다. 두 문제 모두 “코드가 있다”와 “안전하게 운영된다”를 분리해 기록해야 했다.

변경 방향은 공개 CI와 `verify` entry에서 bypass를 두지 않고, 실패한 subprocess의 exit code를 전파하는 것이다. release scanner는 Markdown 링크와 stable ID, 금지 파일명·secret·내부 경로 heuristic을 검사한다. 다만 scanner만으로 모든 secret을 보장한다고 말하지 않으며, 공개 전 별도의 secret scan과 독립 리뷰를 gate로 둔다; 그 절차는 이 저장소에서 재현되지 않는다.

인증 문제는 pattern-level로만 공개한다. 실제 route 목록, server origin, credential, exploit 단계는 제공하지 않는다. historical HMAC 구현이 있었다는 사실이 현재 private boundary가 보장된다는 뜻은 아니다.

검증 범위는 local temp fixture, SVG XML parse, CLI capture의 required `--root`, Node/Python 테스트다. live endpoint·OAuth·권한 probe는 실행하지 않았다. lesson은 품질 gate와 인증 boundary를 문서·코드·실행 결과로 각각 증명해야 한다는 것이다.
