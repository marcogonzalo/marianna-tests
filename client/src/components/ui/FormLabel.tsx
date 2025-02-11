import { Label } from '@headlessui/react';

interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
    htmlFor?: string;
    className?: string;
    children?: React.ReactNode;
}

export default function FormLabel({
    htmlFor,
    className,
    children,
}: LabelProps) {
    return (
        <Label
            htmlFor={htmlFor}
            className={`text-sm/6 font-medium text-gray-700 ${className}`}
        >
            {children}
        </Label>
    );
}
