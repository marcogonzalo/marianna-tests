import InfoBadge from '@/components/ui/InfoBadge';
import { Assessment } from '@/features/assessments/types/client';
import { ScoringMethod } from '@/features/assessments/types/shared';

interface AssessmentCardProps {
    assessment: Assessment;
    onClick?: () => void;
}

export default function AssessmentCard({
    assessment,
    onClick,
}: AssessmentCardProps) {
    return (
        <div
            className={`card p-6 hover:shadow-md transition-shadow ${
                onClick ? 'cursor-pointer' : ''
            }`}
            onClick={onClick}
        >
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {assessment.title}
            </h3>
            <p className="text-gray-500 line-clamp-2 mb-4">
                {assessment.description}
            </p>

            <div className="flex items-center justify-between text-sm mb-4">
                <InfoBadge color="gray">
                    {assessment.scoringMethod === ScoringMethod.BOOLEAN
                        ? 'Boolean (0-1)'
                        : assessment.scoringMethod === ScoringMethod.SCORED
                        ? 'Scored (-1 to 1)'
                        : `Custom (${assessment.minValue} to ${assessment.maxValue})`}
                </InfoBadge>
                <InfoBadge color="gray">
                    {assessment.questions?.length || 0} questions
                </InfoBadge>
            </div>
        </div>
    );
}
