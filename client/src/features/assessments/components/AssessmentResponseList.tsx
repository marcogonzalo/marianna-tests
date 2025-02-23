import React from 'react';
import {
    AssessmentResponse,
    ResponseStatus,
} from '@/features/assessments/types';
interface AssessmentResponseListProps {
    responses: AssessmentResponse[];
    onStatusChange: (id: string, newStatus: ResponseStatus) => void; // Update to use ResponseStatus directly
}

const AssessmentResponseList: React.FC<AssessmentResponseListProps> = ({
    responses,
    onStatusChange,
}) => {
    const handleCopyUrl = (url: string) => {
        navigator.clipboard.writeText(url);
        alert('URL copied to clipboard!');
    };

    return (
        <div className="mt-6">
            <h2 className="text-2xl font-semibold mb-4">
                Assessment Responses
            </h2>
            <table className="min-w-full bg-white border border-gray-200">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border-b">Assessment Name</th>
                        <th className="py-2 px-4 border-b">Status</th>
                        <th className="py-2 px-4 border-b">Copy URL</th>
                        <th className="py-2 px-4 border-b">Created At</th>
                        <th className="py-2 px-4 border-b">Updated At</th>
                    </tr>
                </thead>
                <tbody>
                    {responses.map((response) => (
                        <tr key={response.id}>
                            <td className="py-2 px-4 border-b">
                                {response.assessment?.title}
                            </td>
                            <td className="py-2 px-4 border-b">
                                <select
                                    value={response.status}
                                    onChange={(e) =>
                                        onStatusChange(
                                            response.id,
                                            e.target.value as ResponseStatus,
                                        )
                                    }
                                    className="border rounded p-1"
                                    disabled={
                                        (response.status as ResponseStatus) !==
                                        ResponseStatus.PENDING
                                    }
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
                            <td className="py-2 px-4 border-b">
                                <button
                                    onClick={() =>
                                        handleCopyUrl(
                                            `your-app-url/assessment/${response.id}`,
                                        )
                                    }
                                    className="text-blue-500 hover:underline"
                                >
                                    Copy URL
                                </button>
                            </td>
                            <td className="py-2 px-4 border-b">
                                {new Date(
                                    response.createdAt,
                                ).toLocaleDateString()}
                            </td>
                            <td className="py-2 px-4 border-b">
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
