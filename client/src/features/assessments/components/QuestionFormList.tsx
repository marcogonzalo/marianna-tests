import React, { useEffect, useState } from 'react';
import Question from './Question';
import QuestionForm from './QuestionForm';
import { Question as QuestionType } from '@/features/assessments/types';
import { FormButton } from '@/components/ui';
import {
    createQuestion,
    getAssessment,
    updateQuestion,
    deleteQuestion,
} from '@/features/assessments/api'; // Import the API handler

interface QuestionFormListProps {
    assessmentId: number;
    questions: QuestionType[];
    isEditing: boolean;
}

const QuestionFormList: React.FC<QuestionFormListProps> = ({
    assessmentId,
    questions,
    isEditing,
}) => {
    const [localQuestions, setLocalQuestions] =
        useState<QuestionType[]>(questions);
    const [sortedQuestions, setSortedQuestions] =
        useState<QuestionType[]>(questions);

    useEffect(() => {
        setSortedQuestions(
            [...localQuestions].sort((a, b) => (a.order ?? 0) - (b.order ?? 0)),
        );
    }, [localQuestions]);

    const handleSaveQuestion = async (question: QuestionType) => {
        try {
            if (question.id && question.id <= 0) question.id = undefined;
            // Add your API call here to save the question
            if (question.id) {
                await updateQuestion(question);
            } else {
                await createQuestion(question);
            }
            // Optionally refresh the assessment data after saving
            const updatedAssessment = await getAssessment(assessmentId);
            setLocalQuestions(updatedAssessment.questions ?? []);
        } catch (error) {
            console.error('Error saving question:', error);
        }
    };

    const handleDeleteQuestion = async (questionId: number) => {
        try {
            if (questionId > 0) await deleteQuestion(assessmentId, questionId);
            setLocalQuestions(
                localQuestions.filter((q) => q.id !== questionId),
            );
        } catch (error) {
            console.error('Error deleting question:', error);
        }
    };

    const handleAddQuestion = () => {
        const newQuestion: QuestionType = {
            id: -Date.now(), // Temporary ID, replace with actual ID from backend
            assessmentId,
            text: '',
            order:
                Number(
                    sortedQuestions[sortedQuestions.length - 1]?.order || 0,
                ) + 1,
            choices: [],
        };
        setLocalQuestions([...localQuestions, newQuestion]);
    };

    const handleQuestionChange = (updatedQuestion: QuestionType) => {
        setLocalQuestions((prevQuestions) =>
            prevQuestions.map((question) =>
                question.id === updatedQuestion.id ? updatedQuestion : question,
            ),
        );
    };

    return (
        <div className="flex flex-col gap-y-5">
            {isEditing && (
                <FormButton onClick={handleAddQuestion}>
                    Add Question
                </FormButton>
            )}
            {sortedQuestions.map((question, index) =>
                isEditing ? (
                    <QuestionForm
                        key={`question-${question.id}`}
                        {...question}
                        order={index + 1}
                        onSave={handleSaveQuestion}
                        onDelete={handleDeleteQuestion}
                        onChange={handleQuestionChange}
                    />
                ) : (
                    <Question key={`question-${question.id}`} {...question} />
                ),
            )}
        </div>
    );
};

export default QuestionFormList;
