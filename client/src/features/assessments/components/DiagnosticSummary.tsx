import { Diagnostic } from '@/features/assessments/types/client';

interface DiagnosticSummaryProps {
    score: number | null;
    diagnostic: Diagnostic;
}

export default function DiagnosticSummary({
    score,
    diagnostic,
}: DiagnosticSummaryProps) {
    if (score === undefined || score === null) {
        return null;
    }

    return (
        <div className="mt-6 bg-gray-50 rounded-lg p-4 border border-gray-200">
            <h4 className="font-semibold text-gray-900">
                Trait summary:
            </h4>

            {!diagnostic && (
                <p className="text-sm text-gray-500">Loading trait...</p>
            )}

            {diagnostic && (
                <>
                    <div className="items-center">
                        <p className="text-xs text-gray-500 align-middle">
                            Scoring range:{' '}
                            {diagnostic.minValue != null ? (
                                diagnostic.minValue
                            ) : (
                                <span className="text-lg align-middle">-∞</span>
                            )}{' '}
                            --{' '}
                            {diagnostic.maxValue != null ? (
                                diagnostic.maxValue
                            ) : (
                                <span className="text-lg align-middle">∞</span>
                            )}
                        </p>
                        <div className="text-sm text-gray-700">
                            {diagnostic.description}
                        </div>
                    </div>

                </>
            )}
        </div>
    );
}
