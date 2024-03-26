import { app } from './firebase';
import { getAuth, signOut, signInWithEmailAndPassword, browserSessionPersistence } from 'firebase/auth';
import { useUserStore } from './store';

export const auth = getAuth(app);

export const signInUser = async (email: string, password: string): Promise<string | undefined> => {
    auth.setPersistence(browserSessionPersistence);

    const setUserStore = useUserStore.getState();

    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);

        const idToken = await userCredential.user.getIdToken();

        const customClaim = (await userCredential.user.getIdTokenResult()).claims;
        const isAdmin = typeof customClaim.admin === 'boolean' ? customClaim.admin : false;

        setUserStore.setIsAdmin(isAdmin);
        setUserStore.setIsAuthenticated(true);

        return idToken;
    } catch (error) {
        console.error('Error signing in:', error);
    }
};

export const signOutUser = async (): Promise<void> => {
    const setUserStore = useUserStore.getState();

    try {
        await signOut(auth);
        setUserStore.setIsAdmin(false);
        setUserStore.setIsAuthenticated(false);
    } catch (error) {
        console.error('Error signing out:', error);
    }
};
