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
    @Input() selectedProduct?: Product;

    public form: FormGroup;

    constructor(
        private formBuilder: FormBuilder,
        private productService: ProductsService
    ) {
        this.form = this.formBuilder.group({
            name: ['', Validators.required],
            description: ['', Validators.required],
            price: ['', Validators.required],
            image: ['', Validators.required],
        });
    }

    ngOnChanges(changes: SimpleChanges): void {
        if (this.selectedProduct) this.form.patchValue(this.selectedProduct);
    }

    private handleProduct(
        action: 'create' | 'update',
        product: Product,
        id?: string
    ): void {
        const apiCall =
            id && action === 'update'
                ? this.productService.mutateProduct(product, id)
                : this.productService.mutateProduct(product);

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

    public onSubmit(): void {
        if (this.form.invalid) {
            alert('Form is not valid');
        }

        const product: Product = this.form.getRawValue();

        if (this.mode === 'update' && product.id) {
            this.handleProduct('update', product, product.id);
        } else {
            this.handleProduct('create', product);
        }
    }
}
