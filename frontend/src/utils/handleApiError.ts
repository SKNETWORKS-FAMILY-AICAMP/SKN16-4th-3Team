import { AxiosError } from 'axios';

/**
 * API 에러에서 사용자에게 표시할 메시지를 추출합니다.
 * 
 * @param error - Axios 에러 객체 또는 일반 에러
 * @param defaultMessage - 에러 메시지를 추출할 수 없을 때 사용할 기본 메시지
 * @returns 사용자에게 표시할 에러 메시지
 */
export const getErrorMessage = (error: unknown, defaultMessage: string = '오류가 발생했습니다.'): string => {
    // Axios 에러인 경우
    if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as AxiosError<{ detail?: string }>;

        // 서버에서 보낸 detail 메시지가 있으면 사용 (문자열인 경우만)
        if (axiosError.response?.data?.detail
            && typeof axiosError.response.data.detail === 'string') {
            return axiosError.response.data.detail;
        }

        // HTTP 상태 코드에 따른 기본 메시지
        if (axiosError.response?.status) {
            switch (axiosError.response.status) {
                case 400:
                    return '잘못된 요청입니다.';
                case 401:
                    return '인증이 필요합니다.';
                case 403:
                    return '접근 권한이 없습니다.';
                case 404:
                    return '요청한 리소스를 찾을 수 없습니다.';
                case 409:
                    return '중복된 데이터입니다.';
                case 500:
                    return '서버 오류가 발생했습니다.';
                default:
                    return defaultMessage;
            }
        }
    }

    // 일반 Error 객체인 경우
    if (error instanceof Error) {
        return error.message || defaultMessage;
    }

    // 그 외의 경우 기본 메시지 반환
    return defaultMessage;
};

/**
 * API 에러를 콘솔에 로깅합니다.
 * 
 * @param context - 에러가 발생한 컨텍스트 (예: "사용자 생성")
 * @param error - 에러 객체
 */
export const logApiError = (context: string, error: unknown): void => {
    console.error(`[${context}] 에러 발생:`, error);

    if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as AxiosError;
        console.error('- 상태 코드:', axiosError.response?.status);
        console.error('- 응답 데이터:', axiosError.response?.data);
    }
};
