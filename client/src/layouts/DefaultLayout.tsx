import { Outlet } from 'react-router-dom';
import { NavBar } from './components/NavBar';
import { Main } from './components/Main';

export default function DefaultLayout() {
    return (
        <>
            <NavBar />
            <Main>
                <Outlet />
            </Main>
        </>
    );
}
