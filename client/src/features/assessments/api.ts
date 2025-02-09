import { fetchApi } from '@/lib/api';
import {
    Assessment,
    AssessmentAPI,
    Question,
    QuestionAPI,
} from '@/features/assessments/types/';
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

export async function createQuestion(data: Question): Promise<Question> {
    const transformedData = transformKeys(data, toSnakeCase) as QuestionAPI;
    const response = await fetchApi<QuestionAPI>(
        `/assessments/${data.assessmentId}/questions`,
        {
            method: 'POST',
            body: JSON.stringify(transformedData),
        },
    );
    return transformKeys(response, toCamelCase) as Question;
}

export async function updateQuestion(data: Question): Promise<Question> {
    const transformedData = transformKeys(data, toSnakeCase) as QuestionAPI;
    const response = await fetchApi<QuestionAPI>(
        `/assessments/${data.assessmentId}/questions/${data.id}`,
        {
            method: 'PUT',
            body: JSON.stringify(transformedData),
        },
    );
    const updatedQuestion = transformKeys(response, toCamelCase) as Question;

    return updatedQuestion;
}

export async function deleteQuestion(
    assessmentId: number,
    questionId: number,
): Promise<void> {
    await fetchApi(`/assessments/${assessmentId}/questions/${questionId}`, {
        method: 'DELETE',
    });
}
