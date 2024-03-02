import styles from '../styles/Header.module.css';

import Header from './Header';
import Footer from './Footer';
import Sidebar from './Sidebar';

import { useLocation } from 'react-router-dom';

interface LayoutProps {
	children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
	const location = useLocation();

	const mainClass = location.pathname === '/' ? 'min-h-screen' : 'min-h-screen mt-32 mb-10';

	return (
		<div className="flex max-w-full flex-col overflow-x-hidden">
			<header className={styles.header}>
				<Header />
				<Sidebar />
			</header>
			<main className={mainClass}>{children}</main>
			<Footer />
		</div>
	);
};

export default Layout;
