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
