import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getAssessment } from '@/features/assessments/api';
import { Assessment } from '@/features/assessments/types/client';
import { Page } from '@/layouts/Page';
import AssessmentCard from '@/features/assessments/components/AssessmentCard';
import QuestionFormList from '@/features/assessments/components/QuestionFormList';
import { FormButton } from '@/components/ui';

export default function AssessmentPage() {
    const { id } = useParams<{ id: string }>();
    const [assessment, setAssessment] = useState<Assessment | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        const loadAssessment = async () => {
            try {
                if (!id) throw new Error('Assessment ID is required');
                const data = await getAssessment(parseInt(id));
                setAssessment(data);
                setError(null);
            } catch (err) {
                setError('Failed to load assessment');
                console.error('Error loading assessment:', err);
            } finally {
                setLoading(false);
            }
        };

        loadAssessment();
    }, [id]);

    const handleEditAssessment = () => {
        // Logic to edit assessment
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center">Loading assessment...</div>
                </div>
            </div>
        );
    }

    if (error || !assessment) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center text-red-600">{error}</div>
                </div>
            </div>
        );
    }

    return (
        <Page title={`Assessment: ${assessment.title}`}>
            <AssessmentCard
                assessment={assessment}
                onClick={handleEditAssessment}
            />
            <div className="questions-section mt-6">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-semibold">Questions</h3>
                    <div>
                        <FormButton
                            variant="secondary"
                            onClick={() => setIsEditing(!isEditing)}
                        >
                            {isEditing ? 'View Mode' : 'Edit Mode'}
                        </FormButton>
                    </div>
                </div>
                <QuestionFormList
                    assessmentId={assessment.id!}
                    questions={assessment.questions || []}
                    isEditing={isEditing}
                />
            </div>
        </Page>
    );
}
