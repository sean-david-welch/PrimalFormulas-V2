import { Component } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { NavLogoComponent } from '../nav-logo/nav-logo.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { RouterModule } from '@angular/router';
import {
  faBars,
  faCartShopping,
  faUserCircle,
  faX,
} from '@fortawesome/free-solid-svg-icons';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [NavLogoComponent, FontAwesomeModule, RouterModule, CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css',
})
export class SidebarComponent {
  faBars = faBars;
  faX = faX;
  faShopping = faCartShopping;
  faUserCircle = faUserCircle;

  private open = new BehaviorSubject<boolean>(false);

  public open$ = this.open.asObservable();

  public toggleSidebar() {
    this.open.next(!this.open.value);
  }
}
