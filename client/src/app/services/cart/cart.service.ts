import { Injectable, signal } from '@angular/core';
import { Cart, CartItem, Product } from '../../models/models';

@Injectable({
    providedIn: 'root',
})
export class CartService {
    public cartItems = signal<CartItem[]>([]);

    public getTotalItems(): number {
        return this.cartItems().reduce((acc, item) => acc + item.quantity, 0);
    }

    public getTotalPrice(): number {
        return this.cartItems().reduce(
            (acc, item) => acc + item.product.price * item.quantity,
            0
        );
    }

    public addItem(product: Product, quantity: number = 1): void {
        const existingIndex = this.cartItems().findIndex(
            (item) => item.product.id === product.id
        );

        if (existingIndex !== -1) {
            const updatedItems = [...this.cartItems()];

            updatedItems[existingIndex] = {
                ...updatedItems[existingIndex],
                quantity: updatedItems[existingIndex].quantity + quantity,
            };

            this.cartItems.set(updatedItems);
        } else {
            this.cartItems.set([...this.cartItems(), { product, quantity }]);
        }
    }

    public removeItem(productId: string): void {
        this.cartItems.set(
            this.cartItems().filter((item) => item.product.id !== productId)
        );
    }

    public updateQuantity(productId: string, quantity: number): void {
        const updatedItems = this.cartItems().map((item) => {
            if (item.product.id === productId) {
                return { ...item, quantity };
            }
            return item;
        });

        this.cartItems.set(updatedItems);
    }

    public clearCart(): void {
        this.cartItems.set([]);
    }
}
