import { Component, OnDestroy, OnInit } from '@angular/core';
import { Product } from '../../models/models';
import { ProductsService } from '../../services/products/products.service';
import { Subscription } from 'rxjs';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';
import { NavButtonComponent } from '../nav-button/nav-button.component';
import { RouterModule } from '@angular/router';
import { IntersectionDirective } from '../../lib/intersection.directive';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@Component({
  selector: 'app-products-list',
  standalone: true,
  imports: [
    LoadingSpinnerComponent,
    NavButtonComponent,
    RouterModule,
    IntersectionDirective,
    FontAwesomeModule,
  ],
  templateUrl: './products-list.component.html',
  styleUrl: './products-list.component.css',
})
export class ProductsListComponent implements OnInit, OnDestroy {
  public loading: boolean = false;
  public error: Error | null = null;
  public products: Product[] = [];

  public getProductLink(id: string): string {
    return `/products/${id}`;
  }

  private productSubscription: Subscription = new Subscription();

  constructor(private productsService: ProductsService) {}

  ngOnInit(): void {
    this.getProducts();
    this.productSubscription = this.productsService.productUpdate$.subscribe(
      (newProduct) => {
        if (newProduct) this.getProducts();
      }
    );
  }

  ngOnDestroy(): void {
    this.productSubscription.unsubscribe();
  }

  private getProducts(): void {
    this.loading = true;
    this.error = null;

    this.productsService.fetchProducts().subscribe({
      next: (response) => {
        this.products = response;
        this.loading = false;
      },
      error: (error: Error) => {
        this.loading = false;
        this.error = error;
        console.log(error.message);
      },
    });
  }
}
