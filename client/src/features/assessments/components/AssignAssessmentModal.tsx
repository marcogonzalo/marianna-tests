import { useEffect, useState } from 'react';
import { FormButton } from '@/components/ui';
import {
    getAssessments,
    createAssessmentResponse,
} from '@/features/assessments/api';
import {
    Assessment,
    CreateAssessmentResponse,
} from '@/features/assessments/types/client';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';

interface AssignAssessmentModalProps {
    isOpen: boolean;
    onClose: () => void;
    examineeId: string;
}

export function AssignAssessmentModal({
    isOpen,
    onClose,
    examineeId,
}: AssignAssessmentModalProps) {
    const [assessments, setAssessments] = useState<Assessment[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchAssessments = async () => {
            try {
                const data = await getAssessments();
                setAssessments(data);
                setError(null);
            } catch (err) {
                setError('Failed to load assessments');
                console.error('Error loading assessments:', err);
            } finally {
                setLoading(false);
            }
        };

        if (isOpen) {
            fetchAssessments();
        }
    }, [isOpen]);

    const handleAssign = async (assessmentId: number) => {
        try {
            const data: CreateAssessmentResponse = {
                examineeId,
            };
            await createAssessmentResponse(assessmentId, data);
            alert('Assessment assigned successfully!');
            onClose(); // Close the modal after assignment
        } catch (err) {
            console.error('Error assigning assessment:', err);
            alert('Failed to assign assessment');
        }
    };
    return (
        <Dialog open={isOpen} onClose={onClose} className="relative z-50">
            <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
            <div className="fixed inset-0 flex items-center justify-center p-4">
                <DialogPanel className="mx-auto max-w-md rounded-xl bg-white p-6 shadow-xl">
                    <DialogTitle className="text-lg font-medium mb-4">
                        Assign Assessment
                    </DialogTitle>
                    {loading && (<div>Loading assessments...</div>)}
                    {error && (
                        <div className="mb-4 text-red-600 text-sm">{error}</div>
                    )}
                    {!loading && (<ul>
                        {assessments.map((assessment) => (
                            <li
                                key={assessment.id}
                                className="flex justify-between items-center"
                            >
                                <span>{assessment.title}</span>
                                <FormButton
                                    onClick={() => handleAssign(assessment.id!)}
                                >
                                    Assign
                                </FormButton>
                            </li>
                        ))}
                    </ul>)}
                    <FormButton onClick={onClose}>Close</FormButton>
                </DialogPanel>
            </div>
        </Dialog>
    );
}
