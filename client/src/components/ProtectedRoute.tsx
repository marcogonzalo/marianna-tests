import { Navigate, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { useEffect, useState } from 'react';
import { UserRole } from '@/features/users/types/shared';
export default function ProtectedRoute({ children, allowedRoles }: { children: React.ReactNode, allowedRoles: UserRole[] }) {
    const { token, user: currentUser } = useAuth();
    const location = useLocation();
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const navigate = useNavigate();


    useEffect(() => {  
        if (!allowedRoles.includes(currentUser?.account?.role as UserRole)) {
            navigate(-1);
        }
        setIsLoading(false);
    }, [token, currentUser, allowedRoles]);

    if (isLoading) return <></>;

    if (!token) {
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return children;
}
