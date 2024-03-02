import Loading from '../layouts/Loading';

import { Suspense, lazy, useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Route, Routes, useLocation, Navigate } from 'react-router-dom';

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
				<ScrollToTopPage />
				<Routes>
					<div>
						<h1>hi</h1>
					</div>
				</Routes>
			</Suspense>
		</Router>
	);
};

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
