import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { ScoringMethod } from '@/features/assessments/types/shared';
import { Page } from '../layouts/components/Page';
import {
    FormButton,
    FormInput,
    FormTextarea,
    FormSelect,
} from '@/components/ui';
import { createAssessment } from '@/features/assessments/api';

interface AssessmentForm {
    title: string;
    description: string;
    scoringMethod: ScoringMethod;
    minValue: number;
    maxValue: number;
}

const initialForm: AssessmentForm = {
    title: '',
    description: '',
    scoringMethod: ScoringMethod.BOOLEAN,
    minValue: 0,
    maxValue: 1,
};

export default function CreateAssessmentPage() {
    const navigate = useNavigate();
    const [form, setForm] = useState<AssessmentForm>(initialForm);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        const assessment = await createAssessment(form);
        setIsSubmitting(false);
        navigate(`/assessments/${assessment.id}`);
    };

    const handleScoringMethodChange = (method: ScoringMethod) => {
        let min = 0;
        let max = 1;

        if (method === ScoringMethod.SCORED) {
            min = -1;
            max = 1;
        }

        setForm((prev) => ({
            ...prev,
            scoringMethod: method,
            minValue: min,
            maxValue: max,
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
                    disabled={isSubmitting}
                >
                    Back to Assessments
                </FormButton>
            </div>

            <form
                onSubmit={handleSubmit}
                className="card"
            >
                <div className="space-y-6 bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl p-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Left Column */}
                        <div className="space-y-6">
                            <div>
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

                            <div>
                                <FormSelect
                                    label="Scoring Method"
                                    id="scoringMethod"
                                    value={form.scoringMethod}
                                    onChange={(e) =>
                                        handleScoringMethodChange(
                                            e.target.value as ScoringMethod,
                                        )
                                    }
                                >
                                    {Object.values(ScoringMethod).map(
                                        (method) => (
                                            <option key={method} value={method}>
                                                {method ===
                                                ScoringMethod.BOOLEAN
                                                    ? 'Boolean (0-1)'
                                                    : method ===
                                                      ScoringMethod.SCORED
                                                    ? 'Scored (-1 to 1)'
                                                    : 'Custom Range'}
                                            </option>
                                        ),
                                    )}
                                </FormSelect>

                                {form.scoringMethod === 'custom' && (
                                    <div className="grid grid-cols-2 gap-4 mt-4">
                                        <FormInput
                                            label="Minimum value"
                                            id="minValue"
                                            type="number"
                                            value={form.minValue}
                                            onChange={(e) =>
                                                setForm((prev) => ({
                                                    ...prev,
                                                    minValue: Number(
                                                        e.target.value,
                                                    ),
                                                }))
                                            }
                                            required
                                        />
                                        <FormInput
                                            label="Maximum value"
                                            id="maxValue"
                                            type="number"
                                            value={form.maxValue}
                                            onChange={(e) =>
                                                setForm((prev) => ({
                                                    ...prev,
                                                    maxValue: Number(
                                                        e.target.value,
                                                    ),
                                                }))
                                            }
                                            required
                                        />
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Right Column */}
                        <div className="h-full">
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
                                rows={12}
                                className="h-full"
                            />
                        </div>
                    </div>
                </div>

                <div className="mt-4 flex items-center justify-end gap-x-6">
                    <FormButton
                        variant="secondary"
                        type="button"
                        onClick={() => navigate('/assessments')}
                        className='className="text-sm/6 font-semibold text-gray-900'
                        disabled={isSubmitting}
                    >
                        Cancel
                    </FormButton>
                    <FormButton
                        variant="primary"
                        type="submit"
                        className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                        disabled={isSubmitting}
                    >
                        Create Assessment
                    </FormButton>
                </div>
            </form>
        </Page>
    );
}
