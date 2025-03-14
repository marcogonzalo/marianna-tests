import React, { useEffect, useState } from 'react';
import Question from './Question';
import QuestionForm from './QuestionForm';
import { Question as QuestionType } from '@/features/assessments/types';
import { FormButton } from '@/components/ui';

interface QuestionFormListProps {
    assessmentId: number;
    questions: QuestionType[];
    isEditing: boolean;
    onQuestionsChange: (questions: QuestionType[]) => void;
}

const QuestionFormList: React.FC<QuestionFormListProps> = ({
    assessmentId,
    questions,
    isEditing,
    onQuestionsChange,
}) => {
    const [localQuestions, setLocalQuestions] = useState<QuestionType[]>(questions);
    const [sortedQuestions, setSortedQuestions] = useState<QuestionType[]>(questions);

    useEffect(() => {
        setLocalQuestions(questions);
        setSortedQuestions(
            [...questions].sort((a, b) => (a.order ?? 0) - (b.order ?? 0)),
        );
    }, [questions]);

    useEffect(() => {
        setSortedQuestions(
            [...localQuestions].sort((a, b) => (a.order ?? 0) - (b.order ?? 0)),
        );
    }, [localQuestions]);

    const handleDeleteQuestion = (questionId: number) => {
        const updatedQuestions = localQuestions.filter((q) => q.id !== questionId);
        setLocalQuestions(updatedQuestions);
        onQuestionsChange(updatedQuestions);
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
        const updatedQuestions = [...localQuestions, newQuestion];
        setLocalQuestions(updatedQuestions);
        onQuestionsChange(updatedQuestions);
    };

    const handleQuestionChange = (updatedQuestion: QuestionType) => {
        // Find the original question to compare order changes
        const originalQuestion = localQuestions.find(q => q.id === updatedQuestion.id);
        // If the order changed, update all questions' orders
        if (originalQuestion && originalQuestion.order !== updatedQuestion.order) {
            const newOrder = updatedQuestion.order!;

            // Create a new array with all questions except the one being moved
            const questionsWithoutMoved = localQuestions.filter(q => q.id !== updatedQuestion.id);

            // Insert the updated question at the new position
            questionsWithoutMoved.splice(newOrder - 1, 0, updatedQuestion);

            // Update the order values to match their new positions
            const finalQuestions = questionsWithoutMoved.map((question, index) => ({
                ...question,
                order: index + 1,
            }));
            setLocalQuestions(finalQuestions);
            onQuestionsChange(finalQuestions);
        } else {
            // If only other fields changed, just update the specific question
            const updatedQuestions = localQuestions.map((question) =>
                question.id === updatedQuestion.id ? updatedQuestion : question,
            );
            setLocalQuestions(updatedQuestions);
            onQuestionsChange(updatedQuestions);
        }
    };

    return (
        <div className="flex flex-col gap-y-5">
            {sortedQuestions.map((question) =>
                isEditing ? (
                    <QuestionForm
                        key={`question-${question.id}`}
                        {...question}
                        choices={question.choices || []}
                        onDelete={handleDeleteQuestion}
                        onChange={handleQuestionChange}
                    />
                ) : (
                    <Question key={`question-${question.id}`} {...question} />
                ),
            )}
            {isEditing && (
                <FormButton onClick={handleAddQuestion}>
                    Add Question
                </FormButton>
            )}
        </div>
    );
};

export default QuestionFormList;
