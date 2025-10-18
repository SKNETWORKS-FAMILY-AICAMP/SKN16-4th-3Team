import { useQuery } from '@tanstack/react-query';
import { surveyApi } from '@/api/survey';

/**
 * 사용자의 설문 결과 목록을 가져오는 hook
 */
export const useSurveyResults = () => {
  return useQuery({
    queryKey: ['surveyResults'],
    queryFn: () => surveyApi.getSurveyResults(),
    retry: 2,
    staleTime: 5 * 60 * 1000, // 5분
  });
};

/**
 * 특정 설문 결과 상세 정보를 가져오는 hook
 */
export const useSurveyDetail = (surveyId: number) => {
  return useQuery({
    queryKey: ['surveyDetail', surveyId],
    queryFn: () => surveyApi.getSurveyDetail(surveyId),
    enabled: !!surveyId,
    retry: 2,
    staleTime: 10 * 60 * 1000, // 10분
  });
};
