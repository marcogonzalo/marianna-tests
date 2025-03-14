import { createBrowserRouter } from 'react-router-dom';
import ProtectedRoute from '@/components/ProtectedRoute';
import PrivateLayout from './layouts/PrivateLayout';
import PublicLayout from './layouts/PublicLayout';
import AssessmentPage from './pages/AssessmentPage';
import AssessmentsPage from './pages/AssessmentsPage';
import CreateAssessmentPage from './pages/CreateAssessmentPage';
import AssessmentResponsesPage from './pages/AssessmentResponsesPage';
import AssessmentResponsePage from './pages/AssessmentResponsePage';
import UsersPage from './pages/UsersPage';
import ExamineesPage from './pages/ExamineesPage';
import ExamineePage from './pages/ExamineePage';
import PublicAssessmentResponsePage from './pages/public/PublicAssessmentResponsePage';
import LoginPage from './pages/public/LoginPage';
import LogoutPage from './pages/public/LogoutPage';
import ForgotPasswordPage from './pages/public/ForgotPasswordPage';
import ResetPasswordPage from './pages/public/ResetPasswordPage';
import { UserRole } from './features/users/types/shared';

const allRoles = Object.keys(UserRole).map(
    (role) => UserRole[role as keyof typeof UserRole],
);
const router = createBrowserRouter([
    {
        element: <PrivateLayout />,
        children: [
            {
                path: '/',
                element: (
                    <ProtectedRoute
                        allowedRoles={allRoles}
                    >
                        <AssessmentsPage />
                    </ProtectedRoute>
                ),
            },
            {
                path: '/assessments/:id',
                element: (
                    <ProtectedRoute
                        allowedRoles={allRoles}
                    >
                        <AssessmentPage />
                    </ProtectedRoute>
                ),
            },
            {
                path: '/assessments',
                element: (
                    <ProtectedRoute
                        allowedRoles={allRoles}
                    >
                        <AssessmentsPage />
                    </ProtectedRoute>
                ),
            },
            {
                path: '/assessments/create',
                element: (
                    <ProtectedRoute
                        allowedRoles={[
                            UserRole.ADMIN,
                            
                        ]}
                    >
                        <CreateAssessmentPage />
                    </ProtectedRoute>
                ),
            },
            {
                path: '/assessments/:id/responses',
                element: (
                    <ProtectedRoute
                        allowedRoles={allRoles}
                    >
                        <AssessmentResponsesPage />
                    </ProtectedRoute>
                ),
            },
            {
                path: '/responses/:responseId',
                element: (
                    <ProtectedRoute allowedRoles={allRoles}>
                        <AssessmentResponsePage />
                    </ProtectedRoute>
                ),
            },
            {
                path: '/users',
                element: (
                    <ProtectedRoute allowedRoles={allRoles}>
                        <UsersPage />
                    </ProtectedRoute>
                ),
            },
            {
                path: '/examinees/:id',
                element: (
                    <ProtectedRoute allowedRoles={allRoles}>
                        <ExamineePage />
                    </ProtectedRoute>
                ),
            },
            {
                path: '/examinees',
                element: (
                    <ProtectedRoute allowedRoles={allRoles}>
                        <ExamineesPage />
                    </ProtectedRoute>
                ),
            },
        ],
    },
    {
        element: <PublicLayout />,
        children: [
            {
                path: '/login',
                element: <LoginPage />,
            },
            {
                path: '/public/726573706f6e7365/:responseId/70726976617465',
                element: <PublicAssessmentResponsePage />,
            },
            {
                path: '/logout',
                element: (
                    <ProtectedRoute allowedRoles={allRoles}>
                        <LogoutPage />
                    </ProtectedRoute>
                ),
            },
            {
                path: '/forgot-password',
                element: <ForgotPasswordPage />,
            },
            {
                path: '/reset-password',
                element: <ResetPasswordPage />,
            },
        ],
    },
]);

export default router;
