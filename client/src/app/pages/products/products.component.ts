import { Component } from '@angular/core';
import { ProductsListComponent } from '../../components/products-list/products-list.component';

@Component({
  selector: 'app-products',
  standalone: true,
  imports: [ProductsListComponent],
  templateUrl: './products.component.html',
  styleUrl: './products.component.css',
})
export class ProductsComponent {}
