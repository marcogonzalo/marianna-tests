import { useNavigate } from 'react-router-dom';
import Button from '../../../components/ui/Button';
import AssessmentCard from './AssessmentCard';
import { Assessment } from '../../assessments/types';

interface AssessmentListProps {
  assessments: Assessment[];
}

export default function AssessmentList({ assessments }: AssessmentListProps) {
  const navigate = useNavigate();

  if (assessments.length === 0) {
    return (
      <div className="card p-12 text-center">
        <h3 className="text-lg font-medium text-gray-900">No assessments found</h3>
        <p className="mt-2 text-sm text-gray-500">Get started by creating your first assessment.</p>
        <div className="mt-6">
          <Button variant="primary" onClick={() => navigate('/assessments/create')}>
            Create Assessment
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {assessments.map((assessment) => (
        <AssessmentCard
          key={assessment.id}
          assessment={assessment}
          onClick={() => navigate(`/assessments/${assessment.id}`)}
        />
      ))}
    </div>
  );
} 