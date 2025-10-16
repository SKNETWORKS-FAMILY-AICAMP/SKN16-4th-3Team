import React, { useEffect } from 'react';
import {
    Card,
    Button,
    Progress,
    Typography,
    Space,
    Tag,
    Alert
} from 'antd';
import {
    ArrowLeftOutlined,
    ArrowRightOutlined,
    ReloadOutlined,
    CheckCircleOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { usePersonalColorTest } from '@/hooks/usePersonalColorTest';
import { useCurrentUser } from '@/hooks/useUser';
import RouterPaths from '@/routes/Router';
import type { PersonalColorType } from '@/types/personalColor';

const { Title, Text } = Typography;

const PersonalColorTest: React.FC = () => {
    const navigate = useNavigate();
    const { data: user, isLoading: userLoading } = useCurrentUser();
    const {
        currentQuestion,
        progress,
        result,
        selectAnswer,
        goToNextQuestion,
        goToPreviousQuestion,
        resetTest
    } = usePersonalColorTest();

    const [selectedAnswer, setSelectedAnswer] = React.useState<string>('');

    // 질문이 변경될 때마다 화면을 최상단으로 스크롤
    useEffect(() => {
        if (currentQuestion) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }, [currentQuestion?.id]);

    // 결과가 나타날 때도 화면을 최상단으로 스크롤
    useEffect(() => {
        if (result) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }, [result]);

    // 답변 선택 핸들러
    const handleAnswerSelect = (optionId: string) => {
        setSelectedAnswer(optionId);
        selectAnswer(optionId);
    };

    // 다음 질문으로 이동
    const handleNext = () => {
        if (selectedAnswer) {
            goToNextQuestion();
            setSelectedAnswer(''); // 선택 초기화
        }
    };

    // 이전 질문으로 이동
    const handlePrevious = () => {
        goToPreviousQuestion();
        setSelectedAnswer(''); // 선택 초기화
    };

    // 테스트 다시 하기
    const handleRestart = () => {
        resetTest();
        setSelectedAnswer('');
        // 화면을 최상단으로 스크롤
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // 홈으로 가기
    const handleGoHome = () => {
        navigate(RouterPaths.Home);
    };

    // 로그인 페이지로 이동
    const handleGoToLogin = () => {
        navigate(RouterPaths.Login);
    };

    // 퍼스널컬러 타입별 색상 매핑
    const getColorTypeStyle = (type: PersonalColorType) => {
        const colorMap = {
            spring: { background: 'linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%)', color: '#2d3436' },
            summer: { background: 'linear-gradient(135deg, #a8e6cf 0%, #dcedc8 100%)', color: '#2d3436' },
            autumn: { background: 'linear-gradient(135deg, #d4a574 0%, #8b4513 100%)', color: '#ffffff' },
            winter: { background: 'linear-gradient(135deg, #74b9ff 0%, #0984e3 100%)', color: '#ffffff' }
        };
        return colorMap[type];
    };

    // 로딩 중일 때
    if (userLoading) {
        return (
            <div
                className="min-h-screen flex items-center justify-center"
                style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                }}
            >
                <div className="w-full max-w-md mx-auto p-4">
                    <Card
                        className="shadow-2xl border-0 text-center"
                        style={{
                            borderRadius: '20px',
                            background: 'rgba(255, 255, 255, 0.95)',
                            backdropFilter: 'blur(10px)'
                        }}
                    >
                        <Alert
                            message="로딩 중..."
                            type="info"
                            showIcon
                            style={{
                                background: 'transparent',
                                border: 'none'
                            }}
                        />
                    </Card>
                </div>
            </div>
        );
    }

    // 로그인하지 않은 경우
    if (!user) {
        return (
            <div
                className="min-h-screen flex items-center justify-center"
                style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                }}
            >
                <div className="w-full max-w-md mx-auto p-4">
                    <Card
                        className="shadow-2xl border-0"
                        style={{
                            borderRadius: '20px',
                            background: 'rgba(255, 255, 255, 0.95)',
                            backdropFilter: 'blur(10px)'
                        }}
                    >
                        <div className="text-center p-6">
                            <Title level={3} className="mb-4 text-gray-800">
                                🔐 로그인이 필요합니다
                            </Title>
                            <Text className="text-gray-600 block mb-6">
                                퍼스널 컬러 테스트를 이용하려면 로그인해주세요.
                            </Text>
                            <div className="flex gap-3 justify-center">
                                <Button
                                    onClick={handleGoHome}
                                    size="large"
                                    style={{
                                        borderColor: '#d1d5db',
                                        color: '#6b7280',
                                        borderRadius: '10px'
                                    }}
                                >
                                    홈으로 가기
                                </Button>
                                <Button
                                    type="primary"
                                    onClick={handleGoToLogin}
                                    size="large"
                                    style={{
                                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                        border: 'none',
                                        borderRadius: '10px'
                                    }}
                                >
                                    로그인하기
                                </Button>
                            </div>
                        </div>
                    </Card>
                </div>
            </div>
        );
    }

    // 결과 화면
    if (result) {
        const typeStyle = getColorTypeStyle(result.type);

        return (
            <div
                className="min-h-screen pt-4"
                style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                }}
            >
                <div className="max-w-2xl mx-auto p-4">
                    <Card
                        className="shadow-2xl border-0 mb-6"
                        style={{
                            borderRadius: '20px',
                            background: 'rgba(255, 255, 255, 0.95)',
                            backdropFilter: 'blur(10px)'
                        }}
                    >
                        {/* 헤더 */}
                        <div className="text-center mb-4">
                            <div className="flex justify-center mb-3">
                                <CheckCircleOutlined
                                    className="text-4xl"
                                    style={{ color: '#10b981' }}
                                />
                            </div>
                            <Title level={3} className="mb-1 text-gray-800">
                                🎉 진단 완료!
                            </Title>
                            <Text className="text-gray-600 text-base">당신만의 특별한 컬러를 찾았습니다</Text>
                        </div>

                        {/* 결과 메인 카드 */}
                        <div
                            className="p-4 rounded-2xl mb-4 text-center"
                            style={{
                                background: typeStyle.background,
                                color: typeStyle.color,
                            }}
                        >
                            <Title level={3} style={{ color: typeStyle.color, margin: 0 }}>
                                {result.name}
                            </Title>
                            <Text style={{ color: typeStyle.color, fontSize: '14px', display: 'block', marginTop: '8px' }}>
                                {result.description}
                            </Text>
                            <div className="mt-2">
                                <Text style={{ color: typeStyle.color, fontSize: '12px' }}>
                                    신뢰도: <strong>{result.confidence}%</strong>
                                </Text>
                            </div>
                        </div>

                        {/* 컬러 팔레트 */}
                        <div className="mb-4">
                            <Text strong className="text-gray-700 block mb-2 text-sm">🎨 당신만의 컬러 팔레트</Text>
                            <div className="flex justify-center gap-2 mb-3">
                                {result.swatches.slice(0, 5).map((color, index) => (
                                    <div
                                        key={index}
                                        className="w-10 h-10 rounded-full border-2 border-white shadow-md"
                                        style={{ backgroundColor: color }}
                                        title={`${result.keyColors[index] || color}`}
                                    />
                                ))}
                            </div>
                        </div>

                        {/* 핵심 특징 */}
                        <div className="mb-4">
                            <Text strong className="text-gray-700 block mb-2 text-sm">✨ 당신의 스타일</Text>
                            <div className="flex flex-wrap justify-center gap-2">
                                {result.styles.map((style, index) => (
                                    <Tag
                                        key={index}
                                        className="px-3 py-1 text-xs border-0 rounded-full"
                                        style={{
                                            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                            color: 'white'
                                        }}
                                    >
                                        {style}
                                    </Tag>
                                ))}
                            </div>
                        </div>

                        {/* 추천 메이크업 */}
                        <div className="mb-6">
                            <Text strong className="text-gray-700 block mb-2 text-sm">💄 추천 메이크업</Text>
                            <div className="flex flex-wrap justify-center gap-2">
                                {result.recommendedMakeup.map((item, index) => (
                                    <Tag key={index} color="magenta" className="px-2 py-1 text-xs">
                                        {item}
                                    </Tag>
                                ))}
                            </div>
                        </div>

                        {/* 액션 버튼 */}
                        <div className="flex gap-4 justify-center">
                            <Button
                                size="large"
                                icon={<ReloadOutlined />}
                                onClick={handleRestart}
                                className="px-6"
                                style={{
                                    borderColor: '#d1d5db',
                                    color: '#6b7280',
                                    borderRadius: '10px'
                                }}
                            >
                                다시 테스트
                            </Button>
                            <Button
                                type="primary"
                                size="large"
                                onClick={handleGoHome}
                                className="px-8"
                                style={{
                                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                    border: 'none',
                                    borderRadius: '10px'
                                }}
                            >
                                홈으로 가기
                            </Button>
                        </div>
                    </Card>
                </div>
            </div>
        );
    }

    // 질문 진행 화면
    if (currentQuestion) {
        return (
            <div
                className="min-h-screen flex items-center justify-center"
                style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                }}
            >
                <div className="w-full max-w-md mx-auto p-4">
                    {/* 메인 카드 */}
                    <Card
                        className="shadow-2xl border-0"
                        style={{
                            borderRadius: '20px',
                            background: 'rgba(255, 255, 255, 0.95)',
                            backdropFilter: 'blur(10px)'
                        }}
                    >
                        {/* 헤더 */}
                        <div className="text-center mb-4">
                            <div className="flex items-center justify-center mb-3">
                                <div
                                    className="w-10 h-10 rounded-full flex items-center justify-center text-white text-lg font-bold"
                                    style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
                                >
                                    {progress.currentQuestion}
                                </div>
                            </div>

                            <Title level={4} className="mb-1 text-gray-800">
                                {currentQuestion.category}
                            </Title>

                            <Text className="text-gray-600 text-base">
                                {currentQuestion.question}
                            </Text>
                        </div>

                        {/* 진행도 바 */}
                        <div className="mb-6">
                            <div className="flex justify-between items-center mb-2">
                                <Text className="text-sm text-gray-500">진행률</Text>
                                <Text className="text-sm font-semibold text-gray-700">
                                    {Math.round((progress.currentQuestion / progress.totalQuestions) * 100)}%
                                </Text>
                            </div>
                            <Progress
                                percent={Math.round((progress.currentQuestion / progress.totalQuestions) * 100)}
                                strokeColor={{
                                    '0%': '#667eea',
                                    '100%': '#764ba2',
                                }}
                                trailColor="#f3f4f6"
                                showInfo={false}
                            />
                        </div>

                        {/* 선택지 */}
                        <div className="mb-8">
                            <Space direction="vertical" size="middle" className="w-full">
                                {currentQuestion.options.map((option) => (
                                    <div
                                        key={option.id}
                                        className={`
                      w-full p-4 border-2 rounded-xl cursor-pointer transition-all duration-200
                      ${selectedAnswer === option.id
                                                ? 'border-purple-400 bg-purple-50'
                                                : 'border-gray-200 hover:border-purple-300 hover:bg-gray-50'
                                            }
                    `}
                                        onClick={() => handleAnswerSelect(option.id)}
                                    >
                                        <div className="flex items-center">
                                            <div
                                                className={`
                          w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center
                          ${selectedAnswer === option.id
                                                        ? 'border-purple-500 bg-purple-500'
                                                        : 'border-gray-300'
                                                    }
                        `}
                                            >
                                                {selectedAnswer === option.id && (
                                                    <div className="w-2 h-2 rounded-full bg-white"></div>
                                                )}
                                            </div>
                                            <Text className="text-base text-gray-700">{option.label}</Text>
                                        </div>
                                    </div>
                                ))}
                            </Space>
                        </div>

                        {/* 네비게이션 버튼 */}
                        <div className="flex justify-between items-center">
                            <Button
                                icon={<ArrowLeftOutlined />}
                                onClick={handlePrevious}
                                disabled={progress.currentQuestion === 1}
                                size="large"
                                className="flex items-center"
                                style={{
                                    borderColor: '#d1d5db',
                                    color: progress.currentQuestion === 1 ? '#9ca3af' : '#6b7280'
                                }}
                            >
                                이전
                            </Button>

                            <Button
                                type="primary"
                                icon={<ArrowRightOutlined />}
                                onClick={handleNext}
                                disabled={!selectedAnswer}
                                size="large"
                                className="flex items-center px-8"
                                style={{
                                    background: selectedAnswer
                                        ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                                        : '#d1d5db',
                                    border: 'none',
                                    borderRadius: '10px'
                                }}
                            >
                                {progress.currentQuestion === progress.totalQuestions ? '결과 보기' : '다음'}
                            </Button>
                        </div>
                    </Card>
                </div>
            </div>
        );
    }

    // 로딩 또는 오류 상태
    return (
        <div
            className="min-h-screen flex items-center justify-center"
            style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            }}
        >
            <div className="w-full max-w-md mx-auto p-4">
                <Card
                    className="shadow-2xl border-0 text-center"
                    style={{
                        borderRadius: '20px',
                        background: 'rgba(255, 255, 255, 0.95)',
                        backdropFilter: 'blur(10px)'
                    }}
                >
                    <Alert
                        message="테스트를 불러오는 중입니다..."
                        type="info"
                        showIcon
                        style={{
                            background: 'transparent',
                            border: 'none'
                        }}
                    />
                </Card>
            </div>
        </div>
    );
};

export default PersonalColorTest;