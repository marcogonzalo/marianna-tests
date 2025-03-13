import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    getAssessment,
    getAssessmentResponse,
    getDiagnostics,
} from '@/features/assessments/api';
import {
    Assessment,
    AssessmentResponse,
    Diagnostic,
    Question,
} from '@/features/assessments/types/client';
import { Page } from '../layouts/components/Page';
import AssessmentCard from '@/features/assessments/components/AssessmentCard';
import { FormButton } from '@/components/ui';
import ChoiceList from '@/features/assessments/components/ChoiceList';
import { ResponseStatus } from '@/features/assessments/types';
import DiagnosticSummary from '../features/assessments/components/DiagnosticSummary';
import { getExaminee } from '@/features/examinees/api';
import { Examinee } from '@/features/examinees/types';

export default function AssessmentResponsePage() {
    const { responseId } = useParams<{
        responseId: string;
    }>();
    const navigate = useNavigate();
    const [assessment, setAssessment] = useState<Assessment | null>(null);
    const [questionList, setQuestionList] = useState<Question[] | null>(null);
    const [response, setResponse] = useState<AssessmentResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [matchingDiagnostic, setMatchingDiagnostic] =
        useState<Diagnostic | null>(null);
    const [examinee, setExaminee] = useState<Examinee | null>(null);
    const isViewable = (response: AssessmentResponse): boolean =>
        response.status === ResponseStatus.PENDING ||
        response.status === ResponseStatus.COMPLETED;

    useEffect(() => {
        const loadData = async () => {
            try {
                if (!responseId) throw new Error('Response IDs is required');

                const responseData = await getAssessmentResponse(responseId);
                setResponse(responseData);
                setError(null);

                if (!responseData.assessmentId)
                    throw new Error('Assessment IDs is required');
                const assessmentData = await getAssessment(
                    responseData.assessmentId,
                );
                setAssessment(assessmentData);

                const examineeData = await getExaminee(responseData.examineeId);
                setExaminee(examineeData);

                // Load diagnostics if response is completed and has a score
                if (
                    responseData.status === ResponseStatus.COMPLETED &&
                    responseData.score !== undefined &&
                    assessmentData.id
                ) {
                    const sortedQuestions = [...assessmentData.questions!].sort(
                        (a, b) => (a.order ?? 0) - (b.order ?? 0),
                    );
                    setQuestionList(sortedQuestions);
                    const diagnosticsData = await getDiagnostics(
                        assessmentData.id,
                    );
                    const score = responseData.score;
                    const matching = diagnosticsData.find(
                        (d) =>
                            (d.minValue === undefined ||
                                d.minValue === null ||
                                score >= d.minValue) &&
                            (d.maxValue === undefined ||
                                d.maxValue === null ||
                                score <= d.maxValue),
                    );
                    setMatchingDiagnostic(matching || null);
                }
            } catch (err) {
                setError('Failed to load assessment response data');
                console.error('Error loading assessment response data:', err);
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [responseId]);

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

    return (
        <Page
            title={`Examinee: ${examinee?.firstName} ${examinee?.lastName}`}
        >
            <div className="flex justify-between items-center">
                <div className="flex-1">
                    <AssessmentCard
                        assessment={assessment}
                        onClick={() =>
                            navigate(`/assessments/${assessment.id}`)
                        }
                    />
                </div>
                <div className="ml-4">
                    <FormButton
                        variant="primary"
                        onClick={() =>
                            navigate(`/examinees/${response.examineeId}`)
                        }
                    >
                        Back to Examinee
                    </FormButton>
                </div>
            </div>

            <div className="mt-4">
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

                            <p className="text-sm font-semibold text-gray-900 mt-2">
                                Score obtanied: {response.score}
                            </p>
                        </div>
                    </div>
                    {matchingDiagnostic && (
                        <DiagnosticSummary
                            score={response.score ?? null}
                            diagnostic={matchingDiagnostic}
                        />
                    )}
                    <div className="mt-8 space-y-8">
                        {isViewable(response) &&
                            questionList?.map((question) => {
                                if (
                                    !question.choices ||
                                    question.choices.length === 0
                                )
                                    return null;

                                const choices = [...question.choices].sort(
                                    (a, b) => (a.order ?? 0) - (b.order ?? 0),
                                );
                                return (
                                    <div
                                        key={question.id}
                                        className="border-t border-gray-200 pt-6"
                                    >
                                        <h4 className="text-base font-semibold text-gray-900">
                                            {question.text}
                                        </h4>
                                        <ChoiceList
                                            choices={choices}
                                            name={'question-' + question.id}
                                            showDisabled
                                            response={
                                                response.questionResponses?.find(
                                                    (qr) =>
                                                        qr.questionId ===
                                                        question.id,
                                                )?.numericValue
                                            }
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
