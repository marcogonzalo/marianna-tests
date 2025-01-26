import { ScoringMethod } from './shared';

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
