import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AssessmentList from '@/features/assessments/components/AssessmentList';
import { Assessment } from '@/features/assessments/types';
import { getAssessments } from '@/features/assessments/api';
import { FormButton } from '@/components/ui';
import { Page } from '@/layouts/Page';

export default function AssessmentsPage() {
    const navigate = useNavigate();
    const [assessments, setAssessments] = useState<Assessment[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadAssessments = async () => {
            try {
                const data = await getAssessments();
                setAssessments(data);
                setError(null);
            } catch (err) {
                setError('Failed to load assessments');
                console.error('Error loading assessments:', err);
            } finally {
                setLoading(false);
            }
        };

        loadAssessments();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center">Loading assessments...</div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center text-red-600">{error}</div>
                </div>
            </div>
        );
    }

    return (
        <Page title="Assessments">
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center mb-8">
                        <div>
                            <p className="mt-1 text-sm text-gray-500">
                                Manage and create assessments for your
                                organization.
                            </p>
                        </div>
                        <FormButton
                            variant="primary"
                            onClick={() => navigate('/assessments/create')}
                        >
                            Create Assessment
                        </FormButton>
                    </div>

                    <AssessmentList assessments={assessments} />
                </div>
            </div>
        </Page>
    );
}
