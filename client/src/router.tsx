import { createBrowserRouter } from 'react-router-dom';
import AssessmentPage from './pages/AssessmentPage';
import AssessmentsPage from './pages/AssessmentsPage';
import CreateAssessmentPage from './pages/CreateAssessmentPage';
import AssessmentResponsesPage from './pages/AssessmentResponsesPage';
import AssessmentResponsePage from './pages/AssessmentResponsePage';

const router = createBrowserRouter([
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
        path: '/assessments/:id/responses/:responseId',
        element: <AssessmentResponsePage />,
    },
]);

export default router;
