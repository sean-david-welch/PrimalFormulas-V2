import utils from '../styles/Utils.module.css';

import NavButton from './NavButton';
import { Fragment } from 'react/jsx-runtime';
import { SectionHeadingProps } from '../types/miscTypes';

const SectionHeading: React.FC<SectionHeadingProps> = ({
	headingText,
	buttonLabel,
	buttonUrl,
	buttonIcon,
	onClick,
}) => {
	return (
		<Fragment>
			<h2 className={utils.sectionHeading}>{headingText}</h2>
			<ul className={utils.navList}>
				<NavButton onClick={onClick} to={buttonUrl} icon={buttonIcon} label={buttonLabel} />
			</ul>
		</Fragment>
	);
};

export default SectionHeading;
