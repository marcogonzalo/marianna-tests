import { useLocation } from 'react-router-dom';
import classNames from 'classnames';
import {
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
} from '@headlessui/react';
import { BellIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { Dropdown } from '@/components/ui/Dropdown';

const user = {
    name: 'Tom Cook',
    email: 'tom@example.com',
    imageUrl:
        'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
};
const navigation = [
    { name: 'Assessments', href: '/assessments' },
    { name: 'Examinees', href: '/examinees' },
    { name: 'Users', href: '/users' },
    { name: 'Calendar', href: '#' },
    { name: 'Reports', href: '#' },
];
const userNavigation = [
    { label: 'Your Profile', value: '#' },
    { label: 'Settings', value: '#' },
    { label: 'Sign out', value: '/logout' },
];

export function NavBar() {
    const location = useLocation();
    const currentPath = location.pathname.split('/')[1];

    const isCurrent = (href: string) => href.split('/')[1] === currentPath;

    return (
        <Disclosure as="nav" className="bg-gray-800">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    <div className="flex items-center">
                        <div className="shrink-0">
                            <img
                                alt="Your Company"
                                src="https://tailwindui.com/plus/img/logos/mark.svg?color=indigo&shade=500"
                                className="size-8"
                            />
                        </div>
                        <div className="hidden md:block">
                            <div className="ml-10 flex items-baseline space-x-4">
                                {navigation.map((item) => (
                                    <a
                                        key={item.name}
                                        href={item.href}
                                        aria-current={
                                            isCurrent(item.href)
                                                ? 'page'
                                                : undefined
                                        }
                                        className={classNames(
                                            isCurrent(item.href)
                                                ? 'bg-gray-900 text-white'
                                                : 'text-gray-300 hover:bg-gray-700 hover:text-white',
                                            'rounded-md px-3 py-2 text-sm font-medium',
                                        )}
                                    >
                                        {item.name}
                                    </a>
                                ))}
                            </div>
                        </div>
                    </div>
                    <div className="hidden md:block">
                        <div className="ml-4 flex items-center md:ml-6">
                            <button
                                type="button"
                                className="relative rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                            >
                                <span className="absolute -inset-1.5" />
                                <span className="sr-only">
                                    View notifications
                                </span>
                                <BellIcon
                                    aria-hidden="true"
                                    className="size-6"
                                />
                            </button>

                            {/* Profile dropdown */}
                            <Dropdown
                                title={user.name}
                                className="relative ml-3"
                                items={userNavigation}
                                type="image"
                                imageURL={user.imageUrl}
                            ></Dropdown>
                        </div>
                    </div>
                    <div className="-mr-2 flex md:hidden">
                        {/* Mobile menu button */}
                        <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md bg-gray-800 p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                            <span className="absolute -inset-0.5" />
                            <span className="sr-only">Open main menu</span>
                            <Bars3Icon
                                aria-hidden="true"
                                className="block size-6 group-data-[open]:hidden"
                            />
                            <XMarkIcon
                                aria-hidden="true"
                                className="hidden size-6 group-data-[open]:block"
                            />
                        </DisclosureButton>
                    </div>
                </div>
            </div>

            <DisclosurePanel className="md:hidden">
                <div className="space-y-1 px-2 pb-3 pt-2 sm:px-3">
                    {navigation.map((item) => (
                        <DisclosureButton
                            key={item.name}
                            as="a"
                            href={item.href}
                            aria-current={
                                isCurrent(item.href) ? 'page' : undefined
                            }
                            className={classNames(
                                isCurrent(item.href)
                                    ? 'bg-gray-900 text-white'
                                    : 'text-gray-300 hover:bg-gray-700 hover:text-white',
                                'block rounded-md px-3 py-2 text-base font-medium',
                            )}
                        >
                            {item.name}
                        </DisclosureButton>
                    ))}
                </div>
                <div className="border-t border-gray-700 pb-3 pt-4">
                    <div className="flex items-center px-5">
                        <div className="shrink-0">
                            <img
                                alt=""
                                src={user.imageUrl}
                                className="size-10 rounded-full"
                            />
                        </div>
                        <div className="ml-3">
                            <div className="text-base/5 font-medium text-white">
                                {user.name}
                            </div>
                            <div className="text-sm font-medium text-gray-400">
                                {user.email}
                            </div>
                        </div>
                        <button
                            type="button"
                            className="relative ml-auto shrink-0 rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                        >
                            <span className="absolute -inset-1.5" />
                            <span className="sr-only">View notifications</span>
                            <BellIcon aria-hidden="true" className="size-6" />
                        </button>
                    </div>
                    <div className="mt-3 space-y-1 px-2">
                        {userNavigation.map((item) => (
                            <DisclosureButton
                                key={item.label}
                                as="a"
                                href={item.value}
                                className="block rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white"
                            >
                                {item.label}
                            </DisclosureButton>
                        ))}
                        {userNavigation.length > 0 && (
                            <DisclosureButton
                                key={'Sign out'}
                                as="a"
                                href="#"
                                onClick={() => {}}
                                className="block rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white"
                            >
                                Sign out
                            </DisclosureButton>
                        )}
                    </div>
                </div>
            </DisclosurePanel>
        </Disclosure>
    );
}
