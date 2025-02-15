import { useState } from 'react';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';
import { FormButton, FormInput, FormSelect } from '@/components/ui';
import { createUser } from '@/features/users/api';
import { CreateAccountRequest, CreateUserRequest, UserRole } from '../types';

interface CreateUserModalProps {
    isOpen: boolean;
    onClose: () => void;
    onUserCreated: () => void;
}

export function CreateUserModal({
    isOpen,
    onClose,
    onUserCreated,
}: CreateUserModalProps) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [formData, setFormData] = useState({
        email: '',
        firstName: '',
        lastName: '',
        role: UserRole.ASSESSMENT_DEVELOPER,
        password: '',
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const userAccount: CreateUserRequest = {
                email: formData.email,
                password: formData.password,
                account: {
                    firstName: formData.firstName,
                    lastName: formData.lastName,
                    role: formData.role as UserRole,
                } as CreateAccountRequest,
            };
            await createUser(userAccount);
            onUserCreated();
            onClose();
        } catch (err) {
            setError('Failed to create user');
            console.error('Error creating user:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={isOpen} onClose={onClose} className="relative z-50">
            <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
            <div className="fixed inset-0 flex items-center justify-center p-4">
                <DialogPanel className="mx-auto max-w-md rounded-xl bg-white p-6 shadow-xl">
                    <DialogTitle className="text-lg font-medium mb-4">
                        Create New User
                    </DialogTitle>

                    {error && (
                        <div className="mb-4 text-red-600 text-sm">{error}</div>
                    )}

                    <form onSubmit={handleSubmit}>
                        <div className="space-y-4">
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
                                        {role.replace('_', ' ').toUpperCase()}
                                    </option>
                                ))}
                            </FormSelect>
                            <FormInput
                                label="Email"
                                type="email"
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
                                label="Password"
                                type="password"
                                required
                                value={formData.password}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        password: e.target.value,
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
                                Create User
                            </FormButton>
                        </div>
                    </form>
                </DialogPanel>
            </div>
        </Dialog>
    );
}
