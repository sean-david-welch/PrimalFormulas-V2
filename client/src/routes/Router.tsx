import Loading from '../layouts/Loading';

import { Suspense, lazy, useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Route, Routes, useLocation, Navigate } from 'react-router-dom';

const AppRoutes = () => {
    const ScrollToTopPage = () => {
        const { pathname } = useLocation();

        useEffect(() => {
            window.scrollTo(0, 0);
        }, [pathname]);

        return null;
    };

    return (
        <Router>
            <Suspense fallback={<Loading />}>
                <ScrollToTopPage />
                <Routes>
                    <div>
                        <h1>hi</h1>
                    </div>
                </Routes>
            </Suspense>
        </Router>
    );
};
