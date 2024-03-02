import config from './env';
import { Resources } from '../types/dataTypes';

const resources: Resources = {
	users: {
		endpoint: new URL('/api/auth/users', config.baseUrl).toString(),
		queryKey: 'users',
	},
	cart: {
		endpoint: new URL('/api/create-checkout-session', config.baseUrl).toString(),
		queryKey: 'cart',
	},
	products: {
		endpoint: new URL('/api/products', config.baseUrl).toString(),
		queryKey: 'products',
	},
	about: {
		endpoint: new URL('/api/about', config.baseUrl).toString(),
		queryKey: 'about',
	},
	assets: {
		endpoint: new URL('/api/assets', config.baseUrl).toString(),
		queryKey: 'assets',
	},
};

export default resources;
