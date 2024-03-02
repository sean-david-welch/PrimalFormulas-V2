import { useLocation } from 'react-router-dom';
import { UseSideNavbar } from '../types/miscTypes';

import { useState, useEffect } from 'react';

export const useSideNavbar = (): UseSideNavbar => {
	const [isOpen, setIsOpen] = useState<boolean>(false);

	const toggleSideNavbar = () => {
		setIsOpen(!isOpen);
	};

	return { isOpen, toggleSideNavbar };
};

export const useTransparentHeader = () => {
	const location = useLocation();
	const isHomePage = location.pathname === '/';
	const [isTransparent, setIsTransparent] = useState(isHomePage);

	useEffect(() => {
		const handleScroll = () => {
			if (isHomePage) {
				const heroImageHeight = 250;
				const showTransparent = window.scrollY < heroImageHeight;
				setIsTransparent(showTransparent);
			}
		};

		window.addEventListener('scroll', handleScroll);
		return () => window.removeEventListener('scroll', handleScroll);
	}, [isHomePage]);
	return isTransparent;
};
