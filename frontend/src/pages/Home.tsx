import React from 'react';
import { Typography, Button, Card, Row, Col, Space } from 'antd';
import { HeartOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

const HomePage: React.FC = () => {
  return (
    <main className="max-w-6xl mx-auto px-4 py-12 mt-18">
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
          <Card className="text-center h-full card-hover" variant={'outlined'}>
            <div className="text-4xl mb-4">⚡</div>
            <Title level={4}>빠른 진단</Title>
            <Paragraph className="text-gray-600">
              몇 가지 질문에 답한 후 단 몇 분 만에 개인 맞춤형 퍼스널 컬러 결과를 확인할 수 있습니다.
            </Paragraph>
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card className="text-center h-full card-hover" variant={'outlined'}>
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
  );
};

export default HomePage;