import { Component } from '@angular/core';
import { NavLogoComponent } from '../../components/nav-logo/nav-logo.component';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';

@Component({
  selector: 'app-not-found',
  standalone: true,
  imports: [NavLogoComponent, NavButtonComponent],
  templateUrl: './not-found.component.html',
  styleUrl: './not-found.component.css',
})
export class NotFoundComponent {}
