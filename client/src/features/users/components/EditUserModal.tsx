import { useState, useEffect } from 'react';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';
import { FormButton, FormInput, FormSelect } from '@/components/ui';
import { updateUser } from '@/features/users/api';
import { User, UpdateUserRequest } from '@/features/users/types/client';
import { UserRole } from '@/features/users/types/shared';

interface EditUserModalProps {
    isOpen: boolean;
    onClose: () => void;
    user: User;
    onUserUpdated: (user: User) => void;
}

export default function EditUserModal({
    isOpen,
    onClose,
    user,
    onUserUpdated,
}: EditUserModalProps) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        role: UserRole.ASSESSMENT_REVIEWER,
        email: '',
    });

    useEffect(() => {
        if (user) {
            setFormData({
                firstName: user.account?.firstName || '',
                lastName: user.account?.lastName || '',
                role: (user.account?.role as UserRole) || UserRole.ASSESSMENT_REVIEWER,
                email: user.email,
            });
        }
    }, [user]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        const updatedUser: UpdateUserRequest = {
            email: formData.email,
            account: {
                firstName: formData.firstName,
                lastName: formData.lastName,
                role: formData.role,
            },
        };
        try {
            const updated = await updateUser(user.id, updatedUser);
            onUserUpdated(updated);
            onClose();
        } catch (error) {
            setError('Failed to update user');
            console.error('Error updating user:', error);
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
                        Edit User
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
                            <FormSelect
                                label="Role"
                                required
                                value={formData.role}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        role: e.target.value as UserRole,
                                    }))
                                }
                                id={''}
                            >
                                {Object.values(UserRole).map((role) => (
                                    <option key={role} value={role}>
                                        {role}
                                    </option>
                                ))}
                            </FormSelect>
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
                                Save Changes
                            </FormButton>
                        </div>
                    </form>
                </DialogPanel>
            </div>
        </Dialog>
    );
} 