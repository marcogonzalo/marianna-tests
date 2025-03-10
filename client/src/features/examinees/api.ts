import { fetchApi } from '@/lib/api';
import { transformKeys, toSnakeCase, toCamelCase } from '@/utils/transformKeys';
import {
    Examinee,
    CreateExamineeRequest,
    UpdateExamineeRequest,
    ExamineeAPI,
    ExamineeAPIRequest,
} from './types';

export async function getExaminees(): Promise<Examinee[]> {
    const response = await fetchApi<ExamineeAPI[]>('/examinees');
    return transformKeys(response, toCamelCase) as Examinee[];
}

export async function getExaminee(id: string): Promise<Examinee> {
    const response = await fetchApi<ExamineeAPI>(`/examinees/${id}`);
    return transformKeys(response, toCamelCase) as Examinee;
}

export async function createExaminee(
    data: CreateExamineeRequest,
): Promise<Examinee> {
    const transformedData = transformKeys(
        data,
        toSnakeCase,
    ) as ExamineeAPIRequest;
    const response = await fetchApi<Examinee>('/examinees', {
        method: 'POST',
        body: JSON.stringify(transformedData),
    });
    return transformKeys(response, toCamelCase) as Examinee;
}

export async function updateExaminee(
    id: string,
    data: UpdateExamineeRequest,
): Promise<Examinee> {
    const transformedData = transformKeys(data, toSnakeCase) as ExamineeAPI;
    const response = await fetchApi<ExamineeAPI>(`/examinees/${id}`, {
        method: 'PUT',
        body: JSON.stringify(transformedData),
    });
    return transformKeys(response, toCamelCase) as Examinee;
}

export async function deleteExaminee(id: string): Promise<void> {
    await fetchApi(`/examinees/${id}`, {
        method: 'DELETE',
    });
}
