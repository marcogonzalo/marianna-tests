export type ScoringMethod = 'boolean' | 'scored' | 'custom';

export interface Assessment {
  id: number;
  title: string;
  description?: string;
  min_value: number;
  max_value: number;
  scoring_method: ScoringMethod;
  created_at: string;
  updated_at: string;
  questions: Question[];
}

export interface Question {
  id: number;
  text: string;
  order: number;
  created_at: string;
  assessment_id: number;
  choices: Choice[];
}

export interface Choice {
  id: number;
  text: string;
  value: number;
  order: number;
  created_at: string;
  question_id: number;
} 