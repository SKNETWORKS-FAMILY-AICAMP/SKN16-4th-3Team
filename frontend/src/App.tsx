import { ConfigProvider, theme } from 'antd';
import './App.css';

function App() {
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
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          Home
        </div>
      </div>
    </ConfigProvider>
  );
}

export default App;
