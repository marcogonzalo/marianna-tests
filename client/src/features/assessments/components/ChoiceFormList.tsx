import React, { useState } from 'react';
import { Choice } from '@/features/assessments/types';
import { FormButton, FormInput } from '@/components/ui';

const ChoiceForm: React.FC<Choice> = ({ ...choice }) => {
    const [text, setText] = useState(choice.text);
    const [order, setOrder] = useState(choice.order || 0);
    const [value, setValue] = useState(choice.value || '');

    return (
        <form className="space-y-4">
            <div className="grid grid-cols-8 gap-4">
                <FormInput
                    label="Choice Text"
                    id="choiceText"
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
                <FormInput
                    label="Value"
                    type="text"
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                />
            </div>
        </form>
    );
};

interface ChoiceFormListProps {
    choices: Choice[];
    onSaveChoice: (choice: Choice) => void;
}

const ChoiceFormList: React.FC<ChoiceFormListProps> = ({ choices }) => {
    const [localChoices, setLocalChoices] = useState<Choice[]>(choices);

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
            {localChoices.map((choice) => (
                <ChoiceForm key={choice.id} {...choice} />
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
};

export default ChoiceFormList;
