import React, { useState } from 'react';
import { XMarkIcon, ClipboardDocumentIcon, CheckIcon } from '@heroicons/react/20/solid';
import { FormButton } from '@/components/ui';

interface CopyValueModalProps {
    isOpen: boolean;
    onClose: () => void;
    value: string;
    title?: string;
    label?: string;
    placeholder?: string;
    successMessage?: string;
}

const CopyValueModal: React.FC<CopyValueModalProps> = ({
    isOpen,
    onClose,
    value,
    title = 'Copy Value',
    label = 'Copy this value to clipboard:',
    placeholder = 'Value to copy',
    successMessage = 'Value copied to clipboard!',
}) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(value);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full shadow-xl">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        {title}
                    </h3>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                    >
                        <XMarkIcon className="h-6 w-6" />
                    </button>
                </div>
                
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {label}
                    </label>
                    <div className="flex">
                        <input
                            type="text"
                            value={value}
                            readOnly
                            placeholder={placeholder}
                            className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-l-md bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400"
                        />
                        <FormButton
                            onClick={handleCopy}
                            variant="link"
                            className="rounded-l-none border-l-0 hover:bg-blue-50 dark:hover:bg-blue-900/20"
                        >
                            {copied ? (
                                <CheckIcon className="h-4 w-4 text-green-500" />
                            ) : (
                                <ClipboardDocumentIcon className="h-4 w-4" />
                            )}
                        </FormButton>
                    </div>
                    {copied && (
                        <p className="mt-2 text-sm text-green-600 dark:text-green-400 flex items-center gap-1">
                            <CheckIcon className="h-4 w-4" />
                            {successMessage}
                        </p>
                    )}
                </div>
                
                <div className="flex justify-end">
                    <FormButton
                        onClick={onClose}
                        variant="secondary"
                    >
                        Close
                    </FormButton>
                </div>
            </div>
        </div>
    );
};

export default CopyValueModal;
