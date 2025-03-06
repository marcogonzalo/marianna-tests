import { useEffect, useState } from 'react';
import { FormButton } from '@/components/ui';
import { getDiagnostics, createDiagnostic } from '@/features/assessments/api';
import { Diagnostic } from '@/features/assessments/types/client';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';
import DiagnosticList from './DiagnosticList';
import DiagnosticForm from './DiagnosticForm';

interface DiagnosticsModalProps {
    isOpen: boolean;
    onClose: () => void;
    assessmentId: number;
}

export function DiagnosticsModal({
    isOpen,
    onClose,
    assessmentId,
}: DiagnosticsModalProps) {
    const [diagnostics, setDiagnostics] = useState<Diagnostic[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isAddingDiagnostic, setIsAddingDiagnostic] = useState(false);

    const fetchDiagnostics = async () => {
        try {
            setLoading(true);
            const data = await getDiagnostics(assessmentId);
            setDiagnostics(data);
            setError(null);
        } catch (err) {
            setError('Failed to load traits');
            console.error('Error loading traits:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (isOpen) {
            fetchDiagnostics();
        }
    }, [isOpen, assessmentId]);

    const handleAddDiagnostic = async (diagnostic: Diagnostic) => {
        await createDiagnostic(assessmentId, diagnostic);
        setIsAddingDiagnostic(false);
        await fetchDiagnostics();
    };

    return (
        <Dialog open={isOpen} onClose={onClose} className="relative z-50">
            <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
            <div className="fixed inset-0 flex items-center justify-center p-4">
                <DialogPanel className="mx-auto max-w-md rounded-xl bg-white p-6 shadow-xl w-full">
                    <DialogTitle className="text-lg font-medium mb-4">
                        Assessment traits
                    </DialogTitle>
                    
                    {error && !isAddingDiagnostic && (
                        <div className="mb-4 text-red-600 text-sm">{error}</div>
                    )}
                    
                    {!isAddingDiagnostic ? (
                        <>
                            <DiagnosticList 
                                diagnostics={diagnostics}
                                isLoading={loading}
                                error={error}
                            />
                            
                            <div className="flex justify-between mt-4">
                                <FormButton 
                                    variant="primary" 
                                    onClick={() => setIsAddingDiagnostic(true)}
                                >
                                    Add trait
                                </FormButton>
                                <FormButton variant="secondary" onClick={onClose}>
                                    Close
                                </FormButton>
                            </div>
                        </>
                    ) : (
                        <DiagnosticForm 
                            onSubmit={handleAddDiagnostic}
                            onCancel={() => setIsAddingDiagnostic(false)}
                            assessmentId={assessmentId}
                        />
                    )}
                </DialogPanel>
            </div>
        </Dialog>
    );
}

export default DiagnosticsModal; 