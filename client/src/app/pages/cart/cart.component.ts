import { Component, OnInit } from '@angular/core';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';
import { RouterModule } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { CartService } from '../../services/cart/cart.service';
import { CartDirective } from '../../lib/cart.directive';
import { CartItem } from '../../models/models';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-cart',
    standalone: true,
    imports: [
        NavButtonComponent,
        RouterModule,
        FontAwesomeModule,
        CartDirective,
        CommonModule
    ],
    templateUrl: './cart.component.html',
    styleUrl: './cart.component.css',
})
export class CartComponent implements OnInit {
    public cartItems: CartItem[] = [];


    constructor(private cartService: CartService) {

    }

    ngOnInit(): void {
        this.cartService.loadFromLocalStorage();
        this.cartItems = this.cartService.cartItems();
    }

    public getTotalItems(): number {
        return this.cartService.totalItems();
    }

    public getTotalPrice(): number {
        const totalPrice = this.cartService.totalPrice();
        console.log('total price', totalPrice)
        return totalPrice
    }

    public removeItem(productId: string): void {
        this.cartService.removeItem(productId);
    }

    public updateQuantity(productId: string, quantity: number): void {
        this.cartService.updateQuantity(productId, quantity);
    }

    faTrash = faTrash;
}
