import { NavBar } from './components/NavBar';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import DefaultLayout from './DefaultLayout';

export default function PrivateLayout() {
    return (
        <ProtectedRoute>
            <NavBar />
            <DefaultLayout />
        </ProtectedRoute>
    );
}
