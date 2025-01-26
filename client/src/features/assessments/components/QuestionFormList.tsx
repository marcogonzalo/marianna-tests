import React, { useState } from 'react';
import Question from './Question';
import QuestionForm from './QuestionForm';
import { Question as QuestionType } from '../types';
import { FormButton } from '@/components/ui';

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

    const sortedQuestions = [...localQuestions].sort(
        (a, b) => (a.order ?? 0) - (b.order ?? 0),
    );

    const handleSaveQuestion = async (question: QuestionType) => {
        try {
            // Add your API call here to save the question
            console.log('Saving question:', question);
            // Optionally refresh the assessment data after saving
        } catch (error) {
            console.error('Error saving question:', error);
        }
    };

    const handleAddQuestion = () => {
        const newQuestion: QuestionType = {
            id: Date.now(), // Temporary ID, replace with actual ID from backend
            assessmentId,
            text: '',
            order: localQuestions.length + 1,
        };
        setLocalQuestions([...localQuestions, newQuestion]);
    };

    return (
        <div>
            {isEditing && (
                <FormButton onClick={handleAddQuestion}>
                    Add Question
                </FormButton>
            )}
            {sortedQuestions.map((question) =>
                isEditing ? (
                    <QuestionForm
                        key={question.id}
                        {...question}
                        onSave={handleSaveQuestion}
                    />
                ) : (
                    <Question key={question.id} {...question} />
                ),
            )}
        </div>
    );
};

export default QuestionFormList;
