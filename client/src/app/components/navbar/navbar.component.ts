import { Component, Input } from '@angular/core';
import { NavigationStart, Router } from '@angular/router';
import {
  IconDefinition,
  faArrowRight,
} from '@fortawesome/free-solid-svg-icons';
import { navbarLinkIcons } from './navbar.constants';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NavButtonComponent } from '../nav-button/nav-button.component';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [FontAwesomeModule, NavButtonComponent],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {
  public isHomePage: boolean = true;

  constructor(private router: Router) {
    router.events.subscribe((event) => {
      if (event instanceof NavigationStart) {
        this.isHomePage = event.url === '/';
      }
    });
  }

  @Input() iconName: string = '';
  get icon(): IconDefinition {
    return navbarLinkIcons[this.iconName] || faArrowRight;
  }
}
