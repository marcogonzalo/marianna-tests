import { Question as QuestionType } from '../types/client';

export default function Question({ ...question }: QuestionType) {
    return (
        <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-lg">{question.text}</p>
        </div>
    );
}
