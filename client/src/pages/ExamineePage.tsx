import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getExaminee } from '@/features/examinees/api'; // Assume this function fetches an examinee by ID
import { Examinee } from '@/features/examinees/types'; // Assume this type is defined in a types file
import { Page } from '../layouts/components/Page';
import { FormButton } from '@/components/ui';
import { AssignAssessmentModal } from '@/features/assessments/components/AssignAssessmentModal';
import AssessmentResponseList from '@/features/assessments/components/AssessmentResponseList';
import {
    changeAssessmentResponseStatus,
    getAssessmentResponses,
} from '@/features/assessments/api'; // Import the new function
import {
    AssessmentResponse,
    ResponseStatus,
} from '@/features/assessments/types';

export default function ExamineeDetailPage() {
    const { id } = useParams<{ id: string }>();
    const [examinee, setExaminee] = useState<Examinee | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isAssignModalOpen, setIsAssignModalOpen] = useState(false);
    const [assessmentResponses, setAssessmentResponses] = useState<
        AssessmentResponse[]
    >([]);

    useEffect(() => {
        const fetchExaminee = async () => {
            try {
                if (!id) throw new Error('Examinee ID is required');
                const data = await getExaminee(id);
                setExaminee(data);
                setError(null);
            } catch (err) {
                setError('Failed to load examinee data');
                console.error('Error loading examinee data:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchExaminee();
    }, [id]);

    useEffect(() => {
        fetchAssessmentResponses();
    }, [examinee]);

    const fetchAssessmentResponses = async () => {
        if (examinee) {
            try {
                const responses = await getAssessmentResponses(examinee.id);
                setAssessmentResponses(responses);
            } catch (err) {
                console.error('Error loading assessment responses:', err);
            }
        }
    };

    const handleOpenModal = () => {
        setIsAssignModalOpen(true);
    };

    const handleCloseModal = (assessmentResponse: AssessmentResponse | null) => {
        if (assessmentResponse) {
            setAssessmentResponses((prevResponses) => [
                ...prevResponses,
                assessmentResponse,
            ]);
        }
        setIsAssignModalOpen(false);
    };

    if (loading) {
        return (
            <Page title="Examinee Details">
                <div className="min-h-screen bg-gray-50 py-8">
                    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                        <div className="text-center">
                            Loading examinee data...
                        </div>
                    </div>
                </div>
            </Page>
        );
    }

    if (error || !examinee) {
        return (
            <Page title="Examinee Details">
                <div className="min-h-screen bg-gray-50 py-8">
                    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                        <div className="text-center text-red-600">{error}</div>
                    </div>
                </div>
            </Page>
        );
    }

    async function handleStatusChange(
        id: string,
        newStatus: ResponseStatus,
    ): Promise<void> {
        try {
            await changeAssessmentResponseStatus(id, newStatus);
            setAssessmentResponses((prevResponses) =>
                prevResponses.map((response) =>
                    response.id === id
                        ? { ...response, status: newStatus }
                        : response,
                ),
            );
        } catch (err) {
            console.error('Error updating assessment response status:', err);
            alert('Error updating assessment response status');
        }
    }

    return (
        <Page title={`Examinee: ${examinee.firstName} ${examinee.lastName}`}>
            <div className="min-h-screen bg-gray-50 py-8">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="bg-white shadow-sm rounded-lg p-6">
                        <h2 className="text-2xl font-semibold mb-4">
                            Examinee Details
                        </h2>
                        <div className="grid grid-cols-2">
                            <div className="">
                                <div>
                                    <strong>Name:</strong> {examinee.firstName}{' '}
                                    {examinee.middleName} {examinee.lastName}
                                </div>
                                <div>
                                    <strong>Gender:</strong> {examinee.gender}
                                </div>
                                <div>
                                    <strong>Birth Date:</strong>{' '}
                                    {new Date(
                                        examinee.birthDate,
                                    ).toLocaleDateString()}
                                </div>
                                <div>
                                    <strong>Email:</strong> {examinee.email}
                                </div>
                            </div>
                            <div className="">
                                <div>
                                    <strong>Internal Identifier:</strong>{' '}
                                    {examinee.internalIdentifier}
                                </div>
                                <div>
                                    <strong>Created By:</strong>{' '}
                                    {examinee.created_by}
                                </div>
                                <div>
                                    <strong>Comments:</strong>{' '}
                                    {examinee.comments}
                                </div>
                            </div>
                        </div>
                        <div className="mt-6">
                            <FormButton
                                variant="primary"
                                onClick={handleOpenModal}
                            >
                                Assign Assessment
                            </FormButton>
                        </div>
                    </div>
                </div>
                <AssessmentResponseList
                    responses={assessmentResponses} // Assuming this is the structure of your examinee data
                    onStatusChange={handleStatusChange} // Define this function to handle status changes
                />
            </div>
            <AssignAssessmentModal
                isOpen={isAssignModalOpen}
                onClose={handleCloseModal}
                examineeId={examinee.id}
            />
        </Page>
    );
}
