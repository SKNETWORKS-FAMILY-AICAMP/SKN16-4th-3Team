import type { PersonalColorQuestion, PersonalColorResult } from '@/types/personalColor';

export const PERSONAL_COLOR_QUESTIONS: PersonalColorQuestion[] = [
    // {
    //     id: 1,
    //     category: "목적",
    //     question: "퍼스널 컬러 결과로 어떤 도움을 받고 싶으신가요?",
    //     options: [
    //         {
    //             id: "opt_makeup",
    //             label: "메이크업 추천",
    //             scores: { spring: 0, summer: 0, autumn: 0, winter: 0 }
    //         },
    //         {
    //             id: "opt_clothes",
    //             label: "의상 컬러 추천",
    //             scores: { spring: 0, summer: 0, autumn: 0, winter: 0 }
    //         },
    //         {
    //             id: "opt_products",
    //             label: "제품 추천(파운데이션/립 등)",
    //             scores: { spring: 0, summer: 0, autumn: 0, winter: 0 }
    //         }
    //     ]
    // },
    {
        id: 2,
        category: "피부톤",
        question: "자연광에서 피부 색이 더 노란빛(웜) 같나요, 푸른빛(쿨) 같나요, 아니면 잘 모르겠나요?",
        options: [
            {
                id: "opt_warm",
                label: "노란빛",
                scores: { spring: 2, summer: 0, autumn: 2, winter: 0 }
            },
            {
                id: "opt_cool",
                label: "푸른빛",
                scores: { spring: 0, summer: 2, autumn: 0, winter: 2 }
            },
            {
                id: "opt_unsure",
                label: "잘 모르겠음",
                scores: { spring: 0, summer: 0, autumn: 0, winter: 0 }
            }
        ]
    },
    {
        id: 3,
        category: "혈관",
        question: "손목 정맥색은 어떤 쪽으로 보이나요?",
        options: [
            {
                id: "opt_vein_green",
                label: "녹색빛",
                scores: { spring: 1, summer: 0, autumn: 1, winter: 0 }
            },
            {
                id: "opt_vein_blue",
                label: "푸른빛",
                scores: { spring: 0, summer: 1, autumn: 0, winter: 1 }
            },
            {
                id: "opt_vein_unsure",
                label: "잘 모르겠음",
                scores: { spring: 0, summer: 0, autumn: 0, winter: 0 }
            }
        ]
    },
    {
        id: 4,
        category: "머리카락",
        question: "머리카락(자연 상태)은 밝은 편인가요, 어두운 편인가요, 염색 중인가요?",
        options: [
            {
                id: "opt_hair_light",
                label: "밝음(금빛/밝은 갈색)",
                scores: { spring: 2, summer: 1, autumn: 1, winter: 0 }
            },
            {
                id: "opt_hair_dark",
                label: "어두움(검정/진한 갈색)",
                scores: { spring: 0, summer: 1, autumn: 2, winter: 2 }
            },
            {
                id: "opt_hair_dyed",
                label: "염색 중",
                scores: { spring: 1, summer: 1, autumn: 1, winter: 1 }
            }
        ]
    },
    {
        id: 5,
        category: "눈동자",
        question: "눈동자 색은 상대적으로 밝은가요, 진한가요?",
        options: [
            {
                id: "opt_eye_light",
                label: "밝음(연한 갈색/녹색 등)",
                scores: { spring: 2, summer: 1, autumn: 1, winter: 0 }
            },
            {
                id: "opt_eye_dark",
                label: "진함(검정/진한 갈색)",
                scores: { spring: 0, summer: 1, autumn: 2, winter: 2 }
            }
        ]
    },
    {
        id: 6,
        category: "액세서리",
        question: "액세서리로 더 잘 어울리는 건 골드인가요, 실버인가요, 둘 다인가요?",
        options: [
            {
                id: "opt_metal_gold",
                label: "골드",
                scores: { spring: 2, summer: 0, autumn: 2, winter: 0 }
            },
            {
                id: "opt_metal_silver",
                label: "실버",
                scores: { spring: 0, summer: 2, autumn: 0, winter: 2 }
            },
            {
                id: "opt_metal_both",
                label: "둘 다",
                scores: { spring: 1, summer: 1, autumn: 1, winter: 1 }
            }
        ]
    },
    {
        id: 7,
        category: "화이트 톤",
        question: "햇빛 아래에서 흰색(퓨어 화이트)과 아이보리(아이보리/크림) 중 어떤 색이 얼굴을 더 밝게 보이게 하나요?",
        options: [
            {
                id: "opt_white",
                label: "퓨어 화이트(흰색)",
                scores: { spring: 0, summer: 2, autumn: 0, winter: 2 }
            },
            {
                id: "opt_ivory",
                label: "아이보리/크림",
                scores: { spring: 2, summer: 0, autumn: 2, winter: 0 }
            },
            {
                id: "opt_white_unsure",
                label: "잘 모르겠음",
                scores: { spring: 0, summer: 0, autumn: 0, winter: 0 }
            }
        ]
    }
];

