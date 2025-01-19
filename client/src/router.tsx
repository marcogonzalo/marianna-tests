import { createBrowserRouter } from 'react-router-dom';
import AssessmentsPage from './pages/AssessmentsPage';
import CreateAssessmentPage from './pages/CreateAssessmentPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AssessmentsPage />,
  },
  {
    path: '/assessments',
    element: <AssessmentsPage />,
  },
  {
    path: '/assessments/create',
    element: <CreateAssessmentPage />,
  }
]);