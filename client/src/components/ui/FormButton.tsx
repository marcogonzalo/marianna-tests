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
    const baseStyles = 'btn';

    const variantStyles = {
        primary: 'btn-primary',
        secondary: 'btn-secondary',
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
