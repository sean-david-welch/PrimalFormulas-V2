import { Component, OnInit, inject } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { LoginService } from '../../services/login/login.service';
import { User } from '../../models/models';
import { RouterModule } from '@angular/router';
import { LoginFormComponent } from '../../forms/login-form/login-form.component';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [RouterModule, LoginFormComponent],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit {
    public user: User | null = null;

    public authService = inject(AuthService)
    public loginService = inject(LoginService)

    ngOnInit(): void {
        this.authService.loadFromLocalStorage();
    }


}
