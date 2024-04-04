import { Component, Input } from '@angular/core';
import { DeleteButtonService } from './delete-button.service';
import { Router } from '@angular/router';
import { NavButtonComponent } from '../nav-button/nav-button.component';

@Component({
    selector: 'app-delete-button',
    standalone: true,
    imports: [NavButtonComponent],
    templateUrl: './delete-button.component.html',
    styleUrl: './delete-button.component.css',
})
export class DeleteButtonComponent {
    public loading: boolean = true;
    public error: Error | null = null;

    constructor(
        private router: Router,
        private deleteButtonService: DeleteButtonService
    ) {}

    public onDelete(): void {
        this.loading = true;
        this.error = null;

        this.deleteButtonService.deleteModel(this.endpoint, this.id).subscribe({
            next: () => {
                this.router.navigate([this.returnPath]);
                this.loading = false;
            },
            error: (error: Error) => {
                this.loading = false;
                this.error = this.error;
                console.error(error.message);
            },
        });
    }

    @Input() text: string = '';
    @Input() endpoint: string = '';
    @Input() id: string = '';
    @Input() returnPath: string = '';
}
