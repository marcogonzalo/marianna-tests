import { createBrowserRouter } from 'react-router-dom';
import AssessmentPage from './pages/AssessmentPage';
import AssessmentsPage from './pages/AssessmentsPage';
import CreateAssessmentPage from './pages/CreateAssessmentPage';

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
]);

export default router;
