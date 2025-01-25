import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { ScoringMethod } from '@/features/assessments/types';
import FormButton from '../components/ui/FormButton';
import { Page } from '@/layouts/Page';
import { FormInput, FormTextarea, FormSelect } from '../components/ui';

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
                <FormButton
                    variant="secondary"
                    onClick={() => navigate('/assessments')}
                >
                    Back to Assessments
                </FormButton>
            </div>

            <form
                onSubmit={handleSubmit}
                className="card divide-y divide-gray-200"
            >
                <div className="p-6 space-y-6">
                    <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                        <div className="sm:col-span-4">
                            <div className="mt-2">
                                <FormInput
                                    label="Title"
                                    id="title"
                                    type="text"
                                    value={form.title}
                                    onChange={(e) =>
                                        setForm((prev) => ({
                                            ...prev,
                                            title: e.target.value,
                                        }))
                                    }
                                    required
                                />
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <FormTextarea
                                label="Description"
                                id="description"
                                value={form.description}
                                onChange={(e) =>
                                    setForm((prev) => ({
                                        ...prev,
                                        description: e.target.value,
                                    }))
                                }
                                rows={4}
                            />
                        </div>

                        <div className="sm:col-span-4">
                            <FormSelect
                                label="Scoring Method"
                                id="scoring_method"
                                value={form.scoring_method}
                                onChange={(e) =>
                                    handleScoringMethodChange(
                                        e.target.value as ScoringMethod,
                                    )
                                }
                            >
                                <option value="boolean">Boolean (0-1)</option>
                                <option value="scored">Scored (-1 to 1)</option>
                                <option value="custom">Custom Range</option>
                            </FormSelect>
                        </div>

                        {form.scoring_method === 'custom' && (
                            <div className="sm:col-span-4 grid grid-cols-2 gap-4">
                                <FormInput
                                    label="Minimum value"
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
                                <FormInput
                                    label="Maximum value"
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
                        )}
                    </div>
                </div>

                <div className="mt-6 flex items-center justify-end gap-x-6">
                    <FormButton
                        variant="secondary"
                        type="button"
                        onClick={() => navigate('/assessments')}
                        className='className="text-sm/6 font-semibold text-gray-900'
                    >
                        Cancel
                    </FormButton>
                    <FormButton
                        variant="primary"
                        type="submit"
                        className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    >
                        Create Assessment
                    </FormButton>
                </div>
            </form>
        </Page>
    );
}
