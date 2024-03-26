import { About, AboutMutation } from './aboutTypes';
import { Product, ProductMutation } from './productTypes';
import { Asset, AssetMutation } from './assetTypes';

export interface FormField {
	name: string;
	label: string;
	type: string;
	options?: { label: string; value: string | undefined }[];
	placeholder: string;
	defaultValue?: string;
}

export interface CartItem {
	price: number;
	quantity: number;
}

export interface Cart {
	cart: CartItem[];
}

export interface User {
	email: string;
	password: string;
	role: string;
}

export interface ResourceEntry<T> {
	endpoint: string;
	queryKey: string;
	type?: T;
}

export interface Resources {
	users: ResourceEntry<User>;
	cart: ResourceEntry<Cart>;
	products: ResourceEntry<Product | ProductMutation>;
	about: ResourceEntry<About | AboutMutation>;
	assets: ResourceEntry<Asset | AssetMutation>;
}
