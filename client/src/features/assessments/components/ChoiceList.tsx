import { Choice as ChoiceType } from '../types/client';
import Choice from './Choice';

interface ChoiceListProps {
    choices: ChoiceType[];
    name: string; // name for radio group
    showDisabled?: boolean;
}

export default function ChoiceList({
    choices,
    name,
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
                />
            ))}
        </div>
    );
}
