import { Component, OnChanges, SimpleChanges } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { DialogComponent } from '../../components/dialog/dialog.component';
import { NavLogoComponent } from '../../components/nav-logo/nav-logo.component';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';

@Component({
    selector: 'app-product-form',
    standalone: true,
    imports: [
        ReactiveFormsModule,
        DialogComponent,
        NavLogoComponent,
        NavButtonComponent,
    ],
    templateUrl: './product-form.component.html',
    styleUrl: './product-form.component.css',
})
export class ProductFormComponent implements OnChanges {
    public form: FormGroup;

    ngOnChanges(changes: SimpleChanges): void {}
}
