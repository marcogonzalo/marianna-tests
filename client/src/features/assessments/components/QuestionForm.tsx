import { FormButton, FormInput } from '@/components/ui';
import { Question, Choice } from '../types/client';
import { useState, useRef, useEffect } from 'react';
import ChoiceFormList, { ChoiceFormListRef } from './ChoiceFormList';
import { TrashIcon } from '@heroicons/react/20/solid';

interface QuestionFormProps extends Question {
    onDelete?: (questionId: number) => void;
    onChange: (updatedQuestion: Question) => void;
}

export default function QuestionForm({
    onDelete,
    onChange,
    ...question
}: QuestionFormProps) {
    const [text, setText] = useState(question.text);
    const [order, setOrder] = useState(question.order || 0);
    const [choices, setChoices] = useState<Choice[]>(question.choices || []);
    const choiceListRef = useRef<ChoiceFormListRef>(null);

    useEffect(() => {
        setText(question.text);
        setOrder(question.order || 0);
        setChoices(question.choices || []);
    }, [question.text, question.order, question.choices]);

    const handleChange = (field: keyof Question, newValue: string | number) => {
        const updatedQuestion = {
            ...question,
            [field]: field === 'text' ? newValue : Number(newValue),
            choices: choices,
        };
        onChange(updatedQuestion);
    };

    const handleChoiceChange = (updatedChoice: Choice) => {
        const newChoices = choices.map((choice) =>
            choice.id === updatedChoice.id ? updatedChoice : choice,
        );
        if (!newChoices.find((choice) => choice.id === updatedChoice.id)) {
            newChoices.push(updatedChoice);
        }
        setChoices(newChoices);
        onChange({
            ...question,
            choices: newChoices,
        });
    };

    const handleChoiceDelete = (choiceId: number | undefined) => {
        const newChoices = choices.filter((choice) => choice.id !== choiceId);
        setChoices(newChoices);
        onChange({
            ...question,
            choices: newChoices,
        });
    };

    return (
        <div className="space-y-4">
            <div className="grid grid-cols-8 gap-4">
                <FormInput
                    label="Question Text"
                    id="questionText"
                    type="text"
                    value={text}
                    onChange={(e) => {
                        setText(e.target.value);
                        handleChange('text', e.target.value);
                    }}
                    blockClassName="col-span-6"
                />
                <FormInput
                    label="Order"
                    type="number"
                    value={order}
                    onChange={(e) => {
                        setOrder(Number(e.target.value));
                        handleChange('order', Number(e.target.value));
                    }}
                />
                <div className="flex items-end">
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
                onChange={handleChoiceChange}
                onDelete={handleChoiceDelete}
            />
        </div>
    );
}
