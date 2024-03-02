import Loading from '../layouts/Loading';

import { Suspense, lazy, useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Route, Routes, useLocation, Navigate } from 'react-router-dom';
import Layout from '../layouts/Layout';

const Home = lazy(() => import('../pages/Home'));
const About = lazy(() => import('../pages/About'));
const Products = lazy(() => import('../pages/Products'));

const AppRoutes = () => {
	const ScrollToTopPage = () => {
		const { pathname } = useLocation();

		useEffect(() => {
			window.scrollTo(0, 0);
		}, [pathname]);

		return null;
	};

	return (
		<Router>
			<Suspense fallback={<Loading />}>
				<Layout>
					<ScrollToTopPage />
					<Routes>
						<Route path="/" element={<Home />} />
						<Route path="/about" element={<About />} />
						<Route path="/products" element={<Products />} />
					</Routes>
				</Layout>
			</Suspense>
		</Router>
	);
};

export default AppRoutes;

// const routes: Routes = [
//     { path: '', component: HomeComponent },
//     { path: 'about', component: AboutComponent },
//     { path: 'account', component: AccountComponent },
//     { path: 'cart', component: CartComponent },
//     { path: 'products', component: ProductsComponent },
//     { path: 'products/:id', component: ProductDetailComponent },
//     { path: 'checkout', component: CheckoutComponent },
//     { path: 'not-found', component: NotFoundComponent },
//     { path: '**', redirectTo: '/not-found' },
// ];
