import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { FormButton, FormInput } from '@/components/ui';

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    const auth = useAuth();

    const from = location.state?.from?.pathname || '/examinees';

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await auth.login(username, password);
            navigate(from, { replace: true });
        } catch {
            setError('Invalid email or password');
        }
    };

    return (
        <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                    Sign in to your account
                </h2>
            </div>

            <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                <form className="space-y-6" onSubmit={handleSubmit}>
                    {error && (
                        <div className="text-red-500 text-center">{error}</div>
                    )}
                    <FormInput
                        id="username"
                        name="email"
                        label="Username"
                        type="email"
                        required
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <FormInput
                        id="password"
                        name="password"
                        label="Password"
                        type="password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <FormButton type="submit" className="w-full">
                        Sign in
                    </FormButton>
                </form>
            </div>
        </div>
    );
}
