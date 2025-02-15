import type { UserAPI, AccountAPI } from './api';
import type { User, Account } from './client';

export const transformUser = (data: UserAPI): User => ({
    id: data.id,
    email: data.email,
    createdAt: data.created_at,
    updatedAt: data.updated_at,
    account: data.account ? transformAccount(data.account) : undefined,
});

export const transformAccount = (data: AccountAPI): Account => ({
    id: data.id,
    firstName: data.first_name,
    lastName: data.last_name,
    role: data.role,
    userId: data.user_id,
    createdAt: data.created_at,
    updatedAt: data.updated_at,
});
