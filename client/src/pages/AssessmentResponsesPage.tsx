import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    createAssessmentResponse,
    getAssessment,
    getAssessmentResponses,
} from '@/features/assessments/api';
import {
    Assessment,
    AssessmentResponse,
} from '@/features/assessments/types/client';
import { Page } from '../layouts/components/Page';
import AssessmentCard from '@/features/assessments/components/AssessmentCard';
import { FormButton } from '@/components/ui';

export default function AssessmentResponsesPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [assessment, setAssessment] = useState<Assessment | null>(null);
    const [responses, setResponses] = useState<AssessmentResponse[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                if (!id) throw new Error('Assessment ID is required');
                const [assessmentData, responsesData] = await Promise.all([
                    getAssessment(parseInt(id)),
                    getAssessmentResponses(id),
                ]);
                setAssessment(assessmentData);
                setResponses(responsesData);
                setError(null);
            } catch (err) {
                setError('Failed to load assessment data');
                console.error('Error loading assessment data:', err);
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [id]);

    const handleStartNewResponse = async () => {
        try {
            if (!id) return;
            const response = await createAssessmentResponse(parseInt(id), {
                examineeId: '1',
            });
            navigate(`/assessments/${id}/responses/${response.id}`);
        } catch (error) {
            console.error('Error creating response:', error);
        }
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
        <Page title={`Responses for: ${assessment.title}`}>
            <AssessmentCard
                assessment={assessment}
                onClick={() => navigate(`/assessments/${id}`)}
            />

            <div className="mt-8">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-semibold">Responses</h3>
                    <FormButton
                        variant="primary"
                        onClick={handleStartNewResponse}
                    >
                        Start New Response
                    </FormButton>
                </div>

                <div className="bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl">
                    <table className="min-w-full divide-y divide-gray-300">
                        <thead>
                            <tr>
                                <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                                    ID
                                </th>
                                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                    Status
                                </th>
                                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                    Score
                                </th>
                                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                    Date
                                </th>
                                <th className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                                    <span className="sr-only">Actions</span>
                                </th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {responses.map((response) => (
                                <tr
                                    key={response.id}
                                    className="hover:bg-gray-50 cursor-pointer"
                                    onClick={() =>
                                        navigate(
                                            `/assessments/${id}/responses/${response.id}`,
                                        )
                                    }
                                >
                                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                        {response.id}
                                    </td>
                                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                        <span
                                            className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${
                                                response.status === 'completed'
                                                    ? 'bg-green-50 text-green-700 ring-1 ring-inset ring-green-600/20'
                                                    : response.status ===
                                                      'abandoned'
                                                    ? 'bg-red-50 text-red-700 ring-1 ring-inset ring-red-600/20'
                                                    : 'bg-yellow-50 text-yellow-700 ring-1 ring-inset ring-yellow-600/20'
                                            }`}
                                        >
                                            {response.status}
                                        </span>
                                    </td>
                                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                        {response.score ?? '-'}
                                    </td>
                                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                        {new Date(
                                            response.createdAt!,
                                        ).toLocaleDateString()}
                                    </td>
                                    <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                        <FormButton
                                            variant="link"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                navigate(
                                                    `/assessments/${id}/responses/${response.id}`,
                                                );
                                            }}
                                        >
                                            View
                                        </FormButton>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </Page>
    );
}
