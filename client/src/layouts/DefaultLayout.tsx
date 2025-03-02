import { Main } from './components/Main';
import { Outlet } from 'react-router-dom';

export default function DefaultLayout() {
    return (
        <>
            <Main>
                <Outlet />
            </Main>
        </>
    );
}
