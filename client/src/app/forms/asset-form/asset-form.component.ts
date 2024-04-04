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
import { Asset, MutationResponse } from '../../models/models';
import { AssetService } from '../../services/asset/asset.service';

@Component({
    selector: 'app-asset-form',
    standalone: true,
    imports: [
        ReactiveFormsModule,
        DialogComponent,
        NavLogoComponent,
        NavButtonComponent,
    ],
    templateUrl: './asset-form.component.html',
    styleUrl: './asset-form.component.css',
})
export class AssetFormComponent implements OnChanges {
    @Input() text: string = '';
    @Input() mode: 'create' | 'update' = 'create';
    @Input() selectedAsset?: Asset;

    public form: FormGroup;

    constructor(private builder: FormBuilder, private service: AssetService) {
        this.form = this.builder.group({
            name: ['', Validators.required],
            description: ['', Validators.required],
            price: ['', Validators.required],
            image: ['', Validators.required],
        });
    }

    ngOnChanges(changes: SimpleChanges): void {
        if (this.selectedAsset) this.form.patchValue(this.selectedAsset);
    }

    private handleAsset(
        action: 'create' | 'update',
        asset: Asset,
        name?: string
    ): void {
        const apiCall =
            name && action === 'update'
                ? this.service.mutateAsset(asset, name)
                : this.service.mutateAsset(asset);

        apiCall.subscribe({
            next: (respone: MutationResponse<Asset>) => {
                this.form.reset();
                this.service.notifyAssetAdded(respone.model);
            },
            error: (error: Error) => {
                console.error('Error occurred', error.message);
            },
        });
    }

    public onSubmit(): void {
        if (this.form.invalid) {
            alert('Form is not valid');
        }

        const asset: Asset = this.form.getRawValue();

        if (this.mode === 'update' && asset.id) {
            this.handleAsset('update', asset, asset.id);
        } else {
            this.handleAsset('create', asset);
        }
    }
}
