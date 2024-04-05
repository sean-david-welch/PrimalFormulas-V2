import { Component } from '@angular/core';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';
import { RouterModule } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { CartService } from '../../services/cart/cart.service';
import { CartDirective } from '../../lib/cart.directive';

@Component({
    selector: 'app-cart',
    standalone: true,
    imports: [
        NavButtonComponent,
        RouterModule,
        FontAwesomeModule,
        CartDirective,
    ],
    templateUrl: './cart.component.html',
    styleUrl: './cart.component.css',
})
export class CartComponent {
    faTrash = faTrash;

    constructor(private cartService: CartService) {}

    public cartItems = this.cartService.cartItems();

    public getTotalPrice(): void {
        this.cartService.getTotalPrice();
    }

    public removeItem(productId: string): void {
        this.cartService.removeItem(productId);
    }

    public updateQuantity(productId: string, quantity: number): void {
        this.cartService.updateQuantity(productId, quantity);
    }
}
