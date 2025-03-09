import { useState } from 'react';
import { FormButton, FormInput, FormLabel } from '@/components/ui';
import { Diagnostic } from '@/features/assessments/types/client';
import { Field } from '@headlessui/react';
import TextEditor from '@/components/text-editor';

interface DiagnosticFormProps {
    onSubmit: (diagnostic: Diagnostic) => Promise<void>;
    onCancel: () => void;
    assessmentId: number;
}

export default function DiagnosticForm({
    onSubmit,
    onCancel,
    assessmentId,
}: DiagnosticFormProps) {
    const [description, setDescription] = useState('');
    const [minValue, setMinValue] = useState<number | undefined>();
    const [maxValue, setMaxValue] = useState<number | undefined>();
    const [error, setError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!description.trim()) {
            setError('Description is required');
            return;
        }

        try {
            setIsSubmitting(true);
            setError(null);

            const newDiagnostic: Diagnostic = {
                description,
                minValue,
                maxValue,
                assessmentId,
            };

            await onSubmit(newDiagnostic);

            // Reset form
            setDescription('');
            setMinValue(undefined);
            setMaxValue(undefined);
        } catch (err) {
            setError('Failed to add trait');
            console.error('Error adding trait:', err);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
                Add new trait
            </h3>

            {error && <div className="mb-4 text-red-600 text-sm">{error}</div>}
            <div className="grid grid-cols-2 gap-4">
                <FormInput
                    label="Min Value"
                    type="number"
                    value={minValue !== undefined ? minValue.toString() : ''}
                    onChange={(e) =>
                        setMinValue(
                            e.target.value ? Number(e.target.value) : undefined,
                        )
                    }
                    placeholder="Minimum score"
                />

                <FormInput
                    label="Max Value"
                    type="number"
                    value={maxValue !== undefined ? maxValue.toString() : ''}
                    onChange={(e) =>
                        setMaxValue(
                            e.target.value ? Number(e.target.value) : undefined,
                        )
                    }
                    placeholder="Maximum score"
                />
            </div>
            <Field>
                <FormLabel>Description</FormLabel>
                <TextEditor
                    data={description}
                    onChange={(value) => setDescription(value)}
                />
            </Field>


            <div className="flex justify-end space-x-3 mt-6">
                <FormButton
                    type="button"
                    onClick={onCancel}
                    disabled={isSubmitting}
                >
                    Cancel
                </FormButton>
                <FormButton
                    type="submit"
                    variant="primary"
                    disabled={isSubmitting}
                >
                    {isSubmitting ? 'Saving...' : 'Save trait'}
                </FormButton>
            </div>
        </form>
    );
}
