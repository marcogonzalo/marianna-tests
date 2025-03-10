import { useState } from 'react';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';
import { FormButton, FormInput, FormSelect } from '@/components/ui';
import { createExaminee } from '@/features/examinees/api'; // Assume this function is defined to create an examinee
import {
    CreateExamineeRequest,
    Examinee,
    Gender,
} from '@/features/examinees/types'; // Assume this type is defined in a types file

interface CreateExamineeModalProps {
    isOpen: boolean;
    onClose: () => void;
    onExamineeCreated: (examinee: Examinee) => void;
}

export default function CreateExamineeModal({
    isOpen,
    onClose,
    onExamineeCreated,
}: CreateExamineeModalProps) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState({
        firstName: '',
        middleName: '',
        lastName: '',
        gender: Gender.FEMALE,
        birthDate: '',
        email: '',
        internalIdentifier: '',
        comments: '',
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        const newExaminee: CreateExamineeRequest = {
            firstName: formData.firstName,
            middleName: formData.middleName,
            lastName: formData.lastName,
            email: formData.email,
            gender: formData.gender as Gender,
            birthDate: formData.birthDate as unknown as Date,
            internalIdentifier: formData.internalIdentifier,
            comments: formData.comments,
        };
        try {
            const createdExaminee = await createExaminee(newExaminee);
            onExamineeCreated(createdExaminee);
            onClose(); // Close the modal after creation
        } catch (error) {
            setError('Failed to create examinee');
            console.error('Error creating examinee:', error);
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <Dialog open={isOpen} onClose={onClose} className="relative z-50">
            <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
            <div className="fixed inset-0 flex items-center justify-center p-4">
                <DialogPanel className="mx-auto max-w-md rounded-xl bg-white p-6 shadow-xl">
                    <DialogTitle className="text-lg font-medium mb-4">
                        Create New Examinee
                    </DialogTitle>

                    {error && (
                        <div className="mb-4 text-red-600 text-sm">{error}</div>
                    )}

                    <form onSubmit={handleSubmit}>
                        <div className="grid grid-cols-2 gap-4">
                            <FormInput
                                label="First Name"
                                required
                                value={formData.firstName}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        firstName: e.target.value,
                                    }))
                                }
                            />
                            <FormInput
                                label="Middle Name"
                                value={formData.middleName}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        middleName: e.target.value,
                                    }))
                                }
                            />
                            <FormInput
                                label="Last Name"
                                required
                                value={formData.lastName}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        lastName: e.target.value,
                                    }))
                                }
                            />
                            <FormSelect
                                label="Gender"
                                required
                                value={formData.gender}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        gender: e.target.value as Gender,
                                    }))
                                }
                                id={''}
                            >
                                {Object.values(Gender).map((gender) => (
                                    <option key={gender} value={gender}>
                                        {gender}
                                    </option>
                                ))}
                            </FormSelect>
                            <FormInput
                                label="Birth date"
                                type="date"
                                value={formData.birthDate}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        birthDate: e.target.value,
                                    }))
                                }
                            />
                            <FormInput
                                label="Email"
                                required
                                value={formData.email}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        email: e.target.value,
                                    }))
                                }
                            />
                            <FormInput
                                label="Internal identifier"
                                value={formData.internalIdentifier}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        internalIdentifier: e.target.value,
                                    }))
                                }
                            />

                            <FormInput
                                label="Comments"
                                value={formData.comments}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        comments: e.target.value,
                                    }))
                                }
                            />
                        </div>
                        <div className="mt-6 flex justify-end space-x-3">
                            <FormButton
                                type="button"
                                variant="secondary"
                                onClick={onClose}
                            >
                                Cancel
                            </FormButton>
                            <FormButton
                                type="submit"
                                variant="primary"
                                disabled={loading}
                            >
                                Create Examinee
                            </FormButton>
                        </div>
                    </form>
                </DialogPanel>
            </div>
        </Dialog>
    );
}
