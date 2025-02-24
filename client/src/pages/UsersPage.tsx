import { useState, useEffect } from 'react';
import { deleteUser, getUsers } from '@/features/users/api';
import { User } from '@/features/users/types';
import { Page } from '../layouts/components/Page';
import { FormButton } from '@/components/ui';
import { CreateUserModal } from '@/features/users/components/CreateUserModal';

export default function UsersPage() {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

    useEffect(() => {
        const loadUsers = async () => {
            try {
                const data = await getUsers();
                setUsers(data);
                setError(null);
            } catch (err) {
                setError('Failed to load users');
                console.error('Error loading users:', err);
            } finally {
                setLoading(false);
            }
        };

        loadUsers();
    }, []);

    const populateUsers = async () => {
        const data = await getUsers();
        setUsers(data);
    };

    const handleUserCreated = async () => {
        setLoading(true);
        try {
            await populateUsers();
        } catch (err) {
            setError('Failed to reload users');
            console.error(err);
        } finally {
            setLoading(false);
            onCloseModal();
        }
    };

    const handleUserDeleted = async (userId: string) => {
        if (window.confirm('Are you sure you want to delete this user?')) {
            deleteUser(userId)
                .then(() => {
                    populateUsers();
                })
                .catch((err: Error) => {
                    console.error('Error deleting user:', err);
                    setError('Failed to delete user');
                });
        }
    };

    const onCloseModal = () => {
        populateUsers();
        setIsCreateModalOpen(false);
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center">Loading users...</div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center text-red-600">{error}</div>
                </div>
            </div>
        );
    }

    return (
        <Page title="Users">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-semibold">All Users</h3>
                <FormButton
                    variant="primary"
                    onClick={() => setIsCreateModalOpen(true)}
                >
                    Create User
                </FormButton>
            </div>

            <div className="bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl">
                <table className="min-w-full divide-y divide-gray-300">
                    <thead>
                        <tr>
                            <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                                Name
                            </th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                Email
                            </th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                Role
                            </th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                Created At
                            </th>
                            <th className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                                <span className="sr-only">Actions</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {users.map((user) => (
                            <tr
                                key={user.id}
                                className="hover:bg-gray-50 cursor-pointer"
                            >
                                <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                    {user.account?.firstName}{' '}
                                    {user.account?.lastName}
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                    {user.email}
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                    <span className="inline-flex items-center rounded-md px-2 py-1 text-xs font-medium bg-blue-50 text-blue-700 ring-1 ring-inset ring-blue-600/20">
                                        {user.account?.role}
                                    </span>
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                    {new Date(
                                        user.createdAt,
                                    ).toLocaleDateString()}
                                </td>
                                <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                    <FormButton
                                        variant="link"
                                        className="text-red-600 hover:text-red-800"
                                        onClick={() =>
                                            handleUserDeleted(user.id)
                                        }
                                    >
                                        Delete
                                    </FormButton>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <CreateUserModal
                isOpen={isCreateModalOpen}
                onClose={() => onCloseModal()}
                onUserCreated={handleUserCreated}
            />
        </Page>
    );
}
