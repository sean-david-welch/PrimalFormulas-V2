import { create } from 'zustand';

interface UserState {
    isAdmin: boolean;
    setIsAdmin: (isAdmin: boolean) => void;

    isAuthenticated: boolean;
    setIsAuthenticated: (isAuthenticated: boolean) => void;
}

export const useUserStore = create<UserState>()(set => ({
    isAdmin: false,
    setIsAdmin: (isAdmin: boolean) => set({ isAdmin }),

    isAuthenticated: false,
    setIsAuthenticated: (isAuthenticated: boolean) => set({ isAuthenticated }),
}));
