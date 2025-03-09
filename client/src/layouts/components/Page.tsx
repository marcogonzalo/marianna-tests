import { ReactNode } from 'react';
import { Main } from './Main';
import { Header } from './Header';
import { Helmet } from 'react-helmet';

interface props {
    children: ReactNode;
    title?: string;
    description?: string;
}

export function Page({ title, description, children }: props) {
    return (
        <>
            <Helmet>
                <title>{title}</title>
            </Helmet>
            {title && <Header title={title} description={description} />}
            <Main>{children}</Main>
        </>
    );
}
