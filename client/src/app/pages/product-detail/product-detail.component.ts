import { Component, OnInit } from '@angular/core';
import { LoadingSpinnerComponent } from '../../components/loading-spinner/loading-spinner.component';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';
import { Product } from '../../models/models';
import { ProductsService } from '../../services/products/products.service';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-product-detail',
    standalone: true,
    imports: [LoadingSpinnerComponent, NavButtonComponent, CommonModule],
    templateUrl: './product-detail.component.html',
    styleUrl: './product-detail.component.css',
})
export class ProductDetailComponent implements OnInit {
    public isLoading: boolean = false;
    public error: Error | null = null;
    public product: Partial<Product> = {};

    constructor(
        private productService: ProductsService,
        private route: ActivatedRoute
    ) {}

    ngOnInit(): void {
        this.getProduct();

        this.productService.productUpdate$.subscribe((newProduct) => {
            if (newProduct) this.getProduct();
        });
    }

    private getProduct(): void {
        this.isLoading = true;
        this.error = null;

        this.route.params.subscribe((params) => {
            const id = params['id'];

            this.productService.fetchProductById(id).subscribe({
                next: (response) => {
                    this.product = response;
                    this.isLoading = false;
                },
                error: (error: Error) => {
                    this.isLoading = false;
                    this.error = error;
                    console.log(error.message);
                },
            });
        });
    }
}
