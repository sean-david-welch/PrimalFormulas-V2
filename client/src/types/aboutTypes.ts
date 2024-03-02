export interface About {
	id: string;
	title: string;
	description: string;
	image: string;
	created: string;
}

export interface AboutMutation {
	title: string;
	description: string;
	image: string;
}
