import styles from './styles/App.module.css';

import AppRoutes from './routes/Router';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import useFirebaseAuthSync from './hooks/authHooks';

function App() {
	useFirebaseAuthSync();
	const queryClient = new QueryClient();

	return (
		<QueryClientProvider client={queryClient}>
			<div className={styles.App}>
				<AppRoutes />
			</div>
		</QueryClientProvider>
	);
}

export default App;
