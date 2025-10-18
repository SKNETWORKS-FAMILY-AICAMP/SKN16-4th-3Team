// 퍼스널컬러 타입 정의

export type PersonalColorType = 'spring' | 'summer' | 'autumn' | 'winter';

export interface PersonalColorQuestion {
    id: number;
    category: string;
    question: string;
    options: PersonalColorOption[];
}

export interface PersonalColorOption {
    id: string;
    label: string;
    scores: PersonalColorScores;
}

export interface PersonalColorScores {
    spring?: number;
    summer?: number;
    autumn?: number;
    winter?: number;
}

export interface PersonalColorAnswer {
    questionId: number;
    optionId: string;
    optionLabel: string;
    scores: PersonalColorScores;
}

export interface PersonalColorResult {
    type: PersonalColorType;
    scores: PersonalColorScores;
    confidence: number;
    description: string;
    characteristics: string[];
    recommendations: PersonalColorRecommendation;
    name: string;
    keyColors: string[];
    recommendedMakeup: string[];
    avoidColors: string[];
    styles: string[];
    swatches: string[];
}

export interface PersonalColorRecommendation {
    bestColors: string[];
    avoidColors: string[];
    makeup: {
        foundation: string;
        lipstick: string[];
        eyeshadow: string[];
    };
    fashion: {
        basic: string[];
        accent: string[];
    };
}

export interface TestProgress {
    currentQuestion: number;
    totalQuestions: number;
    answers: PersonalColorAnswer[];
    isCompleted: boolean;
}