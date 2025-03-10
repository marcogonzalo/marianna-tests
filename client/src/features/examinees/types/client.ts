import { Gender } from './shared';

export interface ListedExaminee {
    id: string;
    firstName: string;
    lastName: string;
    internalIdentifier: string;
    createdAt: string; // Adjust the type based on your API response
}

export interface Examinee {
    id: string;
    firstName: string;
    middleName?: string;
    lastName: string;
    gender: Gender;
    birthDate: Date;
    email: string;
    internalIdentifier?: string;
    createdBy: string;
    comments?: string;
    createdAt: string; // Adjust the type based on your API response
}

export interface CreateExamineeRequest {
    firstName: string;
    middleName?: string;
    lastName: string;
    gender: Gender;
    birthDate: Date;
    email: string;
    internalIdentifier?: string;
    comments?: string;
}

export interface UpdateExamineeRequest {
    firstName: string;
    middleName?: string;
    lastName: string;
    gender: Gender;
    birthDate: Date;
    email: string;
    internalIdentifier?: string;
    comments?: string;
}
