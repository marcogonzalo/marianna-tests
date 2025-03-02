import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';

export default function LogoutPage() {
    const { logout } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        const performLogout = async () => {
            await logout();
            navigate('/login');
        };

        performLogout();
    }, [logout, navigate]);

    return (
        <div className="flex min-h-screen items-center justify-center">
            <p className="text-gray-500">Logging out...</p>
        </div>
    );
}
