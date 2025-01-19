import { fetchApi } from '../../lib/api';
import { Assessment } from './types';

export async function getAssessments(): Promise<Assessment[]> {
  return fetchApi<Assessment[]>('/assessments');
}

export async function getAssessment(id: number): Promise<Assessment> {
  return fetchApi<Assessment>(`/assessments/${id}`);
}

export async function createAssessment(data: Omit<Assessment, 'id' | 'created_at' | 'updated_at' | 'questions'>): Promise<Assessment> {
  return fetchApi<Assessment>('/assessments', {
    method: 'POST',
    body: JSON.stringify(data),
  });
} 