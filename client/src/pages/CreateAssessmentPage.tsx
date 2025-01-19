import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { ScoringMethod } from '@/features/assessments/types';
import Button from '@/components/ui/Button';
import { Page } from '@/layouts/Page';

interface AssessmentForm {
    title: string;
    description: string;
    scoring_method: ScoringMethod;
    min_value: number;
    max_value: number;
}

const initialForm: AssessmentForm = {
    title: '',
    description: '',
    scoring_method: 'boolean',
    min_value: 0,
    max_value: 1,
};

export default function CreateAssessmentPage() {
    const navigate = useNavigate();
    const [form, setForm] = useState<AssessmentForm>(initialForm);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        // TODO: Implement API call
        console.log('Form submitted:', form);
    };

    const handleScoringMethodChange = (method: ScoringMethod) => {
        let min = 0;
        let max = 1;

        if (method === 'scored') {
            min = -1;
            max = 1;
        }

        setForm((prev) => ({
            ...prev,
            scoring_method: method,
            min_value: min,
            max_value: max,
        }));
    };

    return (
        <Page title="Create Assessment">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <p className="mt-1 text-sm text-gray-500">
                        Add a new assessment to your collection.
                    </p>
                </div>
                <Button
                    variant="secondary"
                    onClick={() => navigate('/assessments')}
                >
                    Back to Assessments
                </Button>
            </div>

            <form
                onSubmit={handleSubmit}
                className="card divide-y divide-gray-200"
            >
                <div className="p-6 space-y-6">
                    <div>
                        <label
                            htmlFor="title"
                            className="block text-sm font-medium text-gray-700"
                        >
                            Title
                        </label>
                        <input
                            id="title"
                            type="text"
                            value={form.title}
                            onChange={(e) =>
                                setForm((prev) => ({
                                    ...prev,
                                    title: e.target.value,
                                }))
                            }
                            className="input mt-1"
                            required
                        />
                    </div>

                    <div>
                        <label
                            htmlFor="description"
                            className="block text-sm font-medium text-gray-700"
                        >
                            Description
                        </label>
                        <textarea
                            id="description"
                            value={form.description}
                            onChange={(e) =>
                                setForm((prev) => ({
                                    ...prev,
                                    description: e.target.value,
                                }))
                            }
                            className="input mt-1 min-h-[100px]"
                            rows={4}
                        />
                    </div>

                    <div>
                        <label
                            htmlFor="scoring_method"
                            className="block text-sm font-medium text-gray-700"
                        >
                            Scoring Method
                        </label>
                        <select
                            id="scoring_method"
                            value={form.scoring_method}
                            onChange={(e) =>
                                handleScoringMethodChange(
                                    e.target.value as ScoringMethod,
                                )
                            }
                            className="input mt-1"
                        >
                            <option value="boolean">Boolean (0-1)</option>
                            <option value="scored">Scored (-1 to 1)</option>
                            <option value="custom">Custom Range</option>
                        </select>
                    </div>

                    {form.scoring_method === 'custom' && (
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label
                                    htmlFor="min_value"
                                    className="block text-sm font-medium text-gray-700"
                                >
                                    Minimum Value
                                </label>
                                <input
                                    id="min_value"
                                    type="number"
                                    value={form.min_value}
                                    onChange={(e) =>
                                        setForm((prev) => ({
                                            ...prev,
                                            min_value: Number(e.target.value),
                                        }))
                                    }
                                    className="input mt-1"
                                    required
                                />
                            </div>
                            <div>
                                <label
                                    htmlFor="max_value"
                                    className="block text-sm font-medium text-gray-700"
                                >
                                    Maximum Value
                                </label>
                                <input
                                    id="max_value"
                                    type="number"
                                    value={form.max_value}
                                    onChange={(e) =>
                                        setForm((prev) => ({
                                            ...prev,
                                            max_value: Number(e.target.value),
                                        }))
                                    }
                                    className="input mt-1"
                                    required
                                />
                            </div>
                        </div>
                    )}
                </div>

                <div className="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-end gap-3">
                    <Button
                        variant="secondary"
                        type="button"
                        onClick={() => navigate('/assessments')}
                    >
                        Cancel
                    </Button>
                    <Button variant="primary" type="submit">
                        Create Assessment
                    </Button>
                </div>
            </form>
        </Page>
    );
}
