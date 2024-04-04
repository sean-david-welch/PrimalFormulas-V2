import { HttpClient, HttpHandler, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ImageData } from '../../app/models/models';
import { Observable, catchError, map, throwError } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class UploadsService {
    constructor(private http: HttpClient) {
        this.http = http;
    }

    public uploadImage(imageData: ImageData): Observable<any> {
        const { imageFile, presignedUrl } = imageData;
        const headers = new HttpHeaders({
            'Content-Type': imageFile.type,
        });

        return this.http
            .put(presignedUrl, imageFile, {
                headers,
                observe: 'response',
            })
            .pipe(
                map((response) => {
                    return response.status;
                }),
                catchError((error) => {
                    console.error('Error in uploadImage:', error);
                    console.error('Failed imageData:', imageData);
                    return throwError(
                        () => new Error('Failed to upload image')
                    );
                })
            );
    }
}
