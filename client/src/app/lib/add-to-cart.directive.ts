import { Directive, HostListener, Input } from '@angular/core';
import { CartService } from '../services/cart/cart.service';
import { Product } from '../models/models';

@Directive({
    selector: '[appAddToCart]',
    standalone: true,
})
export class AddToCartDirective {
    @Input('appAddToCart') product: Product | undefined;

    constructor(private cartService: CartService) {}

    @HostListener('click')
    onClick() {
        if (this.product) this.cartService.addItem(this.product, 1);
    }
}
