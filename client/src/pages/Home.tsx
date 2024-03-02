import Hero from '../templates/Hero';
import Loading from '../layouts/Loading';
import ErrorPage from '../layouts/Error';
import NavButton from '../components/NavButton';
import BenefitsHome from '../templates/Benefits';
import SectionHeading from '../components/SectionHeading';

import { Product } from '../types/productTypes';
import { useGetResource } from '../hooks/dataHooks';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight, faCartPlus } from '@fortawesome/free-solid-svg-icons';

export const Home = () => {
	const { data: products, isLoading, isError } = useGetResource<Product[]>('products');

	if (isLoading) return <Loading />;
	if (isError) return <ErrorPage />;

	return (
		<section id="home">
			<Hero />
			<BenefitsHome />
			<SectionHeading
				headingText="Browse Our Products:"
				buttonLabel="View All Products"
				buttonUrl="/Shop"
				buttonIcon={<FontAwesomeIcon icon={faArrowRight} className="icon" />}
			/>
			<ul>
				{products &&
					products.map(product => (
						<li key={product.id} className="hidden">
							<div className="product-card">
								<h2>{product.name}</h2>
								<img src={product.image} alt={product.name} />
								<h2>Price: €{product.price}</h2>

								<ul className="product-nav">
									<NavButton
										to={`/product/${product.id}`}
										icon={<FontAwesomeIcon icon={faArrowRight} />}
										label="View Product"
									/>

									<NavButton
										to={'/cart'}
										icon={<FontAwesomeIcon icon={faCartPlus} />}
										label="Add to Cart"
										onClick={() => {}}
									/>
								</ul>
							</div>
						</li>
					))}
			</ul>
		</section>
	);
};

export default Home;
