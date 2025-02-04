import { FormInput, FormLabel } from '@/components/ui';
import { Choice as ChoiceType } from '../types/client';
import { Field, Input, Label } from '@headlessui/react';

interface props extends ChoiceType {
    name: string;
}
export default function Choice({ text, value, name }: props) {
    return (
        <Field>
            <Label className="flex items-center space-x-2 p-2">
                <Input
                    type="radio"
                    value={value}
                    name={name}
                    className="form-radio"
                />
                <span>{text}</span>
            </Label>
        </Field>
    );
}
