# CopyValueModal Component

A reusable modal component for displaying copyable values (tokens, codes, URLs, etc.) with a built-in copy-to-clipboard functionality.

## Features

- **Non-editable input field**: Shows the value in a read-only input for easy selection
- **Copy button**: One-click copy to clipboard with visual feedback
- **Customizable**: Configurable title, label, placeholder, and success message
- **Dark mode support**: Fully responsive with light/dark theme support
- **Accessible**: Proper ARIA labels and keyboard navigation

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `isOpen` | `boolean` | - | Controls modal visibility |
| `onClose` | `() => void` | - | Function called when modal is closed |
| `value` | `string` | - | The value to be displayed and copied |
| `title` | `string` | `'Copy Value'` | Modal title |
| `label` | `string` | `'Copy this value to clipboard:'` | Input field label |
| `placeholder` | `string` | `'Value to copy'` | Input placeholder text |
| `successMessage` | `string` | `'Value copied to clipboard!'` | Success message after copying |

## Usage Examples

### Basic Usage

```tsx
import CopyValueModal from '@/components/ui/modals/CopyValueModal';

const [isOpen, setIsOpen] = useState(false);
const [value, setValue] = useState('');

const handleCopy = (text: string) => {
    setValue(text);
    setIsOpen(true);
};

return (
    <>
        <button onClick={() => handleCopy('example-value')}>
            Copy Value
        </button>
        
        <CopyValueModal
            isOpen={isOpen}
            onClose={() => setIsOpen(false)}
            value={value}
        />
    </>
);
```

### Copy Assessment URL

```tsx
<CopyValueModal
    isOpen={copyModalOpen}
    onClose={handleCloseCopyModal}
    value={urlToCopy}
    title="Copy Assessment URL"
    label="Copy this assessment URL to clipboard:"
    successMessage="Assessment URL copied to clipboard!"
/>
```

### Copy API Token

```tsx
<CopyValueModal
    isOpen={tokenModalOpen}
    onClose={() => setTokenModalOpen(false)}
    value={apiToken}
    title="Copy API Token"
    label="Copy your API token to clipboard:"
    successMessage="API token copied to clipboard!"
/>
```

### Copy Invitation Code

```tsx
<CopyValueModal
    isOpen={inviteModalOpen}
    onClose={() => setInviteModalOpen(false)}
    value={inviteCode}
    title="Copy Invitation Code"
    label="Share this invitation code:"
    successMessage="Invitation code copied to clipboard!"
/>
```

## Implementation Notes

- The modal automatically handles clipboard operations using the `navigator.clipboard.writeText()` API
- Visual feedback is provided with a checkmark icon and success message for 2 seconds after copying
- The modal is responsive and works on both desktop and mobile devices
- Dark mode is automatically applied based on the user's theme preference
- The input field is read-only to prevent accidental modifications

## Accessibility

- Proper focus management when opening/closing the modal
- ARIA labels for screen readers
- Keyboard navigation support (Escape to close)
- High contrast colors for better visibility
- Semantic HTML structure
