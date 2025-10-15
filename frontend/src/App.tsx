import React from 'react';
import { useNavigate, Routes, Route } from 'react-router-dom';
import { ConfigProvider, FloatButton } from 'antd';

import { HomePage, SignUpPage } from './pages';
import { Header, Footer } from './components';

import type { User } from './api/user';
import './App.css';

import RouterPaths from './routes/Router';

function App() {
  const navigation = useNavigate();

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

  // 회원가입 페이지로 이동
  const handleSignUp = () => {
    // React Router의 navigate를 사용하여 페이지 이동
    navigation(RouterPaths.SignUp);
  };

  // 마이페이지로 이동
  const handleMyPage = () => {
    // navigation(RouterPaths.MyPage);
    console.log('마이페이지 이동 - 구현 필요');
  };

  return (
    <ConfigProvider
      theme={{
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
          onSignUp={handleSignUp}
          onLogout={handleLogout}
          onMyPage={handleMyPage}
        />

        {/* Main Routes */}
        <Routes>
          <Route path={RouterPaths.Home} element={<HomePage />} />
          <Route path={RouterPaths.SignUp} element={<SignUpPage />} />
          {/* TODO: 추가 라우트들 */}
          {/* <Route path={RouterPaths.Login} element={<LoginPage />} /> */}
          {/* <Route path={RouterPaths.MyPage} element={<MyPage />} /> */}
        </Routes>

        {/* Footer */}
        <Footer />
        <FloatButton.BackTop type='primary' />
      </div>
    </ConfigProvider>
  );
}

export default App;
