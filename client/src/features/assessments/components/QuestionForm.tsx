import { FormButton, FormInput } from '@/components/ui';
import { Question, Choice } from '../types/client';
import { useState, useRef, useEffect } from 'react';
import ChoiceFormList, { ChoiceFormListRef } from './ChoiceFormList'; // Import ChoiceFormList
import { DocumentCheckIcon, TrashIcon } from '@heroicons/react/20/solid';

interface QuestionFormProps extends Question {
    onSave?: (question: Question) => void;
    onDelete?: (questionId: number) => void; // Add this line
}

export default function QuestionForm({
    onSave,
    onDelete, // Add this line
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

    useEffect(() => {
        setChoices(question.choices || []);
    }, [question.choices]);

    const handleSubmit = async (e: React.FormEvent) => {
        console.log('handleSubmit:', e.target);
        e.preventDefault();
        if (!text.trim()) {
            alert('Question text is required');
            return;
        }

        if (!choiceListRef.current?.validateChoices()) {
            return;
        }

        const currentChoices = choiceListRef.current?.getChoices() || [];
        currentChoices.forEach((choice: Choice) => {
            if (choice.id && choice.id <= 0) choice.id = undefined;
        });
        const updatedQuestion = {
            ...question,
            text,
            order,
            choices: currentChoices,
        };

        try {
            if (onSave) {
                await onSave(updatedQuestion);
                // // Update local choices state with the current choices after save
                // setChoices(currentChoices);
            }
        } catch (error) {
            console.error('Error saving question:', error);
        }
    };

    const handleSaveChoice = (updatedChoice: Choice) => {
        const newChoices = choices.map((choice) =>
            choice.id === updatedChoice.id ? updatedChoice : choice,
        );
        if (!newChoices.find((choice) => choice.id === updatedChoice.id)) {
            newChoices.push(updatedChoice);
        }
        setChoices(newChoices);
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
                <div className="flex items-end">
                    <FormButton
                        type="submit"
                        variant="secondary"
                        className="self-end"
                        disabled={!isChanged}
                    >
                        <DocumentCheckIcon className="h-5 w-5" />
                    </FormButton>
                    {question.id && onDelete && (
                        <FormButton
                            type="button"
                            variant="danger"
                            className="self-end"
                            onClick={() => onDelete(question.id!)}
                        >
                            <TrashIcon className="h-5 w-5" />
                        </FormButton>
                    )}
                </div>
            </div>
            <ChoiceFormList
                ref={choiceListRef}
                choices={choices}
                onSaveChoice={handleSaveChoice}
            />
        </form>
    );
}
