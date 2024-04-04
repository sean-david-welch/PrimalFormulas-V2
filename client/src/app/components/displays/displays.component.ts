import { Component, Input } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import {
  faRightFromBracket,
  faShieldVirus,
  faFire,
  faAtom,
  faHammer,
} from '@fortawesome/free-solid-svg-icons';
import { IntersectionDirective } from '../../lib/intersection.directive';

@Component({
  selector: 'app-displays',
  standalone: true,
  imports: [FontAwesomeModule, IntersectionDirective],
  templateUrl: './displays.component.html',
  styleUrl: './displays.component.css',
})
export class DisplaysComponent {
  @Input() icon: IconDefinition = faRightFromBracket;
  @Input() title?: string;
  @Input() description?: string;

  public benefits = [
    {
      icon: faShieldVirus,
      title: 'Increased Immune Function',
      description:
        "Boost your immune system and defend against illnesses with our desiccated organ supplements. Strengthen your body's natural defense mechanism.",
    },
    {
      icon: faFire,
      title: 'Increased Energy Levels',
      description:
        'Experience a natural energy boost throughout the day. Our desiccated organ supplements provide essential nutrients to fuel your body and enhance vitality.',
    },
    {
      icon: faAtom,
      title: 'Helps Autoimmune Issues',
      description:
        'Find relief and support for autoimmune conditions. Our desiccated organ supplements aid in managing symptoms and promoting overall well-being.',
    },
    {
      icon: faHammer,
      title: 'Faster Recovery',
      description:
        "Enhance your body's recovery process after physical exertion. Our desiccated organ supplements assist in faster healing and rejuvenation.",
    },
  ];
}
