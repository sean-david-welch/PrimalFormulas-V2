import { Injectable } from '@angular/core';
import { Observable, catchError, shareReplay, throwError } from 'rxjs';
import { Asset } from '../../models/models';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AssetService {
  private constructUrl(name: string): string {
    return `http://127.0.0.1:8000/assets/${name}`;
  }

  private cache: Record<string, Observable<Asset>> = {};

  constructor(private http: HttpClient) {
    this.http = http;
  }

  public fetchAsset(name: string): Observable<Asset> {
    if (this.cache[name]) {
      return this.cache[name];
    }
    const url = this.constructUrl(name);

    const asset = (this.cache[name] = this.http.get<Asset>(url).pipe(
      shareReplay(1),
      catchError((error) => {
        return throwError(() => new Error('Fetch Failed', error));
      })
    ));

    return asset;
  }
}
