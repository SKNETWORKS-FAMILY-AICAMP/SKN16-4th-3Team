import { useState, useCallback } from 'react';
import type {
    PersonalColorQuestion,
    PersonalColorAnswer,
    PersonalColorResult,
    PersonalColorType,
    PersonalColorScores,
    TestProgress
} from '@/types/personalColor';
import { PERSONAL_COLOR_QUESTIONS, PERSONAL_COLOR_RESULTS } from '@/constants/personalColorQuestions';

interface UsePersonalColorTestReturn {
    // 상태
    currentQuestion: PersonalColorQuestion | null;
    progress: TestProgress;
    result: PersonalColorResult | null;

    // 액션
    selectAnswer: (optionId: string) => void;
    goToNextQuestion: () => void;
    goToPreviousQuestion: () => void;
    resetTest: () => void;
    calculateResult: () => PersonalColorResult;
}

export const usePersonalColorTest = (): UsePersonalColorTestReturn => {
    // 초기 상태 설정
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState<PersonalColorAnswer[]>([]);
    const [result, setResult] = useState<PersonalColorResult | null>(null);

    // 현재 질문 가져오기
    const currentQuestion = PERSONAL_COLOR_QUESTIONS[currentQuestionIndex] || null;

    // 진행 상태 계산
    const progress: TestProgress = {
        currentQuestion: currentQuestionIndex + 1,
        totalQuestions: PERSONAL_COLOR_QUESTIONS.length,
        answers,
        isCompleted: currentQuestionIndex >= PERSONAL_COLOR_QUESTIONS.length
    };

    // 답변 선택 함수
    const selectAnswer = useCallback((optionId: string) => {
        if (!currentQuestion) return;

        // 선택한 옵션 찾기
        const selectedOption = currentQuestion.options.find(option => option.id === optionId);
        if (!selectedOption) return;

        // 새로운 답변 객체 생성
        const newAnswer: PersonalColorAnswer = {
            questionId: currentQuestion.id,
            optionId: optionId,
            scores: selectedOption.scores
        };

        // 기존 답변 업데이트 또는 새로운 답변 추가
        setAnswers(prev => {
            const existingIndex = prev.findIndex(answer => answer.questionId === currentQuestion.id);
            if (existingIndex >= 0) {
                // 기존 답변 업데이트
                const updated = [...prev];
                updated[existingIndex] = newAnswer;
                return updated;
            } else {
                // 새로운 답변 추가
                return [...prev, newAnswer];
            }
        });
    }, [currentQuestion]);

    // 다음 질문으로 이동
    const goToNextQuestion = useCallback(() => {
        if (currentQuestionIndex < PERSONAL_COLOR_QUESTIONS.length - 1) {
            setCurrentQuestionIndex(prev => prev + 1);
        } else {
            // 마지막 질문이면 결과 계산
            const finalResult = calculateResult();
            setResult(finalResult);
            setCurrentQuestionIndex(prev => prev + 1); // 완료 상태로 변경
        }
    }, [currentQuestionIndex]);

    // 이전 질문으로 이동
    const goToPreviousQuestion = useCallback(() => {
        if (currentQuestionIndex > 0) {
            setCurrentQuestionIndex(prev => prev - 1);
            // 결과가 있다면 제거 (다시 질문 상태로)
            if (result) {
                setResult(null);
            }
        }
    }, [currentQuestionIndex, result]);

    // 결과 계산 함수
    const calculateResult = useCallback((): PersonalColorResult => {
        // 각 퍼스널컬러 타입별 총 점수 계산
        const totalScores: PersonalColorScores = {
            spring: 0,
            summer: 0,
            autumn: 0,
            winter: 0
        };

        // 모든 답변의 점수 합계
        answers.forEach(answer => {
            Object.entries(answer.scores).forEach(([type, score]) => {
                const colorType = type as keyof PersonalColorScores;
                totalScores[colorType] = (totalScores[colorType] || 0) + (score || 0);
            });
        });

        // 가장 높은 점수의 타입 찾기
        const maxScore = Math.max(...Object.values(totalScores));
        const resultType = (Object.entries(totalScores).find(
            ([, score]) => score === maxScore
        )?.[0] || 'spring') as PersonalColorType;

        // 신뢰도 계산 (최고점수 / 전체 점수의 비율)
        const totalAllScores = Object.values(totalScores).reduce((sum, score) => sum + score, 0);
        const confidence = totalAllScores > 0 ? Math.round((maxScore / totalAllScores) * 100) : 0;

        // 결과 객체 생성
        const baseResult = PERSONAL_COLOR_RESULTS[resultType];
        const finalResult: PersonalColorResult = {
            ...baseResult,
            scores: totalScores,
            confidence
        };

        return finalResult;
    }, [answers]);

    // 테스트 초기화
    const resetTest = useCallback(() => {
        setCurrentQuestionIndex(0);
        setAnswers([]);
        setResult(null);
    }, []);

    return {
        currentQuestion,
        progress,
        result,
        selectAnswer,
        goToNextQuestion,
        goToPreviousQuestion,
        resetTest,
        calculateResult
    };
};