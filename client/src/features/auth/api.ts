import { fetchApi } from '@/lib/api';
import { AuthResponseAPI, LoginCredentialsAPI, UserAPI } from './types/api';
import { transformKeys, toCamelCase } from '@/utils/transformKeys';
import { AuthResponse, User } from './types/client';

export async function login(
    credentials: LoginCredentialsAPI,
): Promise<AuthResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetchApi<AuthResponseAPI>('/auth/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded', // it's what OAuth2PasswordRequestForm expects
        },
        body: formData.toString(),
    });

    return transformKeys(response, toCamelCase) as AuthResponse;
}

export async function logout(token: string): Promise<void> {
    await fetchApi('/auth/logout', {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

export async function getCurrentUser(): Promise<User> {
    const response = await fetchApi<UserAPI>('/users/me');
    return transformKeys(response, toCamelCase) as User;
}

export async function requestPasswordReset(email: string): Promise<void> {
    await fetchApi('/auth/reset-password/request', {
        method: 'POST',
        body: JSON.stringify({ email }),
    });
}

export async function resetPassword(token: string, newPassword: string): Promise<void> {
    await fetchApi('/auth/reset-password/confirm', {
        method: 'POST',
        body: JSON.stringify({ token, password: newPassword }),
    });
}
