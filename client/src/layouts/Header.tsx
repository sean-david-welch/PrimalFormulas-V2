import Loading from './Loading';
import NavItem from '../components/NavItem';
import NavButton from '../components/NavButton';

import { Asset } from '../types/assetTypes';
import { Link } from 'react-router-dom';
import { useGetResourceById } from '../hooks/dataHooks';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useTransparentHeader } from '../hooks/navigationHooks';
import { faCartShopping, faCircleUser, faArrowRight } from '@fortawesome/free-solid-svg-icons';

function Navbar() {
	const isTransparent = useTransparentHeader();
	const { data: logo, isLoading, isError } = useGetResourceById<Asset>('assets', 'logo');

	if (isLoading) return <Loading />;

	if (isError) return <div>error...</div>;

	return logo ? (
		<nav id="navbar" className={isTransparent ? 'transparent' : ''}>
			<ul className="nav-list">
				<Link className="logo" to="/">
					<img src={logo?.media} className="logo" id="logo" alt="Logo" />
				</Link>
				<div className="nav-list-side">
					<ul className="nav-list">
						<NavButton to="/shop" icon={<FontAwesomeIcon icon={faArrowRight} />} label="Products" />
						<NavItem id="cart" aria-label="cart-nav" to="/cart">
							<FontAwesomeIcon icon={faCartShopping} size="xl" />
						</NavItem>
						<NavItem id="user" aria-label="user-nav" to="/login">
							<FontAwesomeIcon icon={faCircleUser} size="2xl" />
						</NavItem>
					</ul>
				</div>
			</ul>
		</nav>
	) : null;
}

export default Navbar;
