import { Choice as ChoiceType } from '../types/client';
import Choice from './Choice';

interface ChoiceListProps {
    choices: ChoiceType[];
    name: string; // name for radio group
    response?: number | string;
    showDisabled?: boolean;
}

export default function ChoiceList({
    choices,
    name,
    response,
    showDisabled = false,
}: ChoiceListProps) {
    return (
        <>
            {choices.map((choice) => (
                <Choice
                    key={choice.id}
                    {...choice}
                    name={name}
                    disabled={showDisabled}
                    checked={response === choice.value}
                />
            ))}
        </>
    );
}
