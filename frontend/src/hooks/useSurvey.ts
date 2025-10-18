import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { surveyApi } from '@/api/survey';
import { message } from 'antd';

/**
 * 사용자의 설문 결과 목록을 가져오는 hook
 */
export const useSurveyResults = () => {
  return useQuery({
    queryKey: ['surveyResults'],
    queryFn: () => surveyApi.getSurveyResults(),
    retry: 2,
    staleTime: 1 * 60 * 1000, // 1분으로 단축하여 더 자주 새로고침
    refetchOnWindowFocus: true, // 윈도우 포커스 시 새로고침
    refetchOnMount: true, // 컴포넌트 마운트 시 새로고침
    refetchInterval: 2 * 60 * 1000, // 2분마다 자동 새로고침
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

/**
 * 설문 결과를 삭제하는 hook
 */
export const useDeleteSurvey = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (surveyId: number) => surveyApi.deleteSurvey(surveyId),
    onSuccess: (data) => {
      message.success(data.message || '진단 기록이 삭제되었습니다.');
      // 설문 결과 목록을 다시 불러옴
      queryClient.invalidateQueries({ queryKey: ['surveyResults'] });
    },
    onError: (error: any) => {
      const errorMessage = error.response?.data?.detail || error.message || '삭제 중 오류가 발생했습니다.';
      message.error(errorMessage);
    },
  });
};
