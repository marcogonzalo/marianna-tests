import { Description, Field, Label, Textarea } from '@headlessui/react';
import clsx from 'clsx';

interface props {
    label?: string;
    id: string;
    value: string;
    description?: string;
    onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
    className?: string;
    rows?: number;
}

export default function FormTextarea({
    label,
    id,
    value,
    description,
    onChange,
    className,
    rows = 3,
}: props) {
    return (
        <Field>
            {label && (
                <Label
                    htmlFor={id}
                    className="block text-sm font-medium text-gray-700"
                >
                    {label}
                </Label>
            )}
            {description && (
                <Description className="text-sm/6 text-white/50">
                    {description}
                </Description>
            )}
            <Textarea
                id={id}
                value={value}
                onChange={onChange}
                className={clsx(
                    // 'mt-3 block w-full resize-none rounded-lg border-none bg-white/5 py-1.5 px-3 text-sm/6 text-white',
                    // 'focus:outline-none data-[focus]:outline-2 data-[focus]:-outline-offset-2 data-[focus]:outline-white/25',
                    'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6',
                    { className },
                )}
                rows={rows}
            />
        </Field>
    );
}
