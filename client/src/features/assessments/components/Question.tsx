import { Question as QuestionType } from '../types/client';
import ChoiceList from './ChoiceList';

export default function Question({ ...question }: QuestionType) {
    return (
        <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-lg">{question.text}</p>
            <ChoiceList
                choices={question.choices}
                name={`question-${question.id}`}
            />
        </div>
    );
}
