import { Injectable, signal, computed, WritableSignal } from '@angular/core';
import { CartItem, Product } from '../../models/models';

const CART_KEY = 'shopping_cart'

@Injectable({
    providedIn: 'root',
})
export class CartService {
    public cartItems: WritableSignal<CartItem[]> = signal<CartItem[]>([]);


    public loadFromLocalStorage() {
        const storedCart = localStorage.getItem(CART_KEY)

        if (storedCart) {
            this.cartItems.set(JSON.parse(storedCart));
        }
    }

    private saveToLocalStoage() {
        localStorage.setItem(CART_KEY, JSON.stringify(this.cartItems()));
    }

    public totalItems = computed(() => this.cartItems().reduce((acc, item) => acc + item.quantity, 0));

    public totalPrice = computed(() => this.cartItems().reduce(
        (acc, item) => acc + item.product.price * item.quantity,
        0
    ));

    public addItem(product: Product, quantity: number = 1): void {
        const existingIndex = this.cartItems().findIndex(
            (item) => item.product.id === product.id
        );

        if (existingIndex !== -1) {
            const updatedItems = this.cartItems();
            updatedItems[existingIndex].quantity += quantity;
            this.cartItems.set(updatedItems);
        } else {
            this.cartItems.set([...this.cartItems(), { product, quantity }]);
        }

        this.saveToLocalStoage();
    }

    public removeItem(productId: string): void {
        this.cartItems.set(
            this.cartItems().filter((item) => item.product.id !== productId)
        );

        this.saveToLocalStoage();
    }

    public updateQuantity(productId: string, quantity: number): void {
        const updatedItems = this.cartItems().map((item) => {
            if (item.product.id === productId) {
                return { ...item, quantity };
            }
            return item;
        });

        this.cartItems.set(updatedItems);
        this.saveToLocalStoage();
    }

    public clearCart(): void {
        this.cartItems.set([]);
        this.saveToLocalStoage()
    }
}
