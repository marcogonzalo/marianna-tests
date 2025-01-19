import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/react';
import { ChevronDownIcon } from '@heroicons/react/20/solid';
import classNames from 'classnames';

interface props {
    title: string;
    type?: 'text' | 'image';
    className?: string;
    imageURL?: string;
    items: DropdownItem[];
    divided?: boolean;
}

export interface DropdownItem {
    label: string;
    value: string;
    disabled?: boolean;
    icon?: React.ReactNode;
}

export function Dropdown({
    title,
    type = 'text',
    className,
    imageURL,
    items,
    divided = false,
}: props) {
    const menuItemsClasses = classNames({
        'absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black/5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in':
            true,
        'divide-y divide-gray-100': divided,
    });

    return (
        <Menu
            as="div"
            className={`relative inline-block text-left ${className}`}
        >
            {type === 'text' && (
                <div>
                    <MenuButton className="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                        {title}
                        <ChevronDownIcon
                            aria-hidden="true"
                            className="-mr-1 size-5 text-gray-400"
                        />
                    </MenuButton>
                </div>
            )}
            {type === 'image' && (
                <div>
                    <MenuButton className="relative flex max-w-xs items-center rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                        <span className="absolute -inset-1.5" />
                        <span className="sr-only">Open {title} menu</span>
                        <img
                            alt={`${title}'s menu avatar`}
                            src={imageURL}
                            className="size-8 rounded-full"
                        />
                    </MenuButton>
                </div>
            )}

            <MenuItems transition className={menuItemsClasses}>
                {items.map((item) => (
                    <div className="py-1" key={item.label}>
                        <MenuItem>
                            <a
                                href={item.value}
                                className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100 data-[focus]:outline-none"
                            >
                                {item.icon} {item.label}
                            </a>
                        </MenuItem>
                    </div>
                ))}
            </MenuItems>
        </Menu>
    );
}
