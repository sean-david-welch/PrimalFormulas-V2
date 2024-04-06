import { Component, Input, OnChanges, SimpleChanges, inject } from '@angular/core';
import {
    FormControl,
    FormGroup,
    ReactiveFormsModule,
    Validators,
} from '@angular/forms';
import { DialogComponent } from '../../components/dialog/dialog.component';
import { NavLogoComponent } from '../../components/nav-logo/nav-logo.component';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';
import { MutationResponse, Product } from '../../models/models';
import { ProductsService } from '../../services/products/products.service';

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
    @Input() text: string = '';
    @Input() mode: 'create' | 'update' = 'create';
    @Input() id?: string = '';
    @Input() selectedProduct?: Product;

    public selectedFile: File | null = null;
    private productService = inject(ProductsService)

    public form: FormGroup = new FormGroup({
        name: new FormControl('', Validators.required),
        description: new FormControl('', Validators.required),
        price: new FormControl('', Validators.required),
    });

    ngOnChanges(changes: SimpleChanges): void {
        if (this.selectedProduct) this.form.patchValue(this.selectedProduct);
    }

    private handleProduct(
        action: 'create' | 'update',
        product: Partial<Product>,
        id?: string
    ): void {
        const imageData = this.selectedFile
            ? { imageFile: this.selectedFile }
            : undefined;

        const productData = {
            ...product,
            image: this.selectedFile ? this.selectedFile.name : undefined,
        };

        const apiCall =
            id && action === 'update'
                ? this.productService.mutateProduct(productData, imageData, id)
                : this.productService.mutateProduct(productData, imageData);

        apiCall.subscribe({
            next: (reponse: MutationResponse<Product>) => {
                this.form.reset();
                this.productService.notifyProductAdded(reponse.model);
            },
            error: (error: Error) => {
                console.error('Error occurred', error.message);
            },
        });
    }

    public onFileSelected(event: Event): void {
        const element = event.currentTarget as HTMLInputElement;
        let fileList: FileList | null = element.files;
        if (fileList && fileList.length > 0) {
            this.selectedFile = fileList.item(0);
        } else {
            this.selectedFile = null;
        }
    }

    public onSubmit(): void {
        if (this.form.invalid) {
            alert('Form is not valid');
            return;
        }

        const product: Partial<Product> = this.form.value;

        if (this.mode === 'update' && this.id) {
            this.handleProduct('update', product, this.id);
        } else {
            this.handleProduct('create', product);
        }
    }
}
