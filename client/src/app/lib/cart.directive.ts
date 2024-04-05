import { Directive, HostListener, Input } from '@angular/core';
import { CartService } from '../services/cart/cart.service';
import { Product } from '../models/models';

@Directive({
    selector: '[appCart]',
    standalone: true,
})
export class CartDirective {
    @Input('updateQuantity') productId: string = '';

    constructor(private cartService: CartService) {}

    @HostListener('input', ['$event'])
    handleInput(event: Event) {
        const inputElement = event.target as HTMLInputElement;
        const newQuantity = parseInt(inputElement.value, 10);
        this.cartService.updateQuantity(this.productId, newQuantity);
    }
}
