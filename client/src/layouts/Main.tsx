import { ReactNode } from 'react';

interface props {
    children: ReactNode;
}

export function Main({ children }: props) {
    return (
        <main className="min-h-screen bg-gray-50 py-8">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                {children}
            </div>
        </main>
    );
}
