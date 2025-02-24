import { useEffect, useState } from 'react';
import { getExaminees } from '@/features/examinees/api'; // Assume this function fetches examinees from the API
import { Examinee } from '@/features/examinees/types'; // Assume this type is defined in a types file
import { Link } from 'react-router-dom';
import { Page } from '../layouts/components/Page';
import { FormButton } from '@/components/ui';
import CreateExamineeModal from '@/features/examinees/components/CreateExamineeModal';

export default function ExamineesPage() {
    const [examinees, setExaminees] = useState<Examinee[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

    useEffect(() => {
        const loadExaminees = async () => {
            try {
                const data = await getExaminees();
                setExaminees(data);
                setError(null);
            } catch (err) {
                setError('Failed to load users');
                console.error('Error loading users:', err);
            } finally {
                setLoading(false);
            }
        };
        loadExaminees();
    }, []);

    const populateExaminees = async () => {
        const data = await getExaminees();
        setExaminees(data);
    };

    const handleExamineeCreated = async () => {
        setLoading(true);
        try {
            await populateExaminees();
        } catch (err) {
            setError('Failed to reload examinees');
            console.error(err);
        } finally {
            setLoading(false);
            onCloseModal();
        }
    };

    const onCloseModal = () => {
        populateExaminees();
        setIsCreateModalOpen(false);
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center">Loading examinees...</div>
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
        <Page title="Examinees">
            <div className="flex justify-between items-center mb-6">
                <FormButton
                    variant="primary"
                    onClick={() => setIsCreateModalOpen(true)}
                >
                    Create Examinee
                </FormButton>
            </div>
            <div className="bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl">
                <table className="min-w-full divide-y divide-gray-300">
                    <thead>
                        <tr>
                            <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                                ID
                            </th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                First Name
                            </th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                Last Name
                            </th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                Internal Identifier
                            </th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                Created At
                            </th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {examinees.map((examinee) => (
                            <tr
                                key={examinee.id}
                                className="hover:bg-gray-50 cursor-pointer"
                            >
                                <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                    {examinee.id}
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                    {examinee.firstName}
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                    {examinee.lastName}
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                    {examinee.internalIdentifier}
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                    {new Date(
                                        examinee.createdAt,
                                    ).toLocaleString()}
                                </td>
                                <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                    <Link
                                        to={`/examinees/${examinee.id}`}
                                        className="text-blue-500 hover:underline"
                                    >
                                        View
                                    </Link>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <CreateExamineeModal
                isOpen={isCreateModalOpen}
                onClose={() => onCloseModal()}
                onExamineeCreated={handleExamineeCreated}
            />
        </Page>
    );
}