export const PERSONAL_COLOR_RESULTS: Record<string, PersonalColorResult> = {
    spring: {
        type: 'spring',
        scores: { spring: 0, summer: 0, autumn: 0, winter: 0 },
        confidence: 0,
        name: "봄 웜톤 (Spring Warm)",
        description: "밝고 화사한 당신은 생동감 넘치는 봄의 여신입니다!",
        characteristics: [
            "화사함, 발랄함이 특징적인 스타일",
            "따뜻하고 밝은 피부톤",
            "생기발랄하고 젊은 인상",
            "선명하고 화사한 색상이 잘 어울림"
        ],
        keyColors: ["코럴", "피치", "골든 옐로우", "터콰이즈", "라벤더"],
        recommendedMakeup: ["코럴 블러셔", "피치 립", "골든 아이섀도우", "브라운 마스카라"],
        avoidColors: ["네이비", "다크 그레이", "머스타드", "올리브 그린", "다크 퍼플"],
        styles: ["화사함", "발랄함", "생동감", "밝음", "따뜻함"],
        swatches: ["#FF6F61", "#FFD1B3", "#FFE5B4", "#98FB98", "#40E0D0", "#E6E6FA", "#FFFACD"],
        recommendations: {
            bestColors: ["코럴", "피치", "라이트 옐로우", "민트", "라임그린", "터콰이즈", "라벤더"],
            avoidColors: ["네이비", "다크 그레이", "머스타드", "올리브 그린", "다크 퍼플"],
            makeup: {
                foundation: "코럴 컬러, 피치 블러셔, 골든 아이섀도우",
                lipstick: ["코럴핑크", "피치", "살구색", "따뜻한 코럴"],
                eyeshadow: ["골든브라운", "피치", "코럴", "라이트 옐로우"]
            },
            fashion: {
                basic: ["아이보리", "밝은 베이지", "크림", "라이트 그레이"],
                accent: ["코럴", "피치", "라임그린", "터콰이즈"]
            }
        }
    },
    summer: {
        type: 'summer',
        scores: { spring: 0, summer: 0, autumn: 0, winter: 0 },
        confidence: 0,
        name: "여름 쿨톤 (Summer Cool)",
        description: "우아하고 부드러운 당신은 시원한 여름의 요정입니다!",
        characteristics: [
            "차분함, 세련됨이 특징적인 스타일",
            "시원하고 부드러운 피부톤",
            "우아하고 로맨틱한 인상",
            "부드럽고 차분한 색상이 잘 어울림"
        ],
        keyColors: ["로즈", "라벤더", "소프트 블루", "더스티핑크", "라이트 그레이"],
        recommendedMakeup: ["로즈 블러셔", "더스티핑크 립", "라벤더 아이섀도우", "브라운 마스카라"],
        avoidColors: ["머스타드", "올리브 그린", "오렌지", "브라운", "골드"],
        styles: ["차분함", "세련됨", "우아함", "로맨틱", "부드러움"],
        swatches: ["#F8BBD9", "#E6E6FA", "#ADD8E6", "#DDA0DD", "#D3D3D3", "#FFB6C1", "#B0E0E6"],
        recommendations: {
            bestColors: ["로즈", "라벤더", "소프트 블루", "딥 블루", "라이트 그레이", "소프트 퍼플"],
            avoidColors: ["머스타드", "올리브 그린", "오렌지", "브라운", "골드"],
            makeup: {
                foundation: "로즈핑크, 로즈 블러셔, 핑크 브라운 아이섀도우",
                lipstick: ["로즈핑크", "더스티핑크", "라벤더핑크", "소프트베리"],
                eyeshadow: ["소프트브라운", "라벤더", "핑크브라운", "라이트블루"]
            },
            fashion: {
                basic: ["네이비", "그레이", "화이트", "소프트베이지"],
                accent: ["라벤더", "로즈", "소프트블루", "라이트퍼플"]
            }
        }
    },
    autumn: {
        type: 'autumn',
        scores: { spring: 0, summer: 0, autumn: 0, winter: 0 },
        confidence: 0,
        name: "가을 웜톤 (Autumn Warm)",
        description: "깊고 풍성한 당신은 성숙한 가을의 여왕입니다!",
        characteristics: [
            "따뜻함, 성숙함이 특징적인 스타일",
            "황금빛 따뜻한 피부톤",
            "깊이 있고 성숙한 인상",
            "깊고 따뜻한 색상이 잘 어울림"
        ],
        keyColors: ["버건디", "카키", "골드", "딥 오렌지", "올리브 그린"],
        recommendedMakeup: ["오렌지 블러셔", "브릭레드 립", "골든브라운 아이섀도우", "브라운 마스카라"],
        avoidColors: ["블랙", "순백색", "네이비", "푸시아", "실버"],
        styles: ["따뜻함", "성숙함", "깊이", "풍성함", "고급스러움"],
        swatches: ["#800020", "#8B7355", "#FFD700", "#FF4500", "#556B2F", "#A0522D", "#CD853F"],
        recommendations: {
            bestColors: ["버건디", "카키", "골드", "딥 오렌지", "딥 브라운", "올리브 그린"],
            avoidColors: ["블랙", "순백색", "네이비", "푸시아", "실버"],
            makeup: {
                foundation: "골드 컬러, 오렌지 블러셔, 브라운 계열 아이섀도우",
                lipstick: ["브릭레드", "오렌지브라운", "딥코럴", "버건디"],
                eyeshadow: ["골든브라운", "딥오렌지", "카키", "브론즈"]
            },
            fashion: {
                basic: ["카멜", "딥브라운", "카키", "크림"],
                accent: ["버건디", "골드", "딥오렌지", "올리브그린"]
            }
        }
    },
    winter: {
        type: 'winter',
        scores: { spring: 0, summer: 0, autumn: 0, winter: 0 },
        confidence: 0,
        name: "겨울 쿨톤 (Winter Cool)",
        description: "강렬하고 명확한 당신은 차가운 겨울의 여신입니다!",
        characteristics: [
            "강렬함, 고급스러움이 특징적인 스타일",
            "시원하고 맑은 피부톤",
            "도시적이고 시크한 인상",
            "강렬하고 선명한 색상이 잘 어울림"
        ],
        keyColors: ["블랙", "퓨어 화이트", "로얄블루", "푸시아", "트루레드"],
        recommendedMakeup: ["푸시아 블러셔", "트루레드 립", "스모키 아이섀도우", "블랙 마스카라"],
        avoidColors: ["베이지", "머스타드", "옐로우", "카키", "오렌지"],
        styles: ["강렬함", "고급스러움", "시크함", "도시적", "명확함"],
        swatches: ["#000000", "#FFFFFF", "#4169E1", "#FF1493", "#DC143C", "#50C878", "#191970"],
        recommendations: {
            bestColors: ["블랙", "퓨어 화이트", "버건디", "아이비", "로얄블루", "푸시아"],
            avoidColors: ["베이지", "머스타드", "옐로우", "카키", "오렌지"],
            makeup: {
                foundation: "레드 컬러, 푸시아 블러셔, 스모키 아이섀도우",
                lipstick: ["트루레드", "딥베리", "푸시아", "와인레드"],
                eyeshadow: ["스모키그레이", "딥퍼플", "네이비", "실버"]
            },
            fashion: {
                basic: ["블랙", "퓨어 화이트", "네이비", "차콜 그레이"],
                accent: ["로얄 블루", "푸시아", "트루 레드", "에메랄드"]
            }
        }
    }
};