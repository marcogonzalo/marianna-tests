import { ReactNode } from 'react';
import { Main } from './Main';
import { Header } from './Header';
import { Helmet } from 'react-helmet';

interface props {
    children: ReactNode;
    title?: string;
}

export function Page({ title, children }: props) {
    return (
        <>
            <Helmet>
                <title>{title}</title>
            </Helmet>
            {title && <Header title={title} />}
            <Main>{children}</Main>
        </>
    );
}
