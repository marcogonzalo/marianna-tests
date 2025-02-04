import { Field, Input, Label } from '@headlessui/react';

interface RadioProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string;
    value: string;
    name: string;
}
export default function FormRadio({ label, value, name }: RadioProps) {
    return (
        <Field>
            <Label className="flex items-center space-x-2 p-2">
                <Input
                    type="radio"
                    value={value}
                    name={name}
                    className="form-radio"
                />
                <span>{label}</span>
            </Label>
        </Field>
    );
}
