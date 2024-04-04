import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, catchError, throwError } from 'rxjs';
import { About, Asset, MutationResponse } from '../../models/models';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AboutService {
  private aboutUpdate = new BehaviorSubject<About | null>(null);
  private aboutUpdate$ = this.aboutUpdate.asObservable();

  constructor(private http: HttpClient) {
    this.http = http;
  }

  private constructUrl(params?: string): string {
    return params
      ? `http://127.0.0.1:8000/api/about/${params}`
      : 'http://127.0.0.1:8000/api/about/';
  }

  private handleError(error: Error) {
    console.log('An error occurred', error.message);
    return throwError(() => new Error('An error occurred', error));
  }

  public notifyAboutAdded(about: About): void {
    this.aboutUpdate.next(about);
  }

  public fetchAbouts(): Observable<About[]> {
    const url = this.constructUrl();

    return this.http.get<About[]>(url).pipe(catchError(this.handleError));
  }

  public fetchAboutById(id: string): Observable<About> {
    const url = this.constructUrl(id);

    return this.http.get<About>(url).pipe(catchError(this.handleError));
  }

  public mutateAbout(
    about: Partial<About>,
    id?: string
  ): Observable<MutationResponse<About>> {
    if (id) {
      const url = this.constructUrl(id);

      return this.http
        .put<MutationResponse<About>>(url, about, { withCredentials: true })
        .pipe(catchError(this.handleError));
    } else {
      const url = this.constructUrl();

      return this.http
        .post<MutationResponse<About>>(url, about, { withCredentials: true })
        .pipe(catchError(this.handleError));
    }
  }

  public deleteAbout(id: string): Observable<About> {
    const url = this.constructUrl(id);

    return this.http
      .delete<About>(url, { withCredentials: true })
      .pipe(catchError(this.handleError));
  }
}
