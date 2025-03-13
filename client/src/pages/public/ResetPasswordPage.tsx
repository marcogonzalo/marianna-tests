import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { FormButton, FormInput } from '@/components/ui';
import { resetPassword } from '@/features/auth/api';

export default function ResetPasswordPage() {
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const token = searchParams.get('token');

    if (!token) {
        return (
            <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                    <div className="text-red-500 text-center">
                        Invalid or missing reset token. Please request a new password reset.
                    </div>
                </div>
            </div>
        );
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        setIsSubmitting(true);
        setError('');

        try {
            await resetPassword(token, password);
            navigate('/login', { 
                state: { message: 'Password has been reset successfully. Please login with your new password.' }
            });
        } catch (err) {
            setError('Failed to reset password. The link may have expired. Please request a new reset link.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                    Set new password
                </h2>
            </div>

            <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                <form className="space-y-6" onSubmit={handleSubmit}>
                    {error && (
                        <div className="text-red-500 text-center text-sm">{error}</div>
                    )}
                    <FormInput
                        id="password"
                        name="password"
                        label="New password"
                        type="password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <FormInput
                        id="confirmPassword"
                        name="confirmPassword"
                        label="Confirm new password"
                        type="password"
                        required
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                    />

                    <div>
                        <FormButton
                            type="submit"
                            disabled={isSubmitting}
                            className="w-full"
                        >
                            {isSubmitting ? 'Resetting...' : 'Reset password'}
                        </FormButton>
                    </div>
                </form>
            </div>
        </div>
    );
} 