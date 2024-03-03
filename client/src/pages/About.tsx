import styles from '../styles/About.module.css';

import { About } from '../types/aboutTypes';
import { useGetResource } from '../hooks/dataHooks';

import { faArrowRight } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import SectionHeading from '../components/SectionHeading';

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

			<div className={styles.about}>
				<ul className={styles.infoList}>
					{abouts &&
						abouts.map(about => (
							<li className={styles.aboutCard}>
								<img src={about.image} alt="Info-Item" />
								<div className={styles.aboutInfo}>
									<h2 className={styles.sectionHeading}>{about.title}:</h2>
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
