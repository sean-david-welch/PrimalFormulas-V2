import { Injectable, inject } from '@angular/core';
import { LoginResponse, UserData } from '../../models/models';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, tap, throwError } from 'rxjs';
import { AuthService } from '../auth/auth.service';

@Injectable({
    providedIn: 'root'
})
export class LoginService {

    private http = inject(HttpClient)
    private authService = inject(AuthService)

    private handleError(error: Error) {
        console.log('An error occurred', error.message);
        return throwError(() => new Error('An error occurred', error));
    }

    public registerUser(userData: UserData) {
        const url = 'http://127.0.0.1:8000/register/'

        return this.http.post(url, userData, {}).pipe(catchError(this.handleError));
    }

    public loginUser(username: string, password: string): Observable<LoginResponse> {
        const url = 'http://127.0.0.1:8000/login/'

        return this.http.post<LoginResponse>(url, { username: username, password: password }, {})
            .pipe(tap((response) => this.authService.login(response.user)), catchError(this.handleError));
    }

    public logoutUser(): Observable<void> {
        const url = 'http://127.0.0.1:8000/logout/'

        return this.http.post<void>(url, { withCredential: true })
            .pipe(tap(() => this.authService.logout()), catchError(this.handleError));

    }
}

