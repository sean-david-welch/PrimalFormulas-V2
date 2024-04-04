import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  Observable,
  catchError,
  shareReplay,
  throwError,
} from 'rxjs';
import { Asset, MutationResponse } from '../../models/models';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AssetService {
  private assetUpdate = new BehaviorSubject<Asset | null>(null);
  public assetUpdate$ = this.assetUpdate.asObservable();

  private cache: Record<string, Observable<Asset | null>> = {};

  constructor(private http: HttpClient) {
    this.http = http;
  }

  private constructUrl(name?: string): string {
    return name
      ? `http://127.0.0.1:8000/api/assets/${name}`
      : 'http://127.0.0.1:8000/api/assets/';
  }

  private handleError(error: Error) {
    console.log('An error occurred', error.message);
    return throwError(() => new Error('An error occurred', error));
  }

  public notifyAssetAdded(asset: Asset): void {
    this.assetUpdate.next(asset);
  }

  public fetchAssets(): Observable<Asset[]> {
    const url = this.constructUrl();

    return this.http.get<Asset[]>(url).pipe(catchError(this.handleError));
  }

  public fetchAssetByName(name: string): Observable<Asset | null> {
    if (this.cache[name]) {
      return this.cache[name];
    }
    const url = this.constructUrl(name);

    const asset = (this.cache[name] = this.http
      .get<Asset>(url)
      .pipe(shareReplay(1), catchError(this.handleError)));

    return asset;
  }

  public mutateAsset(
    asset: Partial<Asset>,
    name?: string
  ): Observable<MutationResponse<Asset>> {
    if (name) {
      const url = this.constructUrl(name);

      return this.http
        .put<MutationResponse<Asset>>(url, asset, { withCredentials: true })
        .pipe(catchError(this.handleError));
    } else {
      const url = this.constructUrl();

      return this.http
        .post<MutationResponse<Asset>>(url, asset, { withCredentials: true })
        .pipe(catchError(this.handleError));
    }
  }

  public deleteAsset(name: string): Observable<Asset> {
    const url = this.constructUrl(name);

    return this.http
      .delete<Asset>(url, { withCredentials: true })
      .pipe(catchError(this.handleError));
  }
}
