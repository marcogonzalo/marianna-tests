import { FormButton, FormInput } from '@/components/ui';
import { Question, Choice } from '../types/client';
import { useState, useRef } from 'react';
import { createQuestion, updateQuestion } from '../api'; // Import the API handlers
import ChoiceFormList, { ChoiceFormListRef } from './ChoiceFormList'; // Import ChoiceFormList

interface QuestionFormProps extends Question {
    onSave?: (question: Question) => void;
}

export default function QuestionForm({
    onSave,
    ...question
}: QuestionFormProps) {
    const [text, setText] = useState(question.text);
    const [order, setOrder] = useState(question.order || 0);
    const [choices, setChoices] = useState<Choice[]>(question.choices || []);
    const choiceListRef = useRef<ChoiceFormListRef>(null);
    const isChanged =
        text !== question.text ||
        order !== question.order ||
        JSON.stringify(choices) !== JSON.stringify(question.choices);

    console.log(choices, question.choices);
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!text.trim()) {
            alert('Question text is required');
            return;
        }

        if (!choiceListRef.current?.validateChoices()) {
            return;
        }

        const currentChoices = choiceListRef.current?.getChoices() || [];
        const updatedQuestion = {
            ...question,
            text,
            order,
            choices: currentChoices,
        };

        try {
            if (question.id) {
                await updateQuestion(updatedQuestion);
            } else {
                await createQuestion(updatedQuestion);
            }
            if (onSave) onSave(updatedQuestion);
        } catch (error) {
            console.error('Error saving question:', error);
        }
    };

    const handleSaveChoice = (updatedChoice: Choice) => {
        setChoices((prevChoices) => {
            const index = prevChoices.findIndex(
                (choice) => choice.id === updatedChoice.id,
            );
            if (index !== -1) {
                const newChoices = [...prevChoices];
                newChoices[index] = updatedChoice;
                return newChoices;
            }
            return [...prevChoices, updatedChoice];
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-8 gap-4">
                <FormInput
                    label="Question Text"
                    id="questionText"
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    blockClassName="col-span-6"
                />
                <FormInput
                    label="Order"
                    type="number"
                    value={order}
                    onChange={(e) => setOrder(Number(e.target.value))}
                />
                <FormButton
                    type="submit"
                    variant="secondary"
                    className="self-end"
                    disabled={!isChanged}
                >
                    Save
                </FormButton>
            </div>
            <ChoiceFormList
                ref={choiceListRef}
                choices={choices}
                onSaveChoice={handleSaveChoice}
            />
        </form>
    );
}
