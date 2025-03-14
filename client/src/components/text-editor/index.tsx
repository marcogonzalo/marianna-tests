import { CKEditor } from '@ckeditor/ckeditor5-react';
import { ClassicEditor, Essentials, Paragraph, Bold, Italic, Markdown } from 'ckeditor5';


import 'ckeditor5/ckeditor5.css';

interface TextEditorProps {
    data: string;
    onChange: (value: string) => void;
    format?: 'markdown' | 'html';
}

function TextEditor({ data, format = 'markdown', onChange }: TextEditorProps) {
    const plugins: any[] = [ Essentials, Paragraph, Bold, Italic ];
    const toolbar: string[] = [ 'undo', 'redo', '|', 'bold', 'italic', '|', 'formatPainter' ];
    if (format === 'markdown') {
        plugins.push(Markdown);
    }
    return (
        <CKEditor
            editor={ ClassicEditor }
            config={ {
                licenseKey: 'GPL',
                plugins,
                toolbar,
                initialData: data,
            } }
            onChange={ (event, editor) => {
                const data = editor.getData();
                onChange(data);
                event;
            } }
        />
    );
}

export default TextEditor;
