import { fetchApi } from '@/lib/api';
import { User, CreateUserRequest, UpdateUserRequest, Account } from './types/client';
import { AccountAPI, UserAPI, UserAPIRequest, UserUpdateAPI } from './types/api';
import { transformKeys, toCamelCase, toSnakeCase } from '@/utils/transformKeys';
import { UserRole } from './types';

export async function getUsers(): Promise<User[]> {
    const response = await fetchApi<UserAPI[]>('/users');
    return transformKeys(response, toCamelCase) as User[];
}

export async function getUser(id: string): Promise<User> {
    const response = await fetchApi<UserAPI>(`/users/${id}`);
    return transformKeys(response, toCamelCase) as User;
}

export async function getAccount(id: string): Promise<Account> {
    const response = await fetchApi<AccountAPI>(`/accounts/${id}`);
    return transformKeys(response, toCamelCase) as Account;
}

export async function createUser(data: CreateUserRequest): Promise<User> {
    const transformedData = transformKeys(data, toSnakeCase) as UserAPIRequest;
    const response = await fetchApi<UserAPIRequest>('/users', {
        method: 'POST',
        body: JSON.stringify(transformedData),
    });
    return transformKeys(response, toCamelCase) as User;
}

export async function updateUser(
    id: string,
    data: UpdateUserRequest,
): Promise<User> {
    console.log("*********", data);
    const transformedData = transformKeys(data, toSnakeCase) as UserUpdateAPI;
    console.log("*********", transformedData);
    const response = await fetchApi<UserAPI>(`/users/${id}`, {
        method: 'PUT',
        body: JSON.stringify(transformedData),
    });
    console.log("*********", response);
    return transformKeys(response, toCamelCase) as User;
}

export async function deleteUser(id: string): Promise<void> {
    await fetchApi(`/users/${id}`, {
        method: 'DELETE',
    });
}

export const restoreUser = async (userId: string): Promise<void> => {
    await fetchApi(`/users/${userId}/restore`, {
        method: 'POST',
    });
};
