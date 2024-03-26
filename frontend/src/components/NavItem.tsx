import utils from '../styles/Utils.module.css';

import { Link } from 'react-router-dom';
import { NavItemProps } from '../types/miscTypes';

function NavItem({ to, children }: NavItemProps) {
	return (
		<li className={utils.navItem}>
			<Link className={utils.navLink} to={to}>
				{children}
			</Link>
		</li>
	);
}

export default NavItem;
