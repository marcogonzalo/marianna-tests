import { Assessment } from '../types';

interface AssessmentCardProps {
  assessment: Assessment;
  onClick: () => void;
}

export default function AssessmentCard({ assessment, onClick }: AssessmentCardProps) {
  return (
    <div
      className="card p-6 hover:shadow-md transition-shadow cursor-pointer"
      onClick={onClick}
    >
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{assessment.title}</h3>
      <p className="text-gray-500 line-clamp-2 mb-4">{assessment.description}</p>
      
      <div className="flex items-center justify-between text-sm">
        <div className="inline-flex items-center rounded bg-gray-100 px-2 py-1">
          <span className="text-gray-600">
            {assessment.scoring_method === 'boolean'
              ? 'Boolean (0-1)'
              : assessment.scoring_method === 'scored'
              ? 'Scored (-1 to 1)'
              : `Custom (${assessment.min_value} to ${assessment.max_value})`}
          </span>
        </div>
        <div className="inline-flex items-center rounded bg-gray-100 px-2 py-1">
          <span className="text-gray-600">
            {assessment.questions?.length || 0} questions
          </span>
        </div>
      </div>
    </div>
  );
} 