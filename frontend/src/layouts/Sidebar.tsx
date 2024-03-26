import styles from '../styles/Sidebar.module.css';

import { Fragment } from 'react/jsx-runtime';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useSideNavbar } from '../hooks/navigationHooks';
import { faBars, faX, faCartShopping, faCircleUser } from '@fortawesome/free-solid-svg-icons';

import NavItem from '../components/NavItem';
import LogoHeading from '../components/LogoHeading';

function Sidebar() {
	const { isOpen, toggleSideNavbar } = useSideNavbar();

	return (
		<Fragment>
			<div className={isOpen ? styles.sidebar : styles.sidebarOpen}>
				<nav className={styles.sidebarMenu}>
					<LogoHeading headingText="Primal Formulas" />
					<ul className={styles.navList}>
						<NavItem to="/about">Our Story</NavItem>
						<NavItem to="/shop">Products</NavItem>
						<NavItem to="/login">Account</NavItem>
					</ul>
					<ul className={styles.iconNav}>
						<NavItem to="/cart">
							<FontAwesomeIcon icon={faCartShopping} size="lg" />
						</NavItem>
						<NavItem to="/login">
							<FontAwesomeIcon icon={faCircleUser} size="xl" />
						</NavItem>
					</ul>
				</nav>
				{isOpen && (
					<div className={styles.sidebarIcon} onClick={toggleSideNavbar}>
						<FontAwesomeIcon icon={faX} className={styles.navigation} />
					</div>
				)}
			</div>
			{!isOpen && (
				<div className={styles.sidebarIcon} onClick={toggleSideNavbar}>
					<FontAwesomeIcon icon={faBars} className={styles.navigation} />
				</div>
			)}
		</Fragment>
	);
}

export default Sidebar;
