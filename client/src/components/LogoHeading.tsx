import { Link } from 'react-router-dom';
import { LogoHeadingProps } from '../types/miscTypes';
import { useGetResourceById } from '../hooks/dataHooks';
import { Asset } from '../types/assetTypes';

const LogoHeading: React.FC<LogoHeadingProps> = ({ headingText }) => {
	const { data: logo, isLoading, isError, error } = useGetResourceById<Asset>('assets', 'logo');

	if (isLoading) {
		return <div>Loading...</div>;
	}

	if (isError) {
		return <div>Error: {error.message}</div>;
	}

	return (
		<div className="logo-heading">
			<Link to="/" className="logo-link">
				<img src={logo?.media} id="logo" alt="Logo" className="logo-heading" />
			</Link>
			<h2 className="section-heading">{headingText}</h2>
		</div>
	);
};

export default LogoHeading;
