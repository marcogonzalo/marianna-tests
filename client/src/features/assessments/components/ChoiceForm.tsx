import React, { useState } from 'react';
import { Choice } from '@/features/assessments/types';
import { FormButton, FormInput } from '@/components/ui';

interface ChoiceFormProps extends Choice {
    onSave?: (choice: Choice) => void;
}

const ChoiceForm: React.FC<ChoiceFormProps> = ({ onSave, ...choice }) => {
    const [text, setText] = useState(choice.text);
    const [order, setOrder] = useState(choice.order || 0);
    const [value, setValue] = useState(choice.value || null);

    const isChanged =
        text !== choice.text ||
        order !== choice.order ||
        value !== choice.value;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!text.trim()) {
            alert('Choice text is required');
            return;
        }
        if (value === null || isNaN(value)) {
            alert('Choice value is required and must be a number');
            return;
        }
        if (onSave) onSave({ ...choice, text, order, value });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-10 gap-4">
                <FormInput
                    label="Choice Text"
                    id="choiceText"
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    blockClassName="col-span-6"
                />
                <FormInput
                    label="Value"
                    type="text"
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                />
                <FormInput
                    label="Order"
                    type="number"
                    value={order}
                    onChange={(e) => setOrder(Number(e.target.value))}
                    blockClassName="col-span-6"
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
        </form>
    );
};

export default ChoiceForm;
