import { fetchApi } from '@/lib/api';
import {
    Assessment,
    AssessmentAPI,
    Question,
    QuestionAPI,
    ChoiceAPI,
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

    // Process choices
    for (const choice of data.choices) {
        const transformedChoice = transformKeys(
            choice,
            toSnakeCase,
        ) as ChoiceAPI;
        if (choice.id) {
            await fetchApi<ChoiceAPI>(
                `/assessments/${data.assessmentId}/questions/${data.id}/choices/${choice.id}`,
                {
                    method: 'PUT',
                    body: JSON.stringify(transformedChoice),
                },
            );
        } else {
            await fetchApi<ChoiceAPI>(
                `/assessments/${data.assessmentId}/questions/${data.id}/choices`,
                {
                    method: 'POST',
                    body: JSON.stringify(transformedChoice),
                },
            );
        }
    }

    return updatedQuestion;
}
