import { Injectable, inject } from '@angular/core';
import {
    BehaviorSubject,
    Observable,
    catchError,
    map,
    of,
    switchMap,
    throwError,
} from 'rxjs';
import { Product, MutationResponse } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { UploadsService } from '../../../services/uploads/uploads.service';

@Injectable({
    providedIn: 'root',
})
export class ProductsService {
    private productUpdate = new BehaviorSubject<Product | null>(null);
    public productUpdate$ = this.productUpdate.asObservable();

    private http = inject(HttpClient);
    private uploadService = inject(UploadsService);

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
        imageData?: { imageFile: File },
        id?: string
    ): Observable<MutationResponse<Product>> {
        const mutationObservable = id
            ? this.http.put<MutationResponse<Product>>(
                this.constructUrl(id),
                product,
                {
                    withCredentials: true,
                }
            )
            : this.http.post<MutationResponse<Product>>(
                this.constructUrl(),
                product,
                {
                    withCredentials: true,
                }
            );

        return mutationObservable.pipe(
            switchMap((response) => {
                if (imageData && response.presigned_url) {
                    return this.uploadService
                        .uploadImage({
                            imageFile: imageData.imageFile,
                            presignedUrl: response.presigned_url,
                        })
                        .pipe(
                            map((uploadResponse) => {
                                return {
                                    ...response,
                                    uploadResponse,
                                };
                            })
                        );
                } else {
                    if (!response.presigned_url) {
                    }
                    return of(response);
                }
            }),
            catchError(this.handleError)
        );
    }

    public deleteProduct(id: string): Observable<Product> {
        const url = this.constructUrl(id);

        return this.http
            .delete<Product>(url, { withCredentials: true })
            .pipe(catchError(this.handleError));
    }
}
