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
    ...props
}: ButtonProps) {
    const baseStyles =
        'inline-flex justify-center rounded-md border py-2 px-4 text-sm font-medium shadow-sm';

    const variantStyles = {
        primary:
            'btn-primary border-transparent bg-indigo-600 text-white hover:bg-indigo-700',
        secondary: 'btn-secondary hover:text-white hover:bg-indigo-700',
    };

    const sizeStyles = {
        sm: 'h-9 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-11 px-6 text-lg',
    };

    const combinedClassName = `${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`;

    return (
        <Button className={combinedClassName} {...props}>
            {children}
        </Button>
    );
}
