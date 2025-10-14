import { clsx, type ClassValue } from 'clsx';

/**
 * 조건부 클래스 이름을 결합하는 유틸리티 함수
 * Tailwind CSS 클래스와 조건부 스타일링에 유용합니다.
 * 
 * @param inputs - 클래스 이름 문자열, 객체, 배열 등
 * @returns 결합된 클래스 이름 문자열
 * 
 * @example
 * cn('base-class', isActive && 'active-class', { 'error': hasError })
 * // => 'base-class active-class' (isActive가 true이고 hasError가 false인 경우)
 */
export function cn(...inputs: ClassValue[]) {
    return clsx(inputs);
}

/**
 * Ant Design과 Tailwind CSS를 함께 사용할 때 유용한 헬퍼 함수들
 */
export const styleUtils = {
    /**
     * 그라데이션 텍스트 스타일을 생성합니다
     */
    gradientText: (from: string, to: string) => ({
        background: `linear-gradient(135deg, ${from} 0%, ${to} 100%)`,
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
    }),

    /**
     * 부드러운 그림자 스타일을 생성합니다
     */
    softShadow: (opacity = 0.1) => ({
        boxShadow: `0 4px 6px -1px rgba(0, 0, 0, ${opacity}), 0 2px 4px -1px rgba(0, 0, 0, ${opacity * 0.6})`,
    }),

    /**
     * 호버 효과가 있는 카드 스타일을 생성합니다
     */
    hoverCard: {
        transition: 'all 0.3s ease',
        transform: 'translateY(0)',
        cursor: 'pointer',
        '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        },
    },
};