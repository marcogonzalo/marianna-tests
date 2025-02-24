import FormRadio from '@/components/ui/FormRadio';
import { Choice as ChoiceType } from '../types/client';

interface props extends ChoiceType {
    name: string;
    disabled?: boolean;
    checked?: boolean;
}
export default function Choice({
    id,
    text,
    value,
    name,
    checked = false,
    ...rest
}: props) {
    const inputId = `${name}-${id}`;
    return (
        <FormRadio
            id={inputId}
            value={value}
            name={name}
            label={text}
            checked={checked}
            {...rest}
        />
    );
}
