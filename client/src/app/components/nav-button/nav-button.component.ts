import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';
import { icons } from './nav-button.constants';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-nav-button',
  standalone: true,
  imports: [FontAwesomeModule, RouterModule],
  templateUrl: './nav-button.component.html',
  styleUrl: './nav-button.component.css',
})
export class NavButtonComponent {
  @Input() text: string = '';
  @Input() iconName: string = '';

  @Input() link?: string = '';
  @Input() buttonType?: string;
  @Input() formMethod?: string;

  @Output() onClick: EventEmitter<void> = new EventEmitter<void>();

  get icon(): IconDefinition {
    return icons[this.iconName] || faArrowRight;
  }
}
