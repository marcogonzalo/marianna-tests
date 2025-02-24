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
        <div className="mt-4">
            {choices.map((choice, index) => (
                <Choice
                    key={index}
                    {...choice}
                    name={name}
                    disabled={showDisabled}
                    checked={response === choice.value}
                />
            ))}
        </div>
    );
}
