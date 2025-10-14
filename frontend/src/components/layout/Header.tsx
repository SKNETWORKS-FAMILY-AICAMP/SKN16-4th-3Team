import React from 'react';
import { Typography, Button, Space, Avatar, Dropdown } from 'antd';
import { UserAddOutlined, LoginOutlined, UserOutlined, LogoutOutlined, SettingOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import type { User } from '@/api/user';

const { Title } = Typography;

interface HeaderProps {
  isLoggedIn?: boolean;
  user?: User;
  onLogin?: () => void;
  onSignUp?: () => void;
  onLogout?: () => void;
  onMyPage?: () => void;
}

/**
 * 애플리케이션 헤더 컴포넌트
 * 로그인 상태에 따라 다른 UI를 보여줍니다
 */
export const Header: React.FC<HeaderProps> = ({
  isLoggedIn = false,
  user,
  onLogin,
  onSignUp,
  onLogout,
  onMyPage,
}) => {
  // 로그인된 사용자의 드롭다운 메뉴
  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '마이페이지',
      onClick: onMyPage,
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '설정',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '로그아웃',
      onClick: onLogout,
    },
  ];

  return (
    <header className="bg-white shadow-sm fixed top-0 left-0 right-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <Title level={3} className="gradient-text mb-0">
          퍼스널 컬러 진단 AI
        </Title>

        {isLoggedIn && user ? (
          // 로그인된 상태
          <div className="flex items-center gap-4">
            <span className="text-gray-600 hidden sm:inline">
              안녕하세요, <span className="font-bold text-gray-800">{user.nickname}</span>님
            </span>
            <Dropdown
              menu={{ items: userMenuItems }}
              placement="bottomRight"
              arrow
            >
              <div className="flex items-center gap-2 cursor-pointer hover:bg-gray-50 px-3 py-2 rounded-lg transition-colors">
                <Avatar
                  size="default"
                  icon={<UserOutlined />}
                  className="bg-blue-500"
                />
                <span className="hidden sm:inline text-gray-700">
                  {user.nickname}
                </span>
              </div>
            </Dropdown>
          </div>
        ) : (
          // 로그인되지 않은 상태
          <Space>
            <Button
              type="default"
              icon={<LoginOutlined />}
              onClick={onLogin}
            >
              로그인
            </Button>
            <Button
              type="primary"
              icon={<UserAddOutlined />}
              onClick={onSignUp}
            >
              회원가입
            </Button>
          </Space>
        )}
      </div>
    </header>
  );
};
