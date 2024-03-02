import { useEffect } from 'react';

import { auth } from '../lib/auth';
import { useUserStore } from '../lib/store';

const useFirebaseAuthSync = () => {
    const { setIsAuthenticated, setIsAdmin } = useUserStore();

    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged(async user => {
            if (user) {
                setIsAuthenticated(true);

                const customClaim = (await user.getIdTokenResult()).claims;
                const isAdmin = typeof customClaim.admin === 'boolean' ? customClaim.admin : false;

                setIsAdmin(isAdmin);
            } else {
                setIsAuthenticated(false);
                setIsAdmin(false);
            }
        });

        return () => unsubscribe();
    }, [setIsAdmin, setIsAuthenticated]);
};

export default useFirebaseAuthSync;
