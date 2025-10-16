import React from 'react';
import { Row, Col, Card, Typography, Button, Space, Avatar } from 'antd';
import { UserOutlined, EditOutlined, ManOutlined, WomanOutlined } from '@ant-design/icons';
import { useCurrentUser } from '@/hooks/useUser';
import { getGenderAvatarConfig } from '@/utils/genderUtils';

const { Title, Text } = Typography;

/**
 * 마이페이지 컴포넌트
 */
const MyPage: React.FC = () => {
    const { data: user, isLoading } = useCurrentUser();

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
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 pt-20 pb-8">
            <div className="max-w-4xl mx-auto px-4">
                <Title level={2} className="text-center mb-8">
                    마이페이지
                </Title>

                <Row gutter={[24, 24]}>
                    {/* 사용자 정보 카드 */}
                    <Col xs={24} md={12}>
                        <Card
                            title="프로필 정보"
                            className="shadow-lg border-0"
                            style={{ borderRadius: '16px' }}
                            extra={
                                <Button
                                    type="text"
                                    icon={<EditOutlined />}
                                    onClick={() => {
                                        // TODO: 프로필 수정 기능 구현
                                        console.log('프로필 수정 기능 구현 필요');
                                    }}
                                >
                                    수정
                                </Button>
                            }
                        >
                            <div className="text-center mb-6">
                                {(() => {
                                    const avatarConfig = getGenderAvatar();
                                    const config = getGenderAvatarConfig(user?.gender, user?.id);

                                    return (
                                        <Avatar
                                            size={80}
                                            className={`${avatarConfig.className} mb-4`}
                                            style={avatarConfig.style}
                                        >
                                            {config.avatarType === 'emoji' ? (
                                                <span style={{ fontSize: '40px' }}>{config.emoji}</span>
                                            ) : (
                                                avatarConfig.content
                                            )}
                                        </Avatar>
                                    );
                                })()}
                                <Title level={4} className="mb-0">
                                    {user.nickname}
                                </Title>
                                <Text type="secondary">@{user.username}</Text>
                            </div>

                            <Space direction="vertical" className="w-full" size="middle">
                                <div>
                                    <Text strong>이메일:</Text>
                                    <div>{user.email}</div>
                                </div>
                                {user.gender && (
                                    <div>
                                        <Text strong>성별:</Text>
                                        <div>{user.gender}</div>
                                    </div>
                                )}
                            </Space>
                        </Card>
                    </Col>

                    {/* 활동 정보 카드 */}
                    <Col xs={24} md={12}>
                        <Card
                            title="활동 정보"
                            className="shadow-lg border-0"
                            style={{ borderRadius: '16px' }}
                        >
                            <Space direction="vertical" className="w-full" size="middle">
                                <div>
                                    <Text strong>진단 기록:</Text>
                                    <div>0회</div>
                                </div>
                                <div>
                                    <Text strong>저장된 결과:</Text>
                                    <div>0개</div>
                                </div>
                                <div>
                                    <Text strong>가입일:</Text>
                                    <div>최근 가입</div>
                                </div>
                            </Space>

                            <div className="mt-6">
                                <Button type="primary" block>
                                    퍼스널 컬러 진단하기
                                </Button>
                            </div>
                        </Card>
                    </Col>
                </Row>

                {/* 추가 섹션들 */}
                <Row className="mt-8">
                    <Col span={24}>
                        <Card
                            title="최근 진단 결과"
                            className="shadow-lg border-0"
                            style={{ borderRadius: '16px' }}
                        >
                            <div className="text-center py-8">
                                <Text type="secondary">아직 진단 기록이 없습니다.</Text>
                                <div className="mt-4">
                                    <Button type="primary">첫 진단 시작하기</Button>
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