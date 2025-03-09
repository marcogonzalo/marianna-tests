import { Diagnostic } from '@/features/assessments/types/client';
import Markdown from 'react-markdown';

interface DiagnosticListProps {
    diagnostics: Diagnostic[];
    isLoading?: boolean;
    error?: string | null;
}

export default function DiagnosticList({
    diagnostics,
    isLoading = false,
    error = null,
}: DiagnosticListProps) {
    if (isLoading) {
        return <div className="text-center py-4">Loading traits...</div>;
    }

    if (error) {
        return <div className="text-red-600 text-sm py-2">{error}</div>;
    }

    if (diagnostics.length === 0) {
        return (
            <div className="text-center py-4 text-gray-500">
                No traits found for this assessment.
            </div>
        );
    }

    return (
        <div className="mb-6">
            <ul className="divide-y divide-gray-200">
                {diagnostics.map((diagnostic) => (
                    <li
                        key={diagnostic.id}
                        className="p-2 hover:bg-gray-50 flex"
                    >
                        <div className="mt-1 flex-col items-center text-xs text-gray-500">
                            <p>
                                <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-gray-100 text-gray-800 mr-2">
                                    Min: {diagnostic.minValue ?? '-∞'}
                                </span>
                                <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-gray-100 text-gray-800">
                                    Max: {diagnostic.maxValue ?? '∞'}
                                </span>
                            </p>
                            <div className="ml-2 mt-2 text-sm font-medium text-gray-900">
                                <Markdown>{diagnostic.description}</Markdown>
                            </div>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}
