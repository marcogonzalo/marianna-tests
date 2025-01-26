import type { AssessmentAPI, QuestionAPI, ChoiceAPI } from './api';
import type { Assessment, Question, Choice } from './client';

export const transformAssessment = (data: AssessmentAPI): Assessment => ({
    ...data,
    minValue: data.min_value,
    maxValue: data.max_value,
    scoringMethod: data.scoring_method,
    createdAt: data.created_at,
    updatedAt: data.updated_at,
    questions: (data.questions ?? []).map(transformQuestion),
});

export const transformQuestion = (data: QuestionAPI): Question => ({
    ...data,
    createdAt: data.created_at,
    assessmentId: data.assessment_id,
    choices: (data.choices ?? []).map(transformChoice),
});

export const transformChoice = (data: ChoiceAPI): Choice => ({
    ...data,
    createdAt: data.created_at,
    questionId: data.question_id,
});
