import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, catchError, throwError } from 'rxjs';
import { Product, MutationResponse } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { UploadsService } from '../../../services/uploads/uploads.service';

@Injectable({
    providedIn: 'root',
})
export class ProductsService {
    private productUpdate = new BehaviorSubject<Product | null>(null);
    public productUpdate$ = this.productUpdate.asObservable();

    constructor(
        private http: HttpClient,
        private uploadService: UploadsService
    ) {}

    private constructUrl(params?: string): string {
        return params
            ? `http://127.0.0.1:8000/api/products/${params}/`
            : 'http://127.0.0.1:8000/api/products/';
    }

    private handleError(error: Error) {
        console.log('An error occurred', error.message);
        return throwError(() => new Error('An error occurred', error));
    }

    public notifyProductAdded(product: Product): void {
        this.productUpdate.next(product);
    }

    public fetchProducts(): Observable<Product[]> {
        const url = this.constructUrl();

        return this.http.get<Product[]>(url).pipe(catchError(this.handleError));
    }

    public fetchProductById(id: string): Observable<Product> {
        const url = this.constructUrl(id);

        return this.http.get<Product>(url).pipe(catchError(this.handleError));
    }

    public mutateProduct(
        product: Partial<Product>,
        id?: string
    ): Observable<MutationResponse<Product>> {
        if (id) {
            const url = this.constructUrl(id);

            return this.http
                .put<MutationResponse<Product>>(url, product, {
                    withCredentials: true,
                })
                .pipe(catchError(this.handleError));
        } else {
            const url = this.constructUrl();

            return this.http
                .post<MutationResponse<Product>>(url, product, {
                    withCredentials: true,
                })
                .pipe(catchError(this.handleError));
        }
    }

    public deleteProduct(id: string): Observable<Product> {
        const url = this.constructUrl(id);

        return this.http
            .delete<Product>(url, { withCredentials: true })
            .pipe(catchError(this.handleError));
    }
}
