import { useState } from 'react';
import { Dialog, DialogPanel, DialogTitle, Field } from '@headlessui/react';
import { Assessment } from '@/features/assessments/types/client';
import { FormButton, FormInput, FormLabel } from '@/components/ui';
import TextEditor from '@/components/text-editor';

interface EditAssessmentModalProps {
    assessment: Assessment;
    isOpen: boolean;
    onClose: () => void;
    onSave: (updatedAssessment: Partial<Assessment>) => Promise<void>;
}

export default function EditAssessmentModal({
    assessment,
    isOpen,
    onClose,
    onSave,
}: EditAssessmentModalProps) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState({
        title: assessment.title,
        description: assessment.description || '',
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await onSave(formData);
            onClose();
        } catch (error) {
            setError('Failed to update assessment');
            console.error('Failed to update assessment:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={isOpen} onClose={onClose} className="relative z-50">
            <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
            <div className="fixed inset-0 flex items-center justify-center p-4">
                <DialogPanel className="mx-auto max-w-md rounded-xl bg-white p-6 shadow-xl sm:w-1/2">
                    <DialogTitle className="text-lg font-medium mb-4">
                        Edit Assessment
                    </DialogTitle>

                    {error && (
                        <div className="mb-4 text-red-600 text-sm">{error}</div>
                    )}

                    <form onSubmit={handleSubmit}>
                        <div className="space-y-4">
                            <FormInput
                                label="Title"
                                required
                                value={formData.title}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        title: e.target.value,
                                    }))
                                }
                            />

                            <Field>
                                <FormLabel>Description</FormLabel>
                                <TextEditor
                                    data={formData.description}
                                    onChange={(value) => setFormData((prev) => ({
                                        ...prev,
                                        description: value,
                                    }))}
                                />
                            </Field>
                        </div>

                        <div className="mt-6 flex justify-end space-x-3">
                            <FormButton
                                type="button"
                                variant="secondary"
                                onClick={onClose}
                                disabled={loading}
                            >
                                Cancel
                            </FormButton>
                            <FormButton
                                type="submit"
                                variant="primary"
                                disabled={loading}
                            >
                                Save Changes
                            </FormButton>
                        </div>
                    </form>
                </DialogPanel>
            </div>
        </Dialog>
    );
} 