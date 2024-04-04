import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import {
    FormBuilder,
    FormGroup,
    ReactiveFormsModule,
    Validators,
} from '@angular/forms';
import { DialogComponent } from '../../components/dialog/dialog.component';
import { NavLogoComponent } from '../../components/nav-logo/nav-logo.component';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';
import { About, MutationResponse } from '../../models/models';
import { AboutService } from '../../services/about/about.service';

@Component({
    selector: 'app-about-form',
    standalone: true,
    imports: [
        ReactiveFormsModule,
        DialogComponent,
        NavLogoComponent,
        NavButtonComponent,
    ],
    templateUrl: './about-form.component.html',
    styleUrl: './about-form.component.css',
})
export class AboutFormComponent implements OnChanges {
    @Input() text: string = '';
    @Input() mode: 'create' | 'update' = 'create';
    @Input() selectedAbout?: About;

    public form: FormGroup;

    constructor(private builder: FormBuilder, private service: AboutService) {
        this.form = this.builder.group({
            title: ['', Validators.required],
            description: ['', Validators.required],
            image: ['', Validators.required],
        });
    }

    ngOnChanges(changes: SimpleChanges): void {
        if (this.selectedAbout) this.form.patchValue(this.selectedAbout);
    }

    private handleAbout(
        action: 'create' | 'update',
        about: About,
        id?: string
    ): void {
        const apiCall =
            id && action === 'update'
                ? this.service.mutateAbout(about, id)
                : this.service.mutateAbout(about);

        apiCall.subscribe({
            next: (response: MutationResponse<About>) => {
                this.form.reset();
                this.service.notifyAboutAdded(response.model);
            },
            error: (error: Error) => {
                console.error('Error occurred', error.message);
            },
        });
    }

    public onSubmit(): void {
        if (this.form.invalid) alert('Form is not valid');

        const about: About = this.form.getRawValue();

        if (this.mode === 'update' && about.id) {
            this.handleAbout('update', about, about.id);
        } else {
            this.handleAbout('create', about);
        }
    }
}
