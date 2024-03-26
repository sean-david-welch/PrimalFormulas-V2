import utils from '../styles/Utils.module.css';

import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRightFromBracket } from '@fortawesome/free-solid-svg-icons';

const ErrorPage: React.FC = () => {
	return (
		<div className={utils.error}>
			<h1 className={utils.sectionHeading}>An Error Occurred:</h1>
			<Link to={'/'}>
				<button className={utils.btn}>
					Go Back <FontAwesomeIcon icon={faRightFromBracket} />
				</button>
			</Link>
		</div>
	);
};

export default ErrorPage;
