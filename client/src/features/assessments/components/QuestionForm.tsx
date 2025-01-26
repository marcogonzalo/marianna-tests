import { FormButton, FormInput } from '@/components/ui';
import { Question } from '../types/client';
import { useState } from 'react';

interface QuestionFormProps extends Question {
    onSave?: (question: Question) => void;
}

export default function QuestionForm({
    onSave,
    ...question
}: QuestionFormProps) {
    const [text, setText] = useState(question.text);
    const [order, setOrder] = useState(question.order || 0);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (onSave) onSave({ ...question, text, order });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-8 gap-4">
                <FormInput
                    label="Question Text"
                    id="questionText"
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    blockClassName="col-span-6"
                />
                <FormInput
                    label="Order"
                    type="number"
                    value={order}
                    onChange={(e) => setOrder(Number(e.target.value))}
                />
                <FormButton
                    type="submit"
                    variant="secondary"
                    className="self-end"
                >
                    Save
                </FormButton>
            </div>
        </form>
    );
}
