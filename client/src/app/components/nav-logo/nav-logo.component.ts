import { Component, Input, OnInit } from '@angular/core';
import { Asset } from '../../models/models';
import { AssetService } from '../../services/asset/asset.service';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { catchError, finalize, of, switchMap, tap } from 'rxjs';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-nav-logo',
  standalone: true,
  imports: [LoadingSpinnerComponent, RouterModule],
  templateUrl: './nav-logo.component.html',
  styleUrl: './nav-logo.component.css',
})
export class NavLogoComponent {
  isLoading = false;
  data: Asset | null = null;
  error: string | null = null;

  constructor(private assetService: AssetService, private router: Router) {}

  ngOnInit(): void {
    this.loadAsset();
  }

  private loadAsset(): void {
    this.isLoading = true;
    this.error = null;

    this.assetService
      .fetchAsset('Logo')
      .pipe(
        catchError((err) => {
          this.error = 'Error loading asset';
          return of(null);
        }),
        finalize(() => (this.isLoading = false))
      )
      .subscribe((data) => (this.data = data));
  }

  @Input() logoWidth?: number = 112;
  @Input() logoHeight?: number = 112;
}
