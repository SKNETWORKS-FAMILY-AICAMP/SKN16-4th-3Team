# 팀 개발을 위한 추가 권장사항

## 📋 체크리스트

### 신규 팀원 온보딩
- [ ] Node.js 18+ 설치 확인
- [ ] VS Code 설치 및 권장 확장 프로그램 설치
- [ ] `npm install` 실행
- [ ] `.env.example`을 복사하여 `.env` 파일 생성
- [ ] `npm run dev` 실행하여 개발 서버 정상 작동 확인
- [ ] 테스트 커밋으로 pre-commit 훅 작동 확인

### 코드 리뷰 가이드라인
- PR 생성 시 lint 및 format 검사 통과 확인
- 컴포넌트는 단일 책임 원칙 준수
- 타입 정의 명확히 작성
- 의미있는 커밋 메시지 작성

### 성능 최적화 팁
- React.memo, useMemo, useCallback 적절히 활용
- 번들 크기 최적화를 위한 lazy loading 고려
- 이미지 최적화 및 압축

## 🔗 유용한 링크
- [React 공식 문서](https://react.dev/)
- [TypeScript 공식 문서](https://www.typescriptlang.org/)
- [Vite 공식 문서](https://vitejs.dev/)
- [ESLint 규칙](https://eslint.org/docs/rules/)
- [Prettier 설정](https://prettier.io/docs/en/configuration.html)