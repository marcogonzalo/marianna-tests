import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getAssessment, bulkUpdateQuestions } from '@/features/assessments/api';
import { Assessment, Question } from '@/features/assessments/types/client';
import { Page } from '../layouts/components/Page';
import AssessmentCard from '@/features/assessments/components/AssessmentCard';
import QuestionFormList from '@/features/assessments/components/QuestionFormList';
import { FormButton } from '@/components/ui';
import DiagnosticsModal from '@/features/assessments/components/DiagnosticsModal';

export default function AssessmentPage() {
    const { id } = useParams<{ id: string }>();
    const [assessment, setAssessment] = useState<Assessment | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isEditing, setIsEditing] = useState(false);
    const [isDiagnosticsModalOpen, setIsDiagnosticsModalOpen] = useState(false);
    const [questions, setQuestions] = useState<Question[]>([]);
    const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

    useEffect(() => {
        const loadAssessment = async () => {
            try {
                if (!id) throw new Error('Assessment ID is required');
                const data = await getAssessment(parseInt(id));
                setAssessment(data);
                setQuestions(data.questions || []);
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

    const handleOpenDiagnosticsModal = () => {
        setIsDiagnosticsModalOpen(true);
    };

    const handleCloseDiagnosticsModal = () => {
        setIsDiagnosticsModalOpen(false);
    };

    const handleQuestionsChange = (updatedQuestions: Question[]) => {
        setQuestions(updatedQuestions);
        setHasUnsavedChanges(true);
    };

    const handleSaveQuestions = async () => {
        if (!assessment?.id) return;

        try {
            const updatedQuestions = questions.map((question) => ({
                ...question,
                id: question.id && question.id <= 0 ? undefined : question.id,
                choices: question.choices.map((choice) => ({
                    ...choice,
                    id: choice.id && choice.id <= 0 ? undefined : choice.id,
                })),
            }));
            const updatedQuestionsBulk = await bulkUpdateQuestions(
                assessment.id,
                updatedQuestions,
            );
            setQuestions(updatedQuestionsBulk);
            setHasUnsavedChanges(false);
            // Update the assessment state with the new questions
            setAssessment((prev) =>
                prev ? { ...prev, questions: updatedQuestions } : null,
            );
        } catch (err) {
            console.error('Error saving questions:', err);
            setError('Failed to save questions');
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
        <Page title={`Assessment: ${assessment.title}`}>
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">{assessment.title}</h2>
                <div className="flex space-x-2">
                    <FormButton
                        variant="secondary"
                        onClick={handleOpenDiagnosticsModal}
                    >
                        Manage Diagnostics
                    </FormButton>
                </div>
            </div>

            <AssessmentCard
                assessment={assessment}
                onClick={handleEditAssessment}
            />
            <div className="questions-section mt-6">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-semibold">Questions</h3>
                    <div className="flex space-x-2">
                        {isEditing && hasUnsavedChanges && (
                            <FormButton
                                variant="primary"
                                onClick={handleSaveQuestions}
                            >
                                Save Changes
                            </FormButton>
                        )}
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
                    questions={questions}
                    isEditing={isEditing}
                    onQuestionsChange={handleQuestionsChange}
                />
            </div>

            {assessment.id && (
                <DiagnosticsModal
                    isOpen={isDiagnosticsModalOpen}
                    onClose={handleCloseDiagnosticsModal}
                    assessmentId={assessment.id}
                />
            )}
        </Page>
    );
}
