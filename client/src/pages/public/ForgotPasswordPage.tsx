import { useState } from 'react';
import { Link } from 'react-router-dom';
import { FormButton, FormInput } from '@/components/ui';
import { requestPasswordReset } from '@/features/auth/api';

export default function ForgotPasswordPage() {
    const [email, setEmail] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError('');
        setMessage('');

        try {
            await requestPasswordReset(email);
            setMessage('If an account exists with this email, you will receive password reset instructions.');
            setEmail('');
        } catch (err) {
            setError('An error occurred while processing your request. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                    Reset your password
                </h2>
                <p className="mt-2 text-center text-sm text-gray-600">
                    Enter your email address and we'll send you instructions to reset your password.
                </p>
            </div>

            <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                <form className="space-y-6" onSubmit={handleSubmit}>
                    {error && (
                        <div className="text-red-500 text-center text-sm">{error}</div>
                    )}
                    {message && (
                        <div className="text-green-500 text-center text-sm">{message}</div>
                    )}
                    <FormInput
                        id="email"
                        name="email"
                        label="Email address"
                        type="email"
                        autoComplete="email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <div>
                        <FormButton
                            type="submit"
                            disabled={isSubmitting}
                            className="w-full"
                        >
                            {isSubmitting ? 'Sending...' : 'Send reset instructions'}
                        </FormButton>
                    </div>

                    <div className="text-sm text-center">
                        <Link
                            to="/login"
                            className="font-medium text-indigo-600 hover:text-indigo-500"
                        >
                            Back to login
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
} 