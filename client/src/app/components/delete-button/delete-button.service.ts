import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class DeleteButtonService {
    private constructUrl(endpoint: string, params: string): string {
        return String(
            new URL(endpoint + '/' + params + '/', 'http://127.0.0.1:8000/api/')
        );
    }

    constructor(private http: HttpClient) {
        this.http = http;
    }

    private handleError(error: Error) {
        console.log('An error occurred', error.message);
        return throwError(() => new Error('An error occurred', error));
    }

    public deleteModel(endpoint: string, params: string): Observable<void> {
        const url = this.constructUrl(endpoint, params);

        return this.http
            .delete<void>(url, { withCredentials: true })
            .pipe(catchError(this.handleError));
    }
}
