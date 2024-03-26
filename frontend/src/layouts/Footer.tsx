import styles from '../styles/Footer.module.css';

import { Link } from 'react-router-dom';
import { Asset } from '../types/assetTypes';
import { useGetResourceById } from '../hooks/dataHooks';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebook, faTwitter, faInstagram, faYoutube } from '@fortawesome/free-brands-svg-icons';

import Loading from './Loading';
import NavItem from '../components/NavItem';
import ToTopButton from '../components/ToTopButton';

function Footer() {
	const { data: logo, isLoading, isError, error } = useGetResourceById<Asset>('assets', 'logo');

	if (isLoading) return <Loading />;
	if (isError) return <div>Error: {error.message}</div>;

	return (
		<footer>
			<div className={styles.footerNavigation}>
				<ul className={styles.navList}>
					<NavItem to="/about">About</NavItem>
					<NavItem to="/shop">Products</NavItem>
					<NavItem to="/cart">Cart</NavItem>
					<NavItem to="/login">Login</NavItem>
				</ul>
			</div>
			<div className={styles.footerInformation}>
				<Link to="/">
					<img src={logo?.media} alt="Logo" id="logo" />
				</Link>
				<ul className={styles.addressList}>
					<li className={styles.addressItem}>Primal Formulas Ltd.</li>
					<li className={styles.addressItem}>Clonross, Drumree</li>
					<li className={styles.addressItem}>Co. Meath,</li>
					<li className={styles.addressItem}>A85 PK30</li>
					<li className={styles.addressItem}>Tel: 01 - 8259289</li>
					<li className={styles.addressItem}>Email: info@primalformulas.ie</li>
				</ul>
			</div>
			<div className={styles.socialLinks}>
				<Link to="#" target="_blank" className={styles.facebookSocials}>
					<FontAwesomeIcon icon={faFacebook} size="2xl" />
				</Link>
				<Link to="#" target="_blank" className={styles.twitterSocials}>
					<FontAwesomeIcon icon={faTwitter} size="2xl" />
				</Link>
				<Link to="#" target="_blank" className={styles.instagramSocials}>
					<FontAwesomeIcon icon={faInstagram} size="2xl" />
				</Link>
				<Link to="#" target="_blank" className={styles.youtubeSocials}>
					<FontAwesomeIcon icon={faYoutube} size="2xl" />
				</Link>
			</div>
			<ToTopButton />
		</footer>
	);
}

export default Footer;
