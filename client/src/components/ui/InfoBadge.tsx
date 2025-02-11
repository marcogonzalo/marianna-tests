import React from 'react';

interface InfoBadgeProps extends React.HTMLAttributes<HTMLDivElement> {
    color?: string;
    children: React.ReactNode;
}

export default function InfoBadge({
    color = 'gray',
    children,
    className = '',
    ...rest
}: InfoBadgeProps) {
    const baseStyles = `inline-flex items-center rounded bg-${color}-100 px-2 py-1 ${
        rest.onClick ? 'cursor-pointer' : ''
    } ${className}`;
    const textStyles = `text-${color}-700`;

    return (
        <div className={baseStyles} {...rest}>
            <span className={textStyles}>{children}</span>
        </div>
    );
}
