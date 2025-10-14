/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
    // Ant Design과의 호환성을 위한 설정
    corePlugins: {
        preflight: false, // Ant Design의 기본 스타일과 충돌 방지
    },
}