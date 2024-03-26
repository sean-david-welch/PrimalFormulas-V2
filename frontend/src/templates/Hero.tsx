import NavButton from '../components/NavButton';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';
import Loading from '../layouts/Loading';
import { useGetResourceById } from '../hooks/dataHooks';
import { Asset } from '../types/assetTypes';
import ErrorPage from '../layouts/Error';

export const Hero = () => {
	const { data: hero, isLoading, isError } = useGetResourceById<Asset>('assets', 'hero');

	if (isLoading) return <Loading />;
	if (isError) return <ErrorPage />;

	return hero ? (
		<div className="hero">
			<div className="overlay" />
			<video src={hero.media} autoPlay loop muted playsInline />
			<div className="hero-content">
				<h1 className="hero-head">The foundation for Health & Performance</h1>
				<p className="hero-para">Reach your wellness potential with our comprehnsive formulas</p>
				<ul className="nav-button">
					<NavButton to="/shop" icon={<FontAwesomeIcon icon={faArrowRight} />} label="Shop Primal Formulas" />
				</ul>
			</div>
		</div>
	) : null;
};

export default Hero;
