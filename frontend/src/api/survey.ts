import apiClient from './client';
import type { PersonalColorType } from '../types/personalColor';

/**
 * 퍼스널 컬러 테스트 관련 API 타입 정의
 */

export interface SurveyAnswer {
    question_id: number;
    option_id: string;
    option_label: string;
}

export interface SurveySubmitRequest {
    answers: SurveyAnswer[];
}

export interface SurveySubmitResponse {
    message: string;
    survey_result_id: number;
    result_tone: PersonalColorType;
    confidence: number;
    total_score: number;
}

export interface SurveyResultDetail {
    id: number;
    user_id: number;
    created_at: string;
    result_tone: PersonalColorType;
    confidence: number;
    total_score: number;
    answers: SurveyAnswer[];
}

/**
 * 설문 API 클래스
 */
class SurveyApi {
    /**
     * 퍼스널 컬러 테스트 결과 제출
     * PersonalColorTest 컴포넌트의 진단 결과를 백엔드로 전송
     */
    async submitSurvey(request: SurveySubmitRequest): Promise<SurveySubmitResponse> {
        console.log('📤 [SurveyApi] submitSurvey 요청:', request);
        const response = await apiClient.post<SurveySubmitResponse>(
            '/survey/submit',
            request
        );
        console.log('📥 [SurveyApi] submitSurvey 응답:', response.data);
        return response.data;
    }

    /**
     * 현재 사용자의 모든 설문 결과 조회 (최신순)
     */
    async getSurveyResults(): Promise<SurveyResultDetail[]> {
        const response = await apiClient.get<SurveyResultDetail[]>(
            '/survey/list'
        );
        return response.data;
    }

    /**
     * 특정 설문 결과 상세 조회
     */
    async getSurveyDetail(surveyId: number): Promise<SurveyResultDetail> {
        const response = await apiClient.get<SurveyResultDetail>(
            `/survey/${surveyId}`
        );
        return response.data;
    }

    /**
     * 설문 결과 삭제 (본인이 작성한 것만)
     */
    async deleteSurvey(surveyId: number): Promise<{ message: string }> {
        const response = await apiClient.delete<{ message: string }>(
            `/survey/${surveyId}`
        );
        return response.data;
    }
}

// API 인스턴스 생성
export const surveyApi = new SurveyApi();
