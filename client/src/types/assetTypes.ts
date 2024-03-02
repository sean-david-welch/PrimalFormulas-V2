export interface Asset {
	id: string;
	title: string;
	media: string;
	created: string;
}

export interface AssetMutation {
	title: string;
	media: string;
}
