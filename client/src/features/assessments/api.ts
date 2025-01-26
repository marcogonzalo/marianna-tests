import { fetchApi } from '@/lib/api';
import { Assessment, AssessmentAPI } from '@/features/assessments/types/';
import { transformKeys, toCamelCase, toSnakeCase } from '@/utils/transformKeys';

export async function getAssessments(): Promise<Assessment[]> {
    const data = await fetchApi<AssessmentAPI[]>('/assessments');
    return transformKeys(data, toCamelCase) as Assessment[];
}

export async function getAssessment(id: number): Promise<Assessment> {
    const data = await fetchApi<AssessmentAPI>(`/assessments/${id}`);
    return transformKeys(data, toCamelCase) as Assessment;
}

export async function createAssessment(data: Assessment): Promise<Assessment> {
    const transformedData = transformKeys(data, toSnakeCase) as AssessmentAPI;
    const response = await fetchApi<AssessmentAPI>('/assessments', {
        method: 'POST',
        body: JSON.stringify(transformedData),
    });
    return transformKeys(response, toCamelCase) as Assessment;
}
