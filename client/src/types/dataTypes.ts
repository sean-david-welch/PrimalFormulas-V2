interface CartItem {
    price: number;
    quantity: number;
}

interface PaymentData {
    cart: CartItem[];
}

interface User {
    email: string;
    password: string;
    role: string;
}
