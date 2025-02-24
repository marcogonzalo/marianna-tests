import React, { useState } from 'react';
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
            [field]: field === 'text' ? newValue : Number(newValue),
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
                    type="number"
                    value={value}
                    onChange={(e) => {
                        setValue(e.target.value);
                        handleChange('value', e.target.value);
                    }}
                />
                <FormButton
                    variant="link"
                    onClick={onDelete}
                    className="self-end mb-1 text-red-500 hover:text-red-700"
                >
                    X
                </FormButton>
            </div>
        </form>
    );
};
export default ChoiceForm;
