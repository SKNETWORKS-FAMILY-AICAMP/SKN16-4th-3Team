import React from 'react';
import { Row, Col, Card, Typography, Button, Avatar, Modal, message } from 'antd';
import { UserOutlined, ManOutlined, WomanOutlined, DeleteOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useCurrentUser, useDeleteCurrentUser } from '@/hooks/useUser';
import { getGenderAvatarConfig } from '@/utils/genderUtils';
import RouterPaths from '@/routes/Router';

const { Title, Text } = Typography;

/**
 * 마이페이지 컴포넌트
 */
const MyPage: React.FC = () => {
    const { data: user, isLoading } = useCurrentUser();
    const navigate = useNavigate();
    const deleteCurrentUser = useDeleteCurrentUser();

    // 퍼스널 컬러 테스트로 이동
    const handleGoToTest = () => {
        navigate(RouterPaths.PersonalColorTest);
    };

    // 회원 탈퇴 확인 모달
    const handleDeleteAccount = () => {
        Modal.confirm({
            title: '비밀번호 확인',
            icon: <ExclamationCircleOutlined />,
            content: (
                <div className="mt-4">
                    <p className="mb-3">탈퇴하면 모든 데이터가 삭제되며 복구할 수 없습니다.</p>
                    <input
                        id="password-input"
                        type="password"
                        placeholder="비밀번호를 입력해주세요"
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                </div>
            ),
            okText: '탈퇴하기',
            okType: 'danger',
            cancelText: '취소',
            onOk() {
                const passwordInput = document.getElementById('password-input') as HTMLInputElement;
                const password = passwordInput?.value;

                if (!password) {
                    message.error('비밀번호를 입력해주세요.');
                    return Promise.reject();
                }

                return deleteCurrentUser.mutateAsync({ password })
                    .then(() => {
                        navigate(RouterPaths.Home);
                    })
                    .catch(() => {
                        return Promise.reject();
                    });
            },
        });
    };

    // 성별에 따른 아바타 렌더링
    const getGenderAvatar = () => {
        const config = getGenderAvatarConfig(user?.gender, user?.id);

        if (config.avatarType === 'emoji') {
            return {
                content: config.emoji,
                className: config.className,
                style: config.style
            };
        } else {
            // 기존 아이콘 방식 (fallback)
            let icon;
            switch (config.iconType) {
                case 'man':
                    icon = <ManOutlined />;
                    break;
                case 'woman':
                    icon = <WomanOutlined />;
                    break;
                default:
                    icon = <UserOutlined />;
                    break;
            }
            return {
                content: icon,
                className: config.className,
                style: config.style
            };
        }
    };

    if (isLoading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center pt-20">
                <div>로딩 중...</div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center pt-20">
                <Card className="shadow-xl border-0" style={{ borderRadius: '16px' }}>
                    <div className="text-center p-8">
                        <Title level={3}>로그인이 필요합니다</Title>
                        <Text>마이페이지를 보려면 로그인해주세요.</Text>
                    </div>
                </Card>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 pt-20 pb-8 mt-4">
            <div className="max-w-6xl mx-auto px-4">
                <Title level={2} className="mb-8 text-gray-800">
                    마이페이지
                </Title>

                <Row gutter={[32, 32]}>
                    {/* 왼쪽 박스 - 프로필 정보 */}
                    <Col xs={24} lg={10}>
                        <Card
                            className="shadow-sm border border-gray-200"
                            style={{ borderRadius: '8px' }}
                        >
                            {/* 아바타, 닉네임, 이름 센터 배치 */}
                            <div className="flex flex-col items-center justify-center py-2 border-b border-gray-100">
                                {(() => {
                                    const avatarConfig = getGenderAvatar();
                                    const config = getGenderAvatarConfig(user?.gender, user?.id);

                                    return (
                                        <Avatar
                                            size={100}
                                            className={`${avatarConfig.className} mb-4`}
                                            style={avatarConfig.style}
                                        >
                                            {config.avatarType === 'emoji' ? (
                                                <span style={{ fontSize: '50px' }}>{config.emoji}</span>
                                            ) : (
                                                avatarConfig.content
                                            )}
                                        </Avatar>
                                    );
                                })()}
                                <Title level={3} className="mb-2 text-gray-800 text-center">
                                    {user.nickname}
                                </Title>
                                <Text className="text-gray-500 text-lg text-center">
                                    {user.username}
                                </Text>
                            </div>

                            {/* 진단 기록, 저장된 결과 데이터 */}
                            {/* TODO: survey api 개발 후 연동 */}
                            <div className="p-2">
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-blue-600 mb-1">0</div>
                                        <Text className="text-gray-600">진단 기록</Text>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-green-600 mb-1">0</div>
                                        <Text className="text-gray-600">저장된 결과</Text>
                                    </div>
                                </div>
                            </div>
                        </Card>
                    </Col>

                    {/* 오른쪽 박스 - 상세 정보 */}
                    <Col xs={24} lg={14}>
                        <Card
                            className="shadow-sm border border-gray-200"
                            style={{ borderRadius: '8px' }}
                        >
                            <div className="px-6 py-2">
                                <Title level={4} className="mb-6 text-gray-800">상세 정보</Title>

                                <div className="grid grid-cols-2 gap-6">
                                    {/* 첫 번째 행 */}
                                    <div className="flex flex-col py-3 border-b border-gray-100">
                                        <Text strong className="text-gray-700 mb-2">이메일</Text>
                                        <Text className="text-gray-900">{user.email}</Text>
                                    </div>

                                    <div className="flex flex-col py-3 border-b border-gray-100">
                                        <Text strong className="text-gray-700 mb-2">성별</Text>
                                        <Text className="text-gray-900">{user.gender || '미설정'}</Text>
                                    </div>

                                    {/* 두 번째 행 */}
                                    <div className="flex flex-col py-3">
                                        <Text strong className="text-gray-700 mb-2">가입일</Text>
                                        <Text className="text-gray-900">
                                            {user.create_date ? new Date(user.create_date).toLocaleDateString('ko-KR') : '정보 없음'}
                                        </Text>
                                    </div>

                                    <div className="flex flex-col py-3">
                                        <Text strong className="text-gray-700 mb-2">계정 상태</Text>
                                        <div className="flex items-center">
                                            <div className={`w-2 h-2 rounded-full mr-2 ${user.is_active ? 'bg-green-500' : 'bg-red-500'}`}></div>
                                            <Text className={user.is_active ? 'text-green-600' : 'text-red-600'}>
                                                {user.is_active ? '활성' : '탈퇴'}
                                            </Text>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Card>
                    </Col>
                </Row>

                {/* 최근 진단 기록 섹션 */}
                <Row className="mt-8">
                    <Col span={24}>
                        <Card
                            className="shadow-sm border border-gray-200"
                            style={{ borderRadius: '8px' }}
                        >
                            <div className="px-6 py-2">
                                <Title level={4} className="mb-6 text-gray-800">최근 진단 기록</Title>
                                <div className="text-center py-12 bg-gray-50 rounded-lg">
                                    <Text className="text-gray-500 text-base">아직 진단 기록이 없습니다.</Text>
                                    <div className="mt-4">
                                        <Button type="primary" size="large" onClick={handleGoToTest}>
                                            첫 진단 시작하기
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </Card>
                    </Col>
                </Row>

                {/* 계정 관리 섹션 */}
                <Row className="mt-8">
                    <Col span={24}>
                        <Card
                            className="shadow-sm border border-red-200"
                            style={{ borderRadius: '8px' }}
                        >
                            <div className="px-6 py-2">
                                <Title level={4} className="mb-4 text-red-600">계정 관리</Title>
                                <div className="bg-red-50 p-4 rounded-lg border border-red-200">
                                    <div className="flex justify-between items-center">
                                        <div>
                                            <Text strong className="text-red-700">회원 탈퇴</Text>
                                            <div className="mt-1">
                                                <Text className="text-red-600 text-sm">
                                                    탈퇴 시 모든 개인정보와 진단 기록이 영구적으로 삭제됩니다.
                                                </Text>
                                            </div>
                                        </div>
                                        <Button
                                            danger
                                            icon={<DeleteOutlined />}
                                            onClick={handleDeleteAccount}
                                        >
                                            회원 탈퇴
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </Card>
                    </Col>
                </Row>
            </div>
        </div>
    );
};

export default MyPage;