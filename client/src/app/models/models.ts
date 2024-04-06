export interface Product {
    id: string;
    name: string;
    description: string;
    price: number;
    image: string | File | undefined;
    created: string;
}

export interface About {
    id: string;
    title: string;
    description: string;
    image: string | File | undefined;
    created: string;
}

export interface Asset {
    id: string;
    name: string;
    content: string | File | undefined;
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

export interface CartItem {
    product: Product;
    quantity: number;
}

export interface Cart {
    cartItems: CartItem[];
}
