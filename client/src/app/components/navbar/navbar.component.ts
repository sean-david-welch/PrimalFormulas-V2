import { Component, Input } from '@angular/core';
import { NavigationStart, Router } from '@angular/router';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import {
  faCartShopping,
  faUserCircle,
} from '@fortawesome/free-solid-svg-icons';

import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NavButtonComponent } from '../nav-button/nav-button.component';
import { SidebarComponent } from '../sidebar/sidebar.component';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [FontAwesomeModule, NavButtonComponent, SidebarComponent],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {
  public isHomePage: boolean = true;
  public cartShoppingIcon: IconDefinition = faCartShopping;
  public userCircleIcon: IconDefinition = faUserCircle;

  constructor(private router: Router) {
    router.events.subscribe((event) => {
      if (event instanceof NavigationStart) {
        this.isHomePage = event.url === '/';
      }
    });
  }
}
