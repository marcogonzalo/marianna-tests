import { Button } from '@headlessui/react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'danger' | 'link';
    size?: 'sm' | 'md' | 'lg';
}

export default function FormButton({
    variant = 'primary',
    size = 'md',
    className = '',
    children,
    disabled,
    ...props
}: ButtonProps) {
    const baseStyles =
        'inline-flex justify-center rounded-md border border-transparent py-2 px-4 text-sm font-medium';

    const variantStyles = {
        primary: {
            base: 'btn-primary bg-indigo-600 text-white shadow-sm',
            hover: 'hover:bg-indigo-700',
        },
        secondary: {
            base: 'btn-secondary text-white bg-indigo-400 shadow-sm',
            hover: 'hover:bg-indigo-700',
        },
        link: {
            base: 'btn-text text-indigo-600',
            hover: 'hover:text-indigo-700',
        },
        danger: {
            base: 'btn-danger bg-red-600 text-white shadow-sm',
            hover: 'hover:bg-red-700',
        },
    };

    const sizeStyles = {
        sm: 'h-9 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-11 px-6 text-lg',
    };

    const combinedClassName = `${baseStyles} ${variantStyles[variant].base} ${
        sizeStyles[size]
    } ${
        disabled
            ? 'opacity-50 cursor-not-allowed'
            : variantStyles[variant].hover
    } ${className}`;

    return (
        <Button className={combinedClassName} {...props}>
            {children}
        </Button>
    );
}
