import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
    getAssessment,
    getAssessmentResponse,
    updateAssessmentResponse,
} from '@/features/assessments/api';
import {
    Assessment,
    AssessmentResponse,
    Question,
} from '@/features/assessments/types/client';
import { Page } from '../../layouts/components/Page';
import { FormButton } from '@/components/ui';
import ChoiceList from '@/features/assessments/components/ChoiceList';
import { ResponseStatus } from '@/features/assessments/types';
import InfoBadge from '@/components/ui/InfoBadge';
import Markdown from 'react-markdown';

export default function AssessmentResponsePage() {
    const { responseId } = useParams<{
        responseId: string;
    }>();
    const [assessment, setAssessment] = useState<Assessment | null>(null);
    const [questionList, setQuestionList] = useState<Question[] | null>(null);
    const [response, setResponse] = useState<AssessmentResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isCompleted, setIsCompleted] = useState(false);

    useEffect(() => {
        const loadData = async () => {
            try {
                if (!responseId) throw new Error('Response IDs is required');
                const responseData = await getAssessmentResponse(responseId);
                setResponse(responseData);
                if (responseData.status !== ResponseStatus.PENDING)
                    throw new Error('Asessment not available');
                setError(null);
                if (!responseData.assessmentId)
                    throw new Error('Assessment IDs is required');
                const assessmentData = await getAssessment(
                    responseData.assessmentId,
                );
                setAssessment(assessmentData);
                const sortedQuestions = [...assessmentData.questions!].sort(
                    (a, b) => (a.order ?? 0) - (b.order ?? 0),
                );
                setQuestionList(sortedQuestions);
            } catch (err) {
                setError('Failed to load assessment response data');
                console.error('Error loading assessment response data:', err);
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [responseId]);

    const sendAssessmentResponse = async () => {
        try {
            if (!assessment || !response) return;

            const questionResponses = assessment?.questions?.map((question) => {
                const selectedValue = document.querySelector<HTMLInputElement>(
                    `input[name="question-${question.id}"]:checked`,
                )?.value;
                if (selectedValue === undefined)
                    throw new Error(
                        'Invalid response to question: ' + question.text,
                    );
                return {
                    assessmentResponseId: response.id,
                    questionId: question.id!,
                    numericValue: parseInt(selectedValue),
                };
            });
            const updatedResponse = {
                ...response,
                status: ResponseStatus.COMPLETED,
                questionResponses,
            };
            await updateAssessmentResponse(response.id!, updatedResponse);
            setResponse(updatedResponse);
            setIsCompleted(true);
        } catch (error) {
            console.error('Error submitting responses:', error);
            setError('Failed to submit responses: ' + error);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center">Loading response...</div>
                </div>
            </div>
        );
    }

    if (
        !response ||
        response.status !== ResponseStatus.PENDING ||
        isCompleted
    ) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div
                        className={`text-center ${
                            isCompleted ? 'text-green-600' : 'text-red-600'
                        }`}
                    >
                        The assessment is{' '}
                        {isCompleted ? 'completed' : 'not available'}.
                    </div>
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

    return (
        <Page title={assessment.title} image="https://hazelton.ie/wp-content/uploads/2024/07/15-year-anniversary-logo-2024-copy.jpeg">
            <div className="justify-between items-center">
                <div className="rounded-md p-2 bg-gray-200 p-6 text-gray-700">
                        <Markdown>{assessment.description}</Markdown>

                    <div className="flex items-start gap-2 text-sm mt-4">
                        <InfoBadge color="gray">
                            Time required:{' '}
                            {Math.ceil((assessment.questions?.length || 0) / 2)}{' '}
                            min
                        </InfoBadge>
                        <InfoBadge color="gray">
                            {assessment.questions?.length || 0} questions
                        </InfoBadge>
                    </div>
                </div>
            </div>

            <div className="mt-8 space-y-8 p-6">
                {questionList?.map((question) => {
                    if (!question.choices || question.choices.length === 0)
                        return null;

                    const choices = [...question.choices].sort(
                        (a, b) => (a.order ?? 0) - (b.order ?? 0),
                    );

                    return (
                        <div key={question.id} className="">
                            <h4 className="text-base font-semibold text-gray-900">
                                {question.text}
                            </h4>
                            <ChoiceList
                                choices={choices}
                                name={'question-' + question.id}
                            />
                        </div>
                    );
                })}
            </div>

            <div className="mt-8 text-center">
                {response.status === ResponseStatus.PENDING && (
                    <FormButton
                        variant="primary"
                        onClick={sendAssessmentResponse}
                        className='w-1/2'
                    >
                        Submit Responses
                    </FormButton>
                )}
            </div>
        </Page>
    );
}
