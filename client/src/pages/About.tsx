import SectionHeading from '../components/SectionHeading';

import { About } from '../types/aboutTypes';
import { useGetResource } from '../hooks/dataHooks';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';

export const AboutPage = () => {
	const { data: abouts, isError, isLoading } = useGetResource<About[]>('about');

	if (isLoading) return <div>Loading....</div>;

	if (isError) return <div>Error....</div>;

	return (
		<section id="about">
			<SectionHeading
				headingText="Company Values & History:"
				buttonLabel="View our Products"
				buttonUrl="/shop"
				buttonIcon={<FontAwesomeIcon icon={faArrowRight} className="icon" />}
			/>

			<div className="company-info">
				<ul className="info-list">
					{abouts &&
						abouts.map(about => (
							<li className="info-list-item hidden">
								<img src={about.image} alt="Info-Item" />
								<div className="info-description">
									<h2 className="section-heading">{about.title}:</h2>
									<p>{about.description}</p>
								</div>
							</li>
						))}
				</ul>
			</div>
		</section>
	);
};

export default AboutPage;
