import React, { useState, forwardRef, useImperativeHandle } from 'react';
import { Choice } from '@/features/assessments/types';
import { FormButton, FormInput } from '@/components/ui';

const ChoiceForm: React.FC<
    Choice & {
        onChange: (updatedChoice: Choice) => void;
        onDelete: () => void;
    }
> = ({ onChange, onDelete, ...choice }) => {
    const [text, setText] = useState(choice.text);
    const [order, setOrder] = useState(choice.order || 0);
    const [value, setValue] = useState(choice.value?.toString() || '');

    const handleChange = (field: keyof Choice, newValue: string | number) => {
        const updatedChoice = {
            ...choice,
            [field]: newValue,
            text,
            order,
            value: field === 'value' ? Number(newValue) : Number(value),
        };
        onChange(updatedChoice);
    };

    return (
        <form className="space-y-4">
            <div className="grid grid-cols-10 gap-4">
                <FormInput
                    label="Choice Text"
                    id="choiceText"
                    type="text"
                    value={text}
                    onChange={(e) => {
                        setText(e.target.value);
                        handleChange('text', e.target.value);
                    }}
                    blockClassName="col-span-5 col-start-2"
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
                <FormInput
                    label="Value"
                    type="text"
                    value={value}
                    onChange={(e) => {
                        setValue(e.target.value);
                        handleChange('value', e.target.value);
                    }}
                />
                <FormButton
                    variant="text"
                    onClick={onDelete}
                    className="self-end mb-1 text-red-500 hover:text-red-700"
                >
                    X
                </FormButton>
            </div>
        </form>
    );
};

interface ChoiceFormListProps {
    choices: Choice[];
    onSaveChoice: (choice: Choice) => void;
}

export interface ChoiceFormListRef {
    getChoices: () => Choice[];
    validateChoices: () => boolean;
}

const ChoiceFormList = forwardRef<ChoiceFormListRef, ChoiceFormListProps>(
    ({ choices, onSaveChoice }, ref) => {
        const [localChoices, setLocalChoices] = useState<Choice[]>(choices);

        const handleChoiceChange = (updatedChoice: Choice) => {
            setLocalChoices((prevChoices) =>
                prevChoices.map((choice) =>
                    choice.id === updatedChoice.id ? updatedChoice : choice,
                ),
            );
        };

        const handleDeleteChoice = (choiceId: number | undefined) => {
            setLocalChoices((prevChoices) =>
                prevChoices.filter((choice) => choice.id !== choiceId),
            );
        };

        useImperativeHandle(ref, () => ({
            getChoices: () => localChoices,
            validateChoices: () => {
                for (const choice of localChoices) {
                    console.log(choice);
                    if (!choice.text.trim()) {
                        alert('All choices must have text');
                        return false;
                    }
                    if (choice.value === null || isNaN(Number(choice.value))) {
                        alert('All choices must have a valid numeric value');
                        return false;
                    }
                }
                return true;
            },
        }));

        const handleAddChoice = () => {
            const newChoice: Choice = {
                id: undefined, // Temporary ID, replace with actual ID from backend
                text: '',
                order: localChoices.length + 1,
                value: undefined,
            };
            setLocalChoices([...localChoices, newChoice]);
        };

        return (
            <div>
                {localChoices.map((choice, index) => (
                    <ChoiceForm
                        key={index}
                        {...choice}
                        onChange={handleChoiceChange}
                        onDelete={() => handleDeleteChoice(choice.id)}
                    />
                ))}
                <FormButton
                    variant="text"
                    onClick={handleAddChoice}
                    className="text-blue-500 underline mt-2"
                >
                    Add Choice
                </FormButton>
            </div>
        );
    },
);

export default ChoiceFormList;
