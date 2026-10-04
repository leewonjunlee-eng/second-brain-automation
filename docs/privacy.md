# 개인정보와 공개 경계

공개하지 않는 것: Inbox/Trash/Library/Review 원문, 개인 일정·선호·재무·연락처, token/password/HMAC/env, chat/user ID, private queue, origin/hostname, raw log, full cron prompt, 원본 Git history. 공개 예제는 synthetic technical text와 임시 디렉터리만 사용한다.

현재 보안 상태는 일반적인 제한으로만 기술한다. 역사적 HMAC 설계와 현재 authorization boundary가 다르며, 보안 보장은 주장하지 않는다. CI scanner는 heuristic이며 zero-secret 보장이 아니다. 공개 전 별도의 개인정보 scan과 독립 review가 필요하다.
