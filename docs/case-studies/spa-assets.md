# 사례: SPA 초기화와 정적 자산

Quartz SPA navigation에서는 문서 body의 script가 매번 재실행되지 않아 dashboard와 Kanban이 첫 진입 뒤 비어 보일 수 있었다. 별도로 source folder 대소문자와 Pages public lowercase path가 달라 asset 404가 될 수 있었고, 긴 inline script는 parse/load 오류의 원인이 됐다.

원인은 화면 HTML의 존재와 runtime 초기화를 같은 것으로 본 데 있었다. 변경은 공통 module을 주입하고 `nav` 이벤트에서 초기화하며, `data-*-bound` 같은 idempotent guard로 중복 listener와 중복 fetch를 막는 것이었다. project manifest를 list와 Kanban이 공유해 두 화면의 상태도 분리하지 않았다.

검증은 navigation hook, 한 번의 manifest fetch, 빈 column, narrow viewport overflow 계약을 확인한다. 공개본에는 순수 date/schedule 모듈만 남겼고, 실제 Pages origin이나 개인 asset 경로는 넣지 않았다.

browser replay, live 404, screenshot은 이 cycle에서 실행하지 않았다. 그러므로 “시각 회귀 없음”을 주장하지 않는다. lesson은 SPA에서는 첫 렌더보다 재진입 경로를 별도 계약으로 테스트해야 한다는 것이다.
