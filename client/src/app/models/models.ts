export interface Product {
    id: string;
    name: string;
    description: string;
    price: number;
    image: string;
    created: string;
}

export interface About {
    id: string;
    title: string;
    description: string;
    image: string;
    created: string;
}

export interface Asset {
    id: string;
    name: string;
    content: string;
    created: string;
}

export interface User {
    id: string;
    username: string;
    email: string;
    password: string;
    is_superuser: boolean;
    last_login: string;
}

export interface MutationResponse<T> {
    model: T;
    image: string;
    presigned_url: string;
}

export interface ImageData {
    imageFile: File;
    presignedUrl: string;
}
