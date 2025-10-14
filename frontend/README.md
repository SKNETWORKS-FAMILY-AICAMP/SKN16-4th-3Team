# Frontend - Team Development Setup

이 프로젝트는 React + TypeScript + Vite를 기반으로 개발합니다.

## 🚀 시작하기

### 필수 요구사항
- Node.js 18+
- npm 또는 yarn

### 설치 및 실행
```bash
# 의존성 설치
npm install

# 환경변수 설정
cp .env.example .env

# 개발 서버 실행
npm run dev
```

## 🛠️ 개발 도구

### 코드 품질 관리
- **ESLint**: 코드 문법 검사 및 품질 관리
- **Prettier**: 일관된 코드 포맷팅
- **Husky**: Git hooks를 통한 자동 검사
- **lint-staged**: 커밋 전 staged 파일만 검사

### 사용 가능한 스크립트
```bash
npm run dev          # 개발 서버 실행
npm run build        # 프로덕션 빌드
npm run lint         # ESLint 검사
npm run lint:fix     # ESLint 자동 수정
npm run format       # Prettier 포맷팅
npm run format:check # Prettier 검사
npm run type-check   # TypeScript 타입 검사
```

## 📁 프로젝트 구조
```
src/
├── components/      # 재사용 가능한 컴포넌트
├── pages/          # 페이지 컴포넌트
├── hooks/          # 커스텀 훅
├── utils/          # 유틸리티 함수
├── types/          # TypeScript 타입 정의
├── api/            # API 관련 코드
└── assets/         # 정적 리소스
```

## 🎨 코딩 컨벤션

### 네이밍 규칙
- **컴포넌트**: PascalCase (예: `UserProfile.tsx`)
- **파일/폴더**: kebab-case (예: `user-profile/`)
- **변수/함수**: camelCase (예: `getUserData`)
- **상수**: UPPER_SNAKE_CASE (예: `API_BASE_URL`)

### Git 컨벤션
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅, 세미콜론 누락 등
refactor: 코드 리팩토링
test: 테스트 코드 추가/수정
chore: 빌드 업무 수정, 패키지 매니저 수정
```

## 🔧 팀원 설정 가이드

### VS Code 설정
1. 권장 확장 프로그램 자동 설치 알림이 나타나면 모두 설치
2. 저장 시 자동 포맷팅이 적용됨
3. ESLint 오류가 실시간으로 표시됨

### 첫 커밋 전 확인사항
- Husky가 설치되어 pre-commit 훅이 작동하는지 확인
- 코드 포맷팅과 린팅이 자동으로 실행되는지 확인

## 🎨 UI 라이브러리 및 스타일링

### Ant Design
- **버전**: 최신 버전 사용
- **테마 커스터마이징**: `ConfigProvider`로 글로벌 테마 설정
- **아이콘**: `@ant-design/icons` 패키지 사용

### Tailwind CSS
- **버전**: v4 사용 (`@import "tailwindcss"`)
- **커스텀 유틸리티**: `src/utils/cn.ts`에서 조건부 클래스 관리
- **Ant Design 호환**: `preflight: false`로 충돌 방지

### 스타일링 가이드라인
```tsx
import { cn } from '@/utils/cn';

// 조건부 클래스 적용
<div className={cn(
  'base-class',
  isActive && 'active-class',
  { 'error-class': hasError }
)} />

// Ant Design + Tailwind 조합
<Button 
  type="primary" 
  className="w-full hover:shadow-lg transition-shadow"
>
  버튼
</Button>
```

### 색상 팔레트
- **Primary**: `#1677ff` (Ant Design 기본)
- **Gradient**: Blue to Purple (`#2563eb` → `#7c3aed`)
- **Gray Scale**: Tailwind 기본 색상 시스템 사용

## 📦 추가 패키지

### 유틸리티
- **clsx**: 조건부 클래스 이름 처리
- **@tailwindcss/typography**: 타이포그래피 플러그인

### 개발 도구
- **@tailwindcss/postcss**: PostCSS 통합
- **autoprefixer**: CSS 벤더 프리픽스 자동 추가

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
