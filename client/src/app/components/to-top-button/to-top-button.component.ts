import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faChevronCircleUp } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-to-top-button',
  standalone: true,
  imports: [FontAwesomeModule],
  templateUrl: './to-top-button.component.html',
  styleUrl: './to-top-button.component.css',
})
export class ToTopButtonComponent {
  faChevron = faChevronCircleUp;

  scrollToTop() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  }
}
