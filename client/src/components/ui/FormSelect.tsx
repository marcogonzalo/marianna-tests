import { Field, Description, Select, Label } from '@headlessui/react';
import { ChevronDownIcon } from '@heroicons/react/20/solid';
import clsx from 'clsx';
import { ChangeEventHandler } from 'react';

interface props {
    label?: string;
    id: string;
    description?: string;
    children: React.ReactNode;
    value: number | string | readonly string[] | undefined;
    onChange?: ChangeEventHandler<HTMLSelectElement> | undefined;
    className?: string;
    required?: boolean;
}

export default function FormSelect({
    label,
    id,
    description,
    children,
    value,
    onChange,
    className,
    required = false,
}: props) {
    return (
        <Field>
            {label && (
                <Label
                    htmlFor={id}
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
            <div className="mt-2 grid grid-cols-1">
                <Select
                    id={id}
                    value={value}
                    onChange={onChange}
                    className={clsx(
                        // 'mt-3 block w-full appearance-none rounded-lg border-none bg-white/5 py-1.5 px-3 text-sm/6 text-white',
                        // 'focus:outline-none data-[focus]:outline-2 data-[focus]:-outline-offset-2 data-[focus]:outline-white/25',
                        // // Make the text of each option black on Windows
                        // '*:text-black',
                        'col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pl-3 pr-8 text-base text-gray-900 outline outline-1 -outline-offset-1 outline-gray-300 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6',
                        { className },
                    )}
                    required={required}
                >
                    {children}
                </Select>
                <ChevronDownIcon
                    className="pointer-events-none col-start-1 row-start-1 mr-2 size-5 self-center justify-self-end text-gray-500 sm:size-4"
                    aria-hidden="true"
                />
            </div>
        </Field>
    );
}
