import { Button } from '@headlessui/react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary';
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
        'inline-flex justify-center rounded-md border py-2 px-4 text-sm font-medium shadow-sm';

    const variantStyles = {
        primary: {
            base: 'btn-primary border-transparent bg-indigo-600 text-white',
            hover: 'hover:bg-indigo-700',
        },
        secondary: {
            base: 'btn-secondary text-white bg-indigo-400',
            hover: 'hover:bg-indigo-700',
        },
    };

    const sizeStyles = {
        sm: 'h-9 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-11 px-6 text-lg',
    };

    const combinedClassName = `${baseStyles} ${variantStyles[variant].base} ${
        !disabled && variantStyles[variant].hover
    } ${sizeStyles[size]} ${
        disabled ? 'opacity-50 cursor-not-allowed' : ''
    } ${className}`;

    return (
        <Button className={combinedClassName} {...props}>
            {children}
        </Button>
    );
}
