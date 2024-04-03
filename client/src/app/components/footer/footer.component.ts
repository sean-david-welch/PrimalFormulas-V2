import { Component } from '@angular/core';
import {
  faFacebook,
  faInstagram,
  faTwitter,
  faYoutube,
} from '@fortawesome/free-brands-svg-icons';
import { NavButtonComponent } from '../nav-button/nav-button.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { ToTopButtonComponent } from '../to-top-button/to-top-button.component';
import { NavLogoComponent } from '../nav-logo/nav-logo.component';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [
    NavButtonComponent,
    FontAwesomeModule,
    ToTopButtonComponent,
    NavLogoComponent,
  ],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css',
})
export class FooterComponent {
  twitter = faTwitter;
  facebook = faFacebook;
  youtube = faYoutube;
  instagram = faInstagram;
}
