import { useState } from 'react';
import InfoBadge from '@/components/ui/InfoBadge';
import { Assessment } from '@/features/assessments/types/client';
import { ScoringMethod } from '@/features/assessments/types/shared';
import { PencilIcon } from '@heroicons/react/24/outline';
import Markdown from 'react-markdown';
import EditAssessmentModal from './EditAssessmentModal';

interface AssessmentCardProps {
    assessment: Assessment;
    onClick?: () => void;
    onUpdate?: (assessment: Assessment) => Promise<void>;
}

export default function AssessmentCard({
    assessment,
    onClick,
    onUpdate,
}: AssessmentCardProps) {
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);

    const handleEditClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        setIsEditModalOpen(true);
    };

    const handleSave = async (updatedAssessment: Partial<Assessment>) => {
        if (onUpdate) {
            await onUpdate({
                ...assessment,
                ...updatedAssessment,
            });
        }
    };

    return (
        <>
            <div
                className={`card p-6 hover:shadow-md transition-shadow relative ${
                    onClick ? 'cursor-pointer' : ''
                }`}
                onClick={onClick}
            >
                {onUpdate && (
                    <button
                        onClick={handleEditClick}
                        className="absolute top-4 right-4 p-2 text-gray-500 hover:text-gray-700 rounded-full hover:bg-gray-100"
                    >
                        <PencilIcon className="h-5 w-5" />
                    </button>
                )}

                <h3 className="text-xl font-semibold text-gray-900 mb-2 pr-12">
                    {assessment.title}
                </h3>
                <p className="text-gray-500 line-clamp-2 mb-4">
                    <Markdown>{assessment.description}</Markdown>
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

            <EditAssessmentModal
                assessment={assessment}
                isOpen={isEditModalOpen}
                onClose={() => setIsEditModalOpen(false)}
                onSave={handleSave}
            />
        </>
    );
}
