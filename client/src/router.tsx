import { createBrowserRouter } from 'react-router-dom';
import AssessmentPage from './pages/AssessmentPage';
import AssessmentsPage from './pages/AssessmentsPage';
import CreateAssessmentPage from './pages/CreateAssessmentPage';
import AssessmentResponsesPage from './pages/AssessmentResponsesPage';
import AssessmentResponsePage from './pages/AssessmentResponsePage';
import UsersPage from './pages/UsersPage';
import ExamineesPage from './pages/ExamineesPage';
import ExamineePage from './pages/ExamineePage';
import PublicAssessmentResponsePage from './pages/public/PublicAssessmentResponsePage';
import PrivateLayout from './layouts/PrivateLayout';
import PublicLayout from './layouts/PublicLayout';
import LoginPage from './pages/public/LoginPage';
import LogoutPage from './pages/public/LogoutPage';

const router = createBrowserRouter([
    {
        element: <PrivateLayout />,
        children: [
            {
                path: '/',
                element: <AssessmentsPage />,
            },
            {
                path: '/assessments/:id',
                element: <AssessmentPage />,
            },
            {
                path: '/assessments',
                element: <AssessmentsPage />,
            },
            {
                path: '/assessments/create',
                element: <CreateAssessmentPage />,
            },
            {
                path: '/assessments/:id/responses',
                element: <AssessmentResponsesPage />,
            },
            {
                path: '/responses/:responseId',
                element: <AssessmentResponsePage />,
            },
            {
                path: '/users',
                element: <UsersPage />,
            },
            {
                path: '/examinees/:id',
                element: <ExamineePage />,
            },
            {
                path: '/examinees',
                element: <ExamineesPage />,
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
                path: '/private-response/:responseId',
                element: <PublicAssessmentResponsePage />,
            },
            {
                path: '/logout',
                element: <LogoutPage />,
            },
        ],
    },
]);

export default router;
