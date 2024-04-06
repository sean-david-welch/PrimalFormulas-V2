import { Component, OnInit, inject } from '@angular/core';
import { Asset } from '../../models/models';
import { AssetService } from '../../services/asset/asset.service';
import { catchError, finalize, of } from 'rxjs';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';
import { NavButtonComponent } from '../nav-button/nav-button.component';

@Component({
    selector: 'app-hero',
    standalone: true,
    imports: [LoadingSpinnerComponent, NavButtonComponent],
    templateUrl: './hero.component.html',
    styleUrl: './hero.component.css',
})
export class HeroComponent implements OnInit {
    data: Asset | undefined;
    loading: boolean = false;
    error: string | null = null;

    assetService = inject(AssetService)

    ngOnInit(): void {
        this.loadAsset();
    }

    private loadAsset(): void {
        this.loading = true;
        this.error = null;

        this.assetService
            .fetchAssetByName('Hero').subscribe({
                next: (data) => {
                    if (data) {
                        this.data = data;
                        this.loading = false;
                        setTimeout(() => {
                            const videoElement = document.querySelector('video');
                            if (videoElement instanceof HTMLVideoElement) {
                                videoElement.play().catch(e => console.error("Autoplay failed", e));
                            }
                        }, 0);
                    }
                },
                error: (error) => {
                    this.error = 'Error loading asset';
                    this.loading = false;
                }
            })

    }
}
