import { Component, ElementRef, Input, ViewChild } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NavButtonComponent } from '../nav-button/nav-button.component';
import { IconDefinition } from '@fortawesome/fontawesome-svg-core';
import { faX } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-dialog',
  standalone: true,
  imports: [FontAwesomeModule, NavButtonComponent],
  templateUrl: './dialog.component.html',
  styleUrl: './dialog.component.css',
})
export class DialogComponent {
  faX: IconDefinition = faX;
  showForm: boolean = false;

  @Input() text!: string;
  @ViewChild('dialog') dialog!: ElementRef<HTMLDialogElement>;

  private updateDialogState() {
    const dialogElement = this.dialog.nativeElement;
    if (this.showForm) {
      dialogElement.showModal();
      dialogElement.classList.add('dialog-visible');
    } else {
      dialogElement.close();
      dialogElement.classList.remove('dialog-visible');
    }
  }

  toggleDialog() {
    this.showForm = !this.showForm;
    this.updateDialogState();
  }

  closeDialog() {
    this.showForm = false;
    this.updateDialogState();
  }
}
