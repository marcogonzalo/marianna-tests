import { Diagnostic } from '@/features/assessments/types/client';

interface AssessmentScoreSummaryProps {
    score: number | null;
    diagnostic: Diagnostic;
}

export default function AssessmentScoreSummary({
    score,
    diagnostic,
}: AssessmentScoreSummaryProps) {
    if (score === undefined || score === null) {
        return null;
    }

    return (
        <div className="mt-6 bg-gray-50 rounded-lg p-4 border border-gray-200">
            <h4 className="text-base font-medium text-gray-900 mb-2">
                Assessment score summary
            </h4>

            {!diagnostic && (
                <p className="text-sm text-gray-500">Loading diagnostic...</p>
            )}

            {diagnostic && (
                <>
                    <div className="items-center mb-4 align-middle">
                        <p className="text-sm font-semibold text-gray-900">
                            Score obtanied: {score}
                        </p>
                        <p className="text-sm text-gray-500 mt-2 align-middle">
                            Trait scoring range:{' '}
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
                    </div>

                    <div className="mt-3 p-3">
                        <p className="text-sm text-gray-700">
                            {diagnostic.description}
                        </p>
                    </div>
                </>
            )}
        </div>
    );
}
