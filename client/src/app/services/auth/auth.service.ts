import { Injectable, WritableSignal, signal } from '@angular/core';
import { User } from '../../models/models';

const USER_KEY = 'current_user'

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    public user: WritableSignal<User | null> = signal<User | null>(null);

    public loadFromLocalStorage(): void {
        const storedUser = localStorage.getItem(USER_KEY)

        if (storedUser) {
            this.user.set(JSON.parse(storedUser));
        }
    }

    private saveToLocalStorage(): void {
        localStorage.setItem(USER_KEY, JSON.stringify(this.user()))
    }

    public login(user: User): void {
        this.user.set(user)
        this.saveToLocalStorage()
    }

    public logout(): void {
        this.user.set(null)
        localStorage.removeItem(USER_KEY)
    }

    public isSuperuser(): boolean {
        const currentUser = this.user();

        return currentUser ? currentUser.is_superuser : false;
    }
}
