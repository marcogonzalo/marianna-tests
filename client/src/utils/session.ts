import { User } from "@/features/users/types";

export const storeSessionData = (token: string, user: User) => {
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('user', JSON.stringify(user));
};

export const getSessionData = () => {
    const token = sessionStorage.getItem('token');
    const user = sessionStorage.getItem('user');
    return { token, user: user ? JSON.parse(user) : null };
};

export const clearSessionData = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
};
