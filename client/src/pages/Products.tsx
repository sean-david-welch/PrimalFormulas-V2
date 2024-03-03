import styles from '../styles/Products.module.css';

import Loading from '../layouts/Loading';
import ErrorPage from '../layouts/Error';
import NavButton from '../components/NavButton';

import { Product } from '../types/productTypes';
import { useGetResource } from '../hooks/dataHooks';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight, faCartPlus } from '@fortawesome/free-solid-svg-icons';

function ProductsList() {
	const { data: products, isLoading, isError } = useGetResource<Product[]>('products');

	if (isLoading) return <Loading />;
	if (isError) return <ErrorPage />;

	return (
		<section id="products">
			<div className={styles.products}>
				<ul>
					{products &&
						products.map(product => (
							<li key={product.id} className="hidden">
								<div className={styles.productsCard}>
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
			</div>
		</section>
	);
}

export default ProductsList;
