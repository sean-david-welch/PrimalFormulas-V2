import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { DialogComponent } from '../../components/dialog/dialog.component';
import { NavButtonComponent } from '../../components/nav-button/nav-button.component';
import { NavLogoComponent } from '../../components/nav-logo/nav-logo.component';
import { AuthService } from '../../services/login/login.service';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
    selector: 'app-login-form',
    standalone: true,
    imports: [DialogComponent, NavButtonComponent, NavLogoComponent, ReactiveFormsModule],
    templateUrl: './login-form.component.html',
    styleUrl: './login-form.component.css'
})
export class LoginFormComponent {

    @Input() text: string = '';
    @Output() LoginSuccess = new EventEmitter<void>();

    private authService = inject(AuthService);

    public form: FormGroup = new FormGroup({
        username: new FormControl('', Validators.required),
        password: new FormControl('', Validators.required),
    })

    public onSubmit() {
        if (this.form.invalid) {
            alert('Form is not valid, try again');
            return;
        }

        const { username, password } = this.form.value;

        this.authService.loginUser(username, password).subscribe({
            next: (response) => {
                console.log('Response:', response);
                if (response.token && response.user) {
                    this.LoginSuccess.emit();
                }
            },
            error: (error: Error) => {
                console.error('Login Failed', error.message)
            }
        })
    }
}
