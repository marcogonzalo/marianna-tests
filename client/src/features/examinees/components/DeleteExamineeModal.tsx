import { useState } from 'react';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';
import { FormButton } from '@/components/ui';
import { deleteExaminee } from '../api';
import { Examinee } from '../types';
import { UserRole } from '@/features/users/types/shared';
import { useAuth } from '@/contexts/AuthContext';

interface DeleteExamineeModalProps {
    isOpen: boolean;
    onClose: () => void;
    examinee: Examinee;
    hasAssessmentResponses: boolean;
    onExamineeDeleted: () => void;
}

export default function DeleteExamineeModal({
    isOpen,
    onClose,
    examinee,
    hasAssessmentResponses,
    onExamineeDeleted,
}: DeleteExamineeModalProps) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isHardDelete, setIsHardDelete] = useState(false);
    const { user: currentUser } = useAuth();
    const isAdmin = currentUser?.account?.role === UserRole.ADMIN;

    const handleDelete = async () => {
        setLoading(true);
        setError(null);
        try {
            await deleteExaminee(examinee.id, isHardDelete);
            onExamineeDeleted();
            onClose();
        } catch (err) {
            setError('Failed to delete examinee');
            console.error('Error deleting examinee:', err);
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
                        Delete Examinee
                    </DialogTitle>

                    <div className="space-y-4">
                        <p>
                            Are you sure you want to delete{' '}
                            <span className="font-semibold">
                                {examinee.firstName} {examinee.lastName}
                            </span>
                            ?
                        </p>

                        {hasAssessmentResponses && (
                            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
                                <p className="text-yellow-700">
                                    Warning: This examinee has assessment responses associated with them.
                                    Deleting this examinee may affect related data.
                                </p>
                            </div>
                        )}

                        {isAdmin && (
                            <div className="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="hardDelete"
                                    checked={isHardDelete}
                                    onChange={(e) => setIsHardDelete(e.target.checked)}
                                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                                />
                                <label htmlFor="hardDelete" className="text-sm text-gray-700">
                                    Permanently delete (cannot be undone)
                                </label>
                            </div>
                        )}

                        {error && (
                            <div className="text-red-600 text-sm">{error}</div>
                        )}

                        <div className="flex justify-end space-x-3">
                            <FormButton
                                variant="secondary"
                                onClick={onClose}
                                disabled={loading}
                            >
                                Cancel
                            </FormButton>
                            <FormButton
                                variant="danger"
                                onClick={handleDelete}
                                disabled={loading}
                            >
                                {loading ? 'Deleting...' : 'Delete'}
                            </FormButton>
                        </div>
                    </div>
                </DialogPanel>
            </div>
        </Dialog>
    );
} 