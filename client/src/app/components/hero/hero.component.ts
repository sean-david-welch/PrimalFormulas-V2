import { Component, OnInit } from '@angular/core';
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
export class HeroComponent {
  data: Asset | null = null;
  loading: boolean = false;
  error: string | null = null;

  constructor(private assetService: AssetService) {}

  ngOnInit(): void {
    this.loadAsset();
  }

  private loadAsset(): void {
    this.loading = true;
    this.error = null;

    this.assetService
      .fetchAsset('Hero')
      .pipe(
        catchError((err: Error) => {
          this.error = 'Error loading asset';
          return of(null);
        }),
        finalize(() => (this.loading = false))
      )
      .subscribe((data) => (this.data = data));
  }
}
