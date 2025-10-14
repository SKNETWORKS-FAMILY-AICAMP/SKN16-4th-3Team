import React from 'react';
import { ConfigProvider, theme, Typography, Button, Card, Row, Col, Space } from 'antd';
import { HeartOutlined } from '@ant-design/icons';
import { Header } from './components';
import './App.css';
import type { User } from './api/user';

const { Title, Paragraph } = Typography;

function App() {
  // TODO: API 연동 후 인증 상태를 전역으로 관리하도록 수정
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [user, setUser] = React.useState<User>();

  // 임시 로그인 함수 (실제로는 인증 API 호출)
  const handleLogin = () => {
    setIsLoggedIn(true);
    setUser({
      id: 1,
      nickname: '테스트유저',
      username: 'testuser',
      email: 'test@example.com',
      created_at: '2025-01-01',
      gender: '남성'
    });
  };

  // 로그아웃 함수
  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(undefined);
  };
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#1677ff',
          borderRadius: 6,
        },
      }}
    >
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        {/* Header */}
        <Header
          isLoggedIn={isLoggedIn}
          user={user}
          onLogin={handleLogin}
          onSignUp={() => console.log('회원가입 클릭')}
          onLogout={handleLogout}
          onMyPage={() => console.log('마이페이지 클릭')}
        />

        {/* Main Content */}
        <main className="max-w-6xl mx-auto px-4 py-12 mt-18">
          {/* Hero Section */}
          <div className="text-center mb-16">
            <Title level={1} className="gradient-text text-5xl mb-4">
              나만의 퍼스널 컬러를 찾아보세요
            </Title>
            <Paragraph className="text-xl !text-gray-600 mb-8 max-w-2xl mx-auto">
              간단한 질문에 답변하기만 하면 AI가 당신에게 가장 어울리는 퍼스널 컬러를 분석해드립니다.
              피부톤, 눈동자 색, 머리카락 색상에 대한 몇 가지 질문으로 정확한 진단을 받아보세요.
            </Paragraph>
            <Space size="large">
              <Button type="primary" size="large" className="px-8 py-6 h-auto">
                진단 시작하기
              </Button>
            </Space>
          </div>

          {/* Features Section */}
          <Row gutter={[32, 32]} className="mb-16">
            <Col xs={24} md={8}>
              <Card className="text-center h-full card-hover" variant={'outlined'}>
                <div className="text-4xl mb-4">📝</div>
                <Title level={4}>간편한 질문 방식</Title>
                <Paragraph className="!text-gray-600">
                  복잡한 사진 업로드 없이 간단한 텍스트 질문에만 답하면 됩니다.
                </Paragraph>
              </Card>
            </Col>
            <Col xs={24} md={8}>
              <Card className="text-center h-full card-hover" bordered={false}>
                <div className="text-4xl mb-4">⚡</div>
                <Title level={4}>빠른 진단</Title>
                <Paragraph className="text-gray-600">
                  몇 가지 질문에 답한 후 단 몇 분 만에 개인 맞춤형 퍼스널 컬러 결과를 확인할 수 있습니다.
                </Paragraph>
              </Card>
            </Col>
            <Col xs={24} md={8}>
              <Card className="text-center h-full card-hover" bordered={false}>
                <div className="text-4xl mb-4">🎨</div>
                <Title level={4}>정확한 AI 분석</Title>
                <Paragraph className="!text-gray-600">
                  피부톤, 눈동자, 머리카락 색상 정보를 바탕으로 AI가 정확한 퍼스널 컬러를 분석합니다.
                </Paragraph>
              </Card>
            </Col>
          </Row>

          {/* CTA Section */}
          <Card className="text-center !bg-gradient-to-r from-blue-500 to-purple-600 border-0">
            <div className="text-white">
              <Title level={2} className="!text-white mb-4">
                지금 바로 시작해보세요!
              </Title>
              <Paragraph className="!text-blue-100 text-lg mb-6">
                무료 회원가입 후 간단한 질문으로 나만의 퍼스널 컬러를 발견해보세요
              </Paragraph>
              <Button type="default" size="large" icon={<HeartOutlined />} className="px-8 py-6 h-auto">
                무료로 시작하기
              </Button>
            </div>
          </Card>
        </main>

        {/* Footer */}
        <footer className="bg-gray-800 !text-white py-8 mt-16">
          <div className="max-w-6xl mx-auto px-4 text-center">
            <Title level={4} className="!text-white mb-2">
              퍼스널 컬러 진단 AI
            </Title>
            <Paragraph className="!text-gray-400 mb-0">
              © 2025 Personal Color AI. All rights reserved.
            </Paragraph>
          </div>
        </footer>
      </div>
    </ConfigProvider>
  );
}

export default App;
