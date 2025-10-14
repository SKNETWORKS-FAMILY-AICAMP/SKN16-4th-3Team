import React from 'react';
import { Typography, Card, Row, Col } from 'antd';

const { Title, Paragraph } = Typography;

const SignUpPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-4">
      <Row justify="center" className="w-full max-w-6xl">
        <Col xs={24} sm={20} md={16} lg={12} xl={10}>
          <Card className="shadow-xl border-0" style={{ borderRadius: '16px' }}>
            <div className="text-center mb-8">
              <Title level={2} className="gradient-text mb-2">
                회원가입
              </Title>
              <Paragraph className="text-gray-600 mb-0">
                퍼스널 컬러 진단 AI와 함께 시작하세요
              </Paragraph>
            </div>

            <div className="text-center">
              <p>회원가입 폼이 여기에 들어갑니다.</p>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default SignUpPage;