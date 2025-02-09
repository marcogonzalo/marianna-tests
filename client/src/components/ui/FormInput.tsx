import { Description, Field, Input, Label } from '@headlessui/react';
import clsx from 'clsx';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    description?: string;
    className?: string;
    blockClassName?: string;
}

export default function FormInput({
    id,
    name,
    label,
    description,
    className,
    blockClassName,
    ...props
}: InputProps) {
    return (
        <Field className={blockClassName}>
            {label && (
                <Label
                    htmlFor={id ?? name}
                    className="text-sm/6 font-medium text-gray-9000"
                >
                    {label}
                </Label>
            )}
            {description && (
                <Description className="text-sm/6 text-white/50">
                    {description}
                </Description>
            )}
            <div className="flex items-center rounded-md bg-white pl-3 outline outline-1 -outline-offset-1 outline-gray-300 focus-within:outline focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                <Input
                    id={id ?? name}
                    name={name ?? id}
                    className={clsx(
                        //'mt-3 block w-full rounded-lg border-none bg-white/5 py-1.5 px-3 text-sm/6 text-white',
                        //'focus:outline-none data-[focus]:outline-2 data-[focus]:-outline-offset-2 data-[focus]:outline-white/25',
                        'block min-w-0 grow py-1.5 pl-1 pr-3 text-base text-gray-900 placeholder:text-gray-400 focus:outline focus:outline-0 sm:text-sm/6',
                        { className },
                    )}
                    {...props}
                />
            </div>
        </Field>
    );
}
