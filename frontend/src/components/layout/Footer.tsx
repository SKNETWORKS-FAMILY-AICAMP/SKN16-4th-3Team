import { Typography } from "antd"

const { Title, Paragraph } = Typography;

const Footer = () => {
    return <footer className="bg-gray-800 !text-white py-8 mt-16">
        <div className="max-w-6xl mx-auto px-4 text-center">
            <Title level={4} className="!text-white mb-2">
                퍼스널 컬러 진단 AI
            </Title>
            <Paragraph className="!text-gray-400 mb-0">
                © 2025 Personal Color AI. All rights reserved.
            </Paragraph>
        </div>
    </footer>
}

export default Footer;