import { Component, inject } from '@angular/core';
import { NavLogoComponent } from '../../components/nav-logo/nav-logo.component';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';
import { LoginFormComponent } from '../../forms/login-form/login-form.component';
import { AuthService } from '../../services/auth/auth.service';
import { LoginService } from '../../services/login/login.service';
import { User } from '../../models/models';

@Component({
    selector: 'app-account',
    standalone: true,
    imports: [NavLogoComponent, NavButtonComponent, LoginFormComponent],
    templateUrl: './account.component.html',
    styleUrl: './account.component.css'
})
export class AccountComponent {
    public user: User | null = null;

    public authService = inject(AuthService)
    public loginService = inject(LoginService)

    ngOnInit(): void {
        this.authService.loadFromLocalStorage();
        this.user = this.authService.user();
    }


    public logout() {
        this.loginService.logoutUser().subscribe({
            next: () => {
                // Handle successful logout, e.g., navigate to the login page or set the user to null
                this.user = null;
                // Navigate or update UI as needed
            },
            error: (error) => {
                // Handle any errors, such as showing a message
                console.error('Logout failed', error);
            }
        });
    }

}
