import { clearSessionData, getSessionData } from "@/utils/session";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface FetchOptions extends RequestInit {
    body?: string;
}

export async function fetchApi<T>(
    endpoint: string,
    options: FetchOptions = {},
): Promise<T> {
    const { token } = getSessionData();
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        // Clear the token and user data
        clearSessionData();
        
        // Store the current URL to redirect back after login
        const currentPath = window.location.pathname;
        window.location.href = `/login?redirect=${encodeURIComponent(currentPath)}`;
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
}
