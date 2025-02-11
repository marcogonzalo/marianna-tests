import { Input } from '@headlessui/react';

interface RadioProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string;
    name: string;
}
export default function FormRadio({ id, label, value, name }: RadioProps) {
    return (
        <label
            htmlFor={id}
            className="flex items-center space-x-2 p-2 cursor-pointer"
        >
            <Input
                id={id}
                type="radio"
                value={value}
                name={name}
                className="form-radio"
            />
            <span className="text-sm text-gray-700">{label}</span>
        </label>
    );
}
