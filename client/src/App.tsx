import { RouterProvider } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import router from './router';

export default function App() {
    return (
        <div className="min-h-full">
            <AuthProvider>
                <RouterProvider router={router} />
            </AuthProvider>
        </div>
    );
}
