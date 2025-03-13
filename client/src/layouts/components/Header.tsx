interface props {
    title: string;
    description?: string;
    image?: string;
}

export function Header({ title = 'Title', description, image}: props) {
    return (
        <header className="bg-white shadow">
            <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
                {image && <img src={image} alt={title} style={{ width: '200px', height: 'auto', marginLeft: 'auto', marginRight: 'auto' }} className='mb-10' />}
                <h1 className="text-3xl font-bold tracking-tight text-gray-900">
                    {title}
                </h1>
                {description && (
                    <p className="text-sm text-gray-500">{description}</p>
                )}
            </div>
        </header>
    );
}
