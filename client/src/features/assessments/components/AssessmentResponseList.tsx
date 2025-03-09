import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
    AssessmentResponse,
    ResponseStatus,
} from '@/features/assessments/types';
import { FormButton } from '@/components/ui';
import {
    EnvelopeIcon,
    EyeIcon,
    LinkIcon,
} from '@heroicons/react/20/solid';
interface AssessmentResponseListProps {
    responses: AssessmentResponse[];
    onStatusChange: (id: string, newStatus: ResponseStatus) => void; // Update to use ResponseStatus directly
}

const AssessmentResponseList: React.FC<AssessmentResponseListProps> = ({
    responses,
    onStatusChange,
}) => {
    const navigate = useNavigate();

    const handleCopyUrl = (url: string) => {
        navigator.clipboard.writeText(url);
        alert('URL copied to clipboard!');
    };

    return (
        <div className="mt-6 overflow-x-auto">
            <h2 className="text-2xl font-semibold mb-4">
                Assessment Responses
            </h2>
            <table className="min-w-full bg-white border border-gray-200">
                <thead>
                    <tr className="text-center">
                        <th className="py-2 px-4 border-b sticky left-0 bg-white z-1">
                            Assessment Name
                        </th>
                        <th className="py-2 px-4 border-b">Status</th>
                        <th className="py-2 px-4 border-b">Action</th>
                        <th className="py-2 px-4 border-b">Created At</th>
                        <th className="py-2 px-4 border-b">Updated At</th>
                    </tr>
                </thead>
                <tbody>
                    {responses.map((response) => (
                        <tr key={response.id} className="hover:bg-gray-50">
                            <td className="py-2 px-4 border-b sticky left-0 bg-white z-1 hover:bg-gray-50">
                                {response.status ===
                                ResponseStatus.DISCARDED ? (
                                    <s className="text-gray-500">
                                        {response.assessment?.title}
                                    </s>
                                ) : (
                                    response.assessment?.title
                                )}
                            </td>
                            <td className="py-2 px-4 border-b text-center">
                                <select
                                    value={response.status}
                                    onChange={(e) =>
                                        onStatusChange(
                                            response.id,
                                            e.target.value as ResponseStatus,
                                        )
                                    }
                                    className="border rounded p-1"
                                    disabled={[
                                        ResponseStatus.COMPLETED,
                                        ResponseStatus.DISCARDED,
                                    ].includes(
                                        response.status as ResponseStatus,
                                    )}
                                >
                                    {Object.values(ResponseStatus).map(
                                        (status) => (
                                            <option key={status} value={status}>
                                                {status
                                                    .charAt(0)
                                                    .toUpperCase() +
                                                    status
                                                        .slice(1)
                                                        .toLowerCase()}
                                            </option>
                                        ),
                                    )}
                                </select>
                            </td>
                            <td className="py-2 px-4 border-b text-center">
                                {response.status === ResponseStatus.PENDING && (
                                    <>
                                        <FormButton
                                            title='Copy link'
                                            onClick={() =>
                                                handleCopyUrl(
                                                    `${window.location.origin}/private-response/${response.id}`,
                                                )
                                            }
                                            variant="link"
                                        >
                                            <LinkIcon className="h-5 w-5" />
                                        </FormButton>
                                    </>
                                )}
                                {response.status ===
                                    ResponseStatus.COMPLETED && (
                                    <FormButton
                                        title='View response'
                                        onClick={() =>
                                            navigate(
                                                `/responses/${response.id}`,
                                            )
                                        }
                                        variant="link"
                                    >
                                        <EyeIcon className="h-5 w-5" />
                                    </FormButton>
                                )}
                            </td>
                            <td className="py-2 px-4 border-b text-center">
                                {new Date(
                                    response.createdAt,
                                ).toLocaleDateString()}
                            </td>
                            <td className="py-2 px-4 border-b text-center">
                                {new Date(
                                    response.updatedAt,
                                ).toLocaleDateString()}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AssessmentResponseList;
