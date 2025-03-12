import { useNavigate } from 'react-router-dom';
import { FormButton } from '@/components/ui';
import AssessmentCard from './AssessmentCard';
import { Assessment } from '@/features/assessments/types/client';
import { updateAssessment } from '@/features/assessments/api';

interface AssessmentListProps {
    assessments: Assessment[];
    onAssessmentUpdated?: () => void;
}

export default function AssessmentList({ assessments, onAssessmentUpdated }: AssessmentListProps) {
    const navigate = useNavigate();

    const handleUpdate = async (assessment: Assessment) => {
        try {
            await updateAssessment(assessment.id!, assessment);
            onAssessmentUpdated?.();
        } catch (error) {
            console.error('Error updating assessment:', error);
        }
    };

    if (assessments.length === 0) {
        return (
            <div className="card p-12 text-center">
                <h3 className="text-lg font-medium text-gray-900">
                    No assessments found
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                    Get started by creating your first assessment.
                </p>
                <div className="mt-6">
                    <FormButton
                        variant="primary"
                        onClick={() => navigate('/assessments/create')}
                    >
                        Create Assessment
                    </FormButton>
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
                    onUpdate={handleUpdate}
                />
            ))}
        </div>
    );
}
