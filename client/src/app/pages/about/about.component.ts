import { Component, OnDestroy, OnInit } from '@angular/core';
import { LoadingSpinnerComponent } from '../../components/loading-spinner/loading-spinner.component';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';

import { About } from '../../models/models';
import { Subscription } from 'rxjs';
import { AboutService } from '../../services/about/about.service';
import { AboutFormComponent } from '../../forms/about-form/about-form.component';
import { DeleteButtonComponent } from '../../components/delete-button/delete-button.component';

@Component({
    selector: 'app-about',
    standalone: true,
    imports: [
        LoadingSpinnerComponent,
        NavButtonComponent,
        AboutFormComponent,
        DeleteButtonComponent,
    ],
    templateUrl: './about.component.html',
    styleUrl: './about.component.css',
})
export class AboutComponent implements OnInit, OnDestroy {
    public isLoading: boolean = false;
    public error: Error | null = null;
    public abouts: About[] = [];

    private aboutSubscription: Subscription = new Subscription();

    constructor(private aboutService: AboutService) {
        this.aboutService = aboutService;
    }

    ngOnInit(): void {
        this.getAbouts();
        this.aboutSubscription = this.aboutService.aboutUpdate$.subscribe(
            (newAbout) => {
                if (newAbout) this.getAbouts();
            }
        );
    }

    ngOnDestroy(): void {
        this.aboutSubscription.unsubscribe();
    }

    private getAbouts(): void {
        this.isLoading = true;
        this.error = null;

        this.aboutService.fetchAbouts().subscribe({
            next: (response: About[]) => {
                this.abouts = response;
                this.isLoading = false;
            },
            error: (error: Error) => {
                this.isLoading = false;
                this.error = error;
                console.log(error.message);
            },
        });
    }
}
