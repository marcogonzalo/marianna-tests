import { fetchApi } from '@/lib/api';
import { AuthResponseAPI, LoginCredentialsAPI } from './types/api';
import { transformKeys, toCamelCase } from '@/utils/transformKeys';
import { AuthResponse } from './types/client';

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
