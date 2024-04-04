import { Component, Input, OnInit } from '@angular/core';
import { Asset } from '../../models/models';
import { AssetService } from '../../services/asset/asset.service';
import { RouterModule } from '@angular/router';
import { LoadingSpinnerComponent } from '../loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-nav-logo',
  standalone: true,
  imports: [LoadingSpinnerComponent, RouterModule],
  templateUrl: './nav-logo.component.html',
  styleUrl: './nav-logo.component.css',
})
export class NavLogoComponent implements OnInit {
  isLoading = false;
  data: Asset | null = null;
  error: Error | string | null = null;

  constructor(private assetService: AssetService) {}

  ngOnInit(): void {
    this.loadAsset();
  }

  private loadAsset(): void {
    this.isLoading = true;
    this.error = null;

    this.assetService.fetchAssetByName('logo-small').subscribe({
      next: (response) => {
        this.data = response;
        this.isLoading = false;
      },
      error: (error: Error) => {
        this.isLoading = false;
        this.error = error;
        console.log(error.message);
      },
    });
  }

  @Input() logoWidth?: number = 112;
  @Input() logoHeight?: number = 112;
}
