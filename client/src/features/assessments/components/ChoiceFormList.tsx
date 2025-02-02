import { useState, forwardRef, useImperativeHandle } from 'react';
import { Choice } from '@/features/assessments/types';
import { FormButton } from '@/components/ui';
import ChoiceForm from './ChoiceForm';

interface ChoiceFormListProps {
    choices: Choice[];
    onSaveChoice: (choice: Choice) => void;
}

export interface ChoiceFormListRef {
    getChoices: () => Choice[];
    validateChoices: () => boolean;
}

const ChoiceFormList = forwardRef<ChoiceFormListRef, ChoiceFormListProps>(
    ({ choices }, ref) => {
        const [localChoices, setLocalChoices] = useState<Choice[]>(choices);

        const sortedChoices = [...localChoices].sort(
            (a, b) => (a.order ?? 0) - (b.order ?? 0),
        );

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
                value: 0,
                questionId: 0,
            };
            setLocalChoices([...localChoices, newChoice]);
        };

        return (
            <div>
                {sortedChoices.map((choice, index) => (
                    <ChoiceForm
                        key={choice.id ?? index}
                        {...choice}
                        onChange={handleChoiceChange}
                        onDelete={() => handleDeleteChoice(choice.id)}
                    />
                ))}
                <FormButton
                    variant="text"
                    onClick={handleAddChoice}
                    className="underline self-center"
                >
                    Add Choice
                </FormButton>
            </div>
        );
    },
);

export default ChoiceFormList;
