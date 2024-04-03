import { Component, Input, OnInit } from '@angular/core';
import { Asset } from '../../models/models';
import { AssetService } from '../../services/asset/asset.service';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-nav-logo',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './nav-logo.component.html',
  styleUrl: './nav-logo.component.css',
})
export class NavLogoComponent {
  @Input() logoWidth?: number = 112;
  @Input() logoHeight?: number = 112;

  data: Asset | null = {
    id: '',
    name: '',
    content: '',
    created: '',
  };

  isLoading = <boolean>false;

  constructor(private assetService: AssetService) {}

  ngOnInit(): void {
    this.isLoading = true;

    this.assetService.fetchAsset('Logo').subscribe((response) => {
      this.data = response;
      this.isLoading = false;
    });
  }
}
