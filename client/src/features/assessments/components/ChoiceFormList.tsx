import { useState, forwardRef, useImperativeHandle, useEffect } from 'react';
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
        const [sortedChoices, setSortedChoices] = useState<Choice[]>(choices);

        // Add this useEffect to update localChoices when props change
        useEffect(() => {
            setLocalChoices(choices);
        }, [choices]);

        useEffect(() => {
            setSortedChoices(
                [...localChoices].sort(
                    (a, b) => (a.order ?? 0) - (b.order ?? 0),
                ),
            );
        }, [localChoices]);

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
                id: -Date.now(), // Temporary ID to avoid object overwriting in array, replace with actual ID from backend
                text: '',
                order:
                    Number(
                        sortedChoices[sortedChoices.length - 1]?.order || 0,
                    ) + 1,
                value: 0,
                questionId: 0,
            };
            setLocalChoices([...localChoices, newChoice]);
        };

        return (
            <>
                {sortedChoices.map((choice) => (
                    <ChoiceForm
                        key={choice.id}
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
            </>
        );
    },
);

export default ChoiceFormList;
