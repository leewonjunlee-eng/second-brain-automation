# 사례: 시간대 경계와 일정 산술

배경은 KST 기준 dashboard와 달력이다. 자정 전후 사용자가 보는 날짜가 한 칸 밀리거나, 브라우저 local timezone을 이미 KST로 바꾼 값에 다시 9시간 더하는 문제가 반복될 수 있었다. 저장소 이력과 날짜 유틸리티는 이 문제의 설계·수정 근거이지만 실제 HTTP 응답이나 배포 화면은 아니다.

원인은 날짜 표시와 날짜 산술의 책임이 섞인 데 있었다. 변경은 `Intl.DateTimeFormat(..., timeZone: 'Asia/Seoul')`로 표시용 날짜를 얻고, 주간 계산은 UTC date parts에서 수행하도록 나눴다. `date.js`는 일요일을 포함해 월요일 시작 주를 만들며 `schedule-utils.js`는 유효한 날짜·시간·범위만 통과시킨다.

공개 검증은 KST 자정 직전/직후, UTC와 `Asia/Seoul` 실행, 일요일 주간 crossing, 연말·윤년, 유효/무효 hour/day/range, occurrence의 범위 안팎을 구분한다. 예제는 개인 일정 없이 synthetic input만 사용한다.

capture 파일명과 `created` 날짜는 UTC 기준으로 생성하고, dashboard·일정 표시와 주간 산술은 `Asia/Seoul`(KST) 유틸리티를 사용한다. 두 기준은 의도적으로 같다고 가정하지 않는다.

한계는 시스템 시계·브라우저 렌더링·live timezone 설정을 보장하지 않는다는 점이다. 날짜 유틸리티 테스트 통과를 production SLA나 배포 성공으로 확대하지 않는다. 교훈은 “날짜를 문자열로 하드코딩하지 말고 표시 timezone과 산술 기준을 명시하라”이다.
