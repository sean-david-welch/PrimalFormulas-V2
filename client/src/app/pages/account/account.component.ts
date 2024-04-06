import { Component } from '@angular/core';
import { NavLogoComponent } from '../../components/nav-logo/nav-logo.component';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';
import { LoginFormComponent } from '../../forms/login-form/login-form.component';

@Component({
    selector: 'app-account',
    standalone: true,
    imports: [NavLogoComponent, NavButtonComponent, LoginFormComponent],
    templateUrl: './account.component.html',
    styleUrl: './account.component.css'
})
export class AccountComponent {

}
