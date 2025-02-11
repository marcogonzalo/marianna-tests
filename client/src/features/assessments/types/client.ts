import { ScoringMethod } from './shared';

export interface Assessment {
    id?: number;
    title: string;
    description?: string;
    minValue?: number;
    maxValue?: number;
    scoringMethod: ScoringMethod;
    createdAt?: string;
    updatedAt?: string;
    questions?: Question[];
}

export interface Question {
    id?: number;
    text: string;
    order?: number;
    createdAt?: string;
    assessmentId: number;
    choices: Choice[];
}

export interface Choice {
    id?: number;
    text: string;
    value: number;
    order?: number;
    createdAt?: string;
    questionId: number;
}

export interface AssessmentResponse {
    id?: number;
    assessmentId?: number;
    status?: 'in_progress' | 'completed' | 'abandoned';
    score?: number;
    createdAt?: string;
    updatedAt?: string;
    questionResponses?: QuestionResponse[];
}

export interface QuestionResponse {
    id?: number;
    assessmentResponseId: number;
    questionId: number;
    numericValue: number;
    createdAt?: string;
}
