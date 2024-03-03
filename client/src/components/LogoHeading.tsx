import utils from '../styles/Utils.module.css';

import { Link } from 'react-router-dom';
import { Asset } from '../types/assetTypes';

import { LogoHeadingProps } from '../types/miscTypes';
import { useGetResourceById } from '../hooks/dataHooks';

const LogoHeading: React.FC<LogoHeadingProps> = ({ headingText }) => {
	const { data: logo, isLoading, isError, error } = useGetResourceById<Asset>('assets', 'logo');

	if (isLoading) {
		return <div>Loading...</div>;
	}

	if (isError) {
		return <div>Error: {error.message}</div>;
	}

	return (
		<div className={utils.logoHeading}>
			<Link to="/" className={utils.logoLink}>
				<img src={logo?.media} id="logo" alt="Logo" />
			</Link>
			<h2 className={utils.sectionHeading}>{headingText}</h2>
		</div>
	);
};

export default LogoHeading;
