import { ResponseStatus, ScoringMethod } from './shared';

export interface AssessmentAPI {
    id?: number;
    title: string;
    description?: string;
    min_value?: number;
    max_value?: number;
    scoring_method: ScoringMethod;
    created_at?: string;
    updated_at?: string;
    questions?: QuestionAPI[];
}


export interface AssessmentUpdateAPI {
    title: string;
    description?: string;
}

export interface DiagnosticAPI {
    id?: number;
    assessment_id?: number;
    min_value?: number;
    max_value?: number;
    description: string;
}

export interface QuestionAPI {
    id?: number;
    text: string;
    order?: number;
    created_at?: string;
    assessment_id: number;
    choices?: ChoiceAPI[];
}

export interface ChoiceAPI {
    id?: number;
    text: string;
    value: number;
    order?: number;
    created_at?: string;
    question_id: number;
}

export interface AssessmentResponseAPI {
    id?: number;
    assessment_id: number;
    assessment?: AssessmentAPI;
    status: ResponseStatus;
    examinee_id?: string;
    score?: number;
    created_at: string;
    updated_at?: string;
    question_responses?: QuestionResponseAPI[];
}

export interface QuestionResponseAPI {
    id?: number;
    assessment_response_id: number;
    question_id: number;
    numeric_value: number;
    created_at?: string;
}
