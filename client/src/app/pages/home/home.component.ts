import { Component } from '@angular/core';
import { HeroComponent } from '../../components/hero/hero.component';
import { DisplaysComponent } from '../../components/displays/displays.component';
import { ProductsListComponent } from '../../components/products-list/products-list.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [HeroComponent, DisplaysComponent, ProductsListComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent {}
