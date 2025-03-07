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

            const questionResponses = assessment?.questions
                ?.map((question) => {
                    const selectedValue =
                        document.querySelector<HTMLInputElement>(
                            `input[name="question-${question.id}"]:checked`,
                        )?.value;

                    if (!selectedValue)
                        throw new Error(
                            'Invalid response to question: ' + question.text,
                        );
                    return {
                        assessmentResponseId: response.id,
                        questionId: question.id!,
                        numericValue: selectedValue
                            ? parseInt(selectedValue)
                            : 0,
                    };
                })
                .filter((qr) => !!qr.numericValue);
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
        <Page title={`Response for: ${assessment.title}`}>
            <div className="flex justify-between items-center mb-4">
                <div className="flex-1">
                    <div className="card p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                            {assessment.title}
                        </h3>
                        <p className="text-gray-500 line-clamp-2 mb-4">
                            {assessment.description}
                        </p>

                        <div className="flex items-start gap-2 text-sm">
                            <InfoBadge color="gray">
                                Time required:{' '}
                                {Math.ceil(
                                    (assessment.questions?.length || 0) / 2,
                                )}{' '}
                                min
                            </InfoBadge>
                            <InfoBadge color="gray">
                                {assessment.questions?.length || 0} questions
                            </InfoBadge>
                        </div>
                    </div>
                </div>
                <div className="ml-4">
                    {response.status === ResponseStatus.PENDING && (
                        <FormButton
                            variant="primary"
                            onClick={sendAssessmentResponse}
                        >
                            Submit Responses
                        </FormButton>
                    )}
                </div>
            </div>

            <div className="mt-8">
                <div className="">
                    <div className="flex justify-between items-center mb-6">
                        <div>
                            {response.score !== null && (
                                <p className="mt-1 text-sm text-gray-500">
                                    Score: {response.score}
                                </p>
                            )}
                        </div>
                    </div>

                    <div className="mt-8 space-y-8">
                        {questionList?.map((question) => {
                            if (
                                !question.choices ||
                                question.choices.length === 0
                            )
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
                </div>
            </div>
        </Page>
    );
}
