import React from 'react';
import { Form, Input, Button, message, Row, Col, Card, Typography } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title } = Typography;

interface LoginFormValues {
    nickname: string;
    password: string;
}

const LoginForm: React.FC = () => {
    const navigate = useNavigate();
    const [form] = Form.useForm<LoginFormValues>();

    // 폼 제출 처리 (로그인 API 호출)
    const handleSubmit = async (values: LoginFormValues) => {
        try {
            console.log('로그인 데이터:', values);
            
            // TODO: 실제 로그인 API 호출
            // const response = await loginAPI(values);
            
            message.success('로그인 성공!');
            navigate('/'); // 메인 페이지로 이동
        } catch (error) {
            message.error('로그인에 실패했습니다. 닉네임과 비밀번호를 확인해주세요.');
        }
    };

    // 회원가입 페이지로 이동
    const handleSignupClick = () => {
        navigate('/signup');
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-4 mt-16">
            <Row justify="center" className="w-full max-w-6xl">
                <Col xs={24} sm={20} md={16} lg={12} xl={10}>
                    <Card className="shadow-xl border-0" style={{ borderRadius: '16px' }}>
                        <div className="text-center mb-8">
                            <Title level={2} className="gradient-text mb-2">
                                로그인
                            </Title>
                        </div>

                        {/* 로그인 폼 */}
                        <Form
                            form={form}
                            layout="vertical"
                            onFinish={handleSubmit}
                            size="large"
                        >
                            <Form.Item
                                label="닉네임"
                                name="nickname"
                                rules={[
                                    { required: true, message: '닉네임을 입력하세요' },
                                    { min: 2, max: 14, message: '닉네임은 2-14자 사이로 입력하세요' }
                                ]}
                            >
                                <Input
                                    prefix={<UserOutlined style={{ color: '#bfbfbf' }} />}
                                    placeholder="닉네임"
                                    className="h-12 rounded-lg"
                                />
                            </Form.Item>

                            <Form.Item
                                label="비밀번호"
                                name="password"
                                rules={[
                                    { required: true, message: '비밀번호를 입력하세요' }
                                ]}
                            >
                                <Input.Password
                                    prefix={<LockOutlined style={{ color: '#bfbfbf' }} />}
                                    placeholder="비밀번호"
                                    className="h-12 rounded-lg"
                                />
                            </Form.Item>

                            {/* 버튼 그룹 */}
                            <Form.Item className="mt-6 mb-0">
                                {/* LOGIN 버튼 */}
                                <Button
                                    type="primary"
                                    htmlType="submit"
                                    block
                                    size="large"
                                    className="h-12 rounded-lg text-base font-semibold mb-4 bg-gray-800 hover:bg-gray-700 border-gray-800"
                                >
                                    LOGIN
                                </Button>

                                {/* 회원가입 버튼 */}
                                <Button
                                    block
                                    size="large"
                                    onClick={handleSignupClick}
                                    className="h-11 rounded-lg text-sm text-gray-600 border-gray-300 hover:border-gray-400 hover:text-gray-700"
                                >
                                    회원가입
                                </Button>
                            </Form.Item>
                        </Form>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default LoginForm;
