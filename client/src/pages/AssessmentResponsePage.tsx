import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    getAssessment,
    getAssessmentResponse,
    updateAssessmentResponse,
} from '@/features/assessments/api';
import {
    Assessment,
    AssessmentResponse,
} from '@/features/assessments/types/client';
import { Page } from '@/layouts/Page';
import AssessmentCard from '@/features/assessments/components/AssessmentCard';
import { FormButton } from '@/components/ui';
import ChoiceList from '@/features/assessments/components/ChoiceList';

export default function AssessmentResponsePage() {
    const { id, responseId } = useParams<{
        id: string;
        responseId: string;
    }>();
    const navigate = useNavigate();
    const [assessment, setAssessment] = useState<Assessment | null>(null);
    const [response, setResponse] = useState<AssessmentResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                if (!id || !responseId)
                    throw new Error('Assessment and Response IDs are required');
                const [assessmentData, responseData] = await Promise.all([
                    getAssessment(parseInt(id)),
                    getAssessmentResponse(parseInt(responseId)),
                ]);
                setAssessment(assessmentData);
                setResponse(responseData);
                setError(null);
            } catch (err) {
                setError('Failed to load response data');
                console.error('Error loading response data:', err);
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [id, responseId]);

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center">Loading response...</div>
                </div>
            </div>
        );
    }

    if (error || !assessment || !response) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center text-red-600">{error}</div>
                </div>
            </div>
        );
    }

    const sendAssessmentResponse = async () => {
        try {
            if (!assessment || !response) return;

            const questionResponses = assessment?.questions
                ?.map((question) => {
                    const selectedValue =
                        document.querySelector<HTMLInputElement>(
                            `input[name="question-${question.id}"]:checked`,
                        )?.value;

                    return {
                        assessmentResponseId: response.id!,
                        questionId: question.id!,
                        numericValue: selectedValue
                            ? parseInt(selectedValue)
                            : 0,
                    };
                })
                .filter((qr) => qr.numericValue > 0);

            const updatedResponse = {
                questionResponses,
            };

            await updateAssessmentResponse(response.id!, updatedResponse);
            navigate(`/assessments/${id}/responses`);
        } catch (error) {
            console.error('Error submitting responses:', error);
            setError('Failed to submit responses');
        }
    };

    return (
        <Page title={`Response for: ${assessment.title}`}>
            <div className="flex justify-between items-center mb-4">
                <div className="flex-1">
                    <AssessmentCard
                        assessment={assessment}
                        onClick={() => navigate(`/assessments/${id}`)}
                    />
                </div>
                <div className="ml-4">
                    <FormButton
                        variant="secondary"
                        onClick={sendAssessmentResponse}
                    >
                        Submit Responses
                    </FormButton>
                </div>
                {/* <div className="ml-4">
                    <FormButton
                        variant="secondary"
                        onClick={() => navigate(`/assessments/${id}/responses`)}
                    >
                        Back to Responses
                    </FormButton>
                </div> */}
            </div>

            <div className="mt-8">
                <div className="bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl p-6">
                    <div className="flex justify-between items-center mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900">
                                Response Details
                            </h3>
                            <p className="mt-1 text-sm text-gray-500">
                                Status:{' '}
                                <span
                                    className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${
                                        response.status === 'completed'
                                            ? 'bg-green-50 text-green-700'
                                            : response.status === 'abandoned'
                                            ? 'bg-red-50 text-red-700'
                                            : 'bg-yellow-50 text-yellow-700'
                                    }`}
                                >
                                    {response.status}
                                </span>
                            </p>
                            {response.score !== null && (
                                <p className="mt-1 text-sm text-gray-500">
                                    Score: {response.score}
                                </p>
                            )}
                        </div>
                    </div>

                    <div className="mt-8 space-y-8">
                        {assessment.questions?.map((question) => {
                            // const questionResponse =
                            //     response.questionResponses?.find(
                            //         (qr) => qr.questionId === question.id,
                            //     );

                            return (
                                <div
                                    key={question.id}
                                    className="border-t border-gray-200 pt-6"
                                >
                                    <h4 className="text-base font-semibold text-gray-900">
                                        {question.text}
                                    </h4>
                                    <ChoiceList
                                        choices={question.choices}
                                        name={'question-' + question.id}
                                    />
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </Page>
    );
}
