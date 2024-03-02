export interface Product {
	id: string;
	name: string;
	description: string;
	price: number;
	image: string;
	created: string;
}

export interface ProductMutation {
	name: string;
	description: string;
	price: number;
	image: string;
}
