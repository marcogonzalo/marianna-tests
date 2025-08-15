import { fetchApi } from '@/lib/api';
import {
    Assessment,
    AssessmentAPI,
    AssessmentResponse,
    AssessmentResponseAPI,
    CreateAssessmentResponse,
    Question,
    QuestionAPI,
    ResponseStatus,
    Diagnostic,
    DiagnosticAPI,
    AssessmentUpdate,
    AssessmentUpdateAPI,
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

export async function getResponsesToAssessmentes(
    assessmentId: number,
): Promise<AssessmentResponse[]> {
    const data = await fetchApi<AssessmentResponseAPI[]>(
        `/assessments/${assessmentId}/responses`,
    );
    return transformKeys(data, toCamelCase) as AssessmentResponse[];
}

export async function getAssessmentResponse(
    responseId: string,
): Promise<AssessmentResponse> {
    const data = await fetchApi<AssessmentResponse>(`/responses/${responseId}`);
    return transformKeys(data, toCamelCase) as AssessmentResponse;
}

export async function getPublicAssessmentResponse(
    responseId: string,
): Promise<AssessmentResponse> {
    const data = await fetchApi<AssessmentResponse>(`/responses/public/${responseId}`);
    return transformKeys(data, toCamelCase) as AssessmentResponse;
}

export async function createAssessmentResponse(
    assessmentId: number,
    data: CreateAssessmentResponse,
): Promise<AssessmentResponse> {
    const transformedData = transformKeys(
        data,
        toSnakeCase,
    ) as AssessmentResponseAPI;
    const response = await fetchApi<AssessmentResponse>(
        `/assessments/${assessmentId}/responses`,
        {
            method: 'POST',
            body: JSON.stringify(transformedData),
        },
    );
    return transformKeys(response, toCamelCase) as AssessmentResponse;
}

export async function updateAssessmentResponse(
    responseId: string,
    data: AssessmentResponse,
): Promise<AssessmentResponse> {
    const transformedData = transformKeys(
        data,
        toSnakeCase,
    ) as AssessmentResponseAPI;
    const response = await fetchApi<AssessmentResponseAPI>(
        `/responses/${responseId}`,
        {
            method: 'PUT',
            body: JSON.stringify(transformedData),
        },
    );
    return transformKeys(response, toCamelCase) as AssessmentResponse;
}

export async function changeAssessmentResponseStatus(
    responseId: string,
    status: ResponseStatus,
): Promise<AssessmentResponse> {
    const response = await fetchApi<AssessmentResponseAPI>(
        `/responses/${responseId}/change-status`,
        {
            method: 'PATCH',
            body: JSON.stringify({ status }),
        },
    );
    return transformKeys(response, toCamelCase) as AssessmentResponse;
}

export async function getAssessmentResponses(
    examineeId?: string,
): Promise<AssessmentResponse[]> {
    const data = await fetchApi<AssessmentResponseAPI[]>(
        examineeId ? `/responses?examinee_id=${examineeId}` : '/responses',
    );
    return transformKeys(data, toCamelCase) as AssessmentResponse[];
}

export const getDiagnostics = async (
    assessmentId: number,
): Promise<Diagnostic[]> => {
    const data = await fetchApi<DiagnosticAPI[]>(
        `/assessments/${assessmentId}/diagnostics`,
    );
    return transformKeys(data, toCamelCase) as Diagnostic[];
};

export const createDiagnostic = async (
    assessmentId: number,
    diagnostic: Diagnostic,
): Promise<Diagnostic> => {
    const transformedData = transformKeys(
        diagnostic,
        toSnakeCase,
    ) as DiagnosticAPI;
    const data = await fetchApi<DiagnosticAPI>(
        `/assessments/${assessmentId}/diagnostics`,
        {
            method: 'POST',
            body: JSON.stringify(transformedData),
        },
    );
    return transformKeys(data, toCamelCase) as Diagnostic;
};

export async function updateAssessment(
    assessmentId: number,
    data: AssessmentUpdate
): Promise<Assessment> {
    const transformedData = transformKeys(data, toSnakeCase) as AssessmentUpdateAPI;
    const response = await fetchApi<AssessmentAPI>(
        `/assessments/${assessmentId}`,
        {
            method: 'PATCH',
            body: JSON.stringify(transformedData),
        },
    );
    return transformKeys(response, toCamelCase) as Assessment;
}

export async function bulkUpdateQuestions(
    assessmentId: number,
    questions: Question[]
): Promise<Question[]> {
    const transformedData = transformKeys(questions, toSnakeCase) as QuestionAPI[];
    const response = await fetchApi<QuestionAPI[]>(
        `/assessments/${assessmentId}/questions/bulk`,
        {
            method: 'PUT',
            body: JSON.stringify(transformedData),
        },
    );
    return transformKeys(response, toCamelCase) as Question[];
}
