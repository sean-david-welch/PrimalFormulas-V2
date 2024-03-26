import styles from '../styles/Footer.module.css';

import { faArrowUp } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const ToTopButton: React.FC = () => {
	const scrollToTop = () => {
		window.scrollTo({
			top: 0,
			behavior: 'smooth',
		});
	};
	return (
		<button id="toTopButton" aria-label="scroll-to-top-button" className={styles.toTopButton} onClick={scrollToTop}>
			<FontAwesomeIcon icon={faArrowUp} size="2x" />
		</button>
	);
};

export default ToTopButton;
