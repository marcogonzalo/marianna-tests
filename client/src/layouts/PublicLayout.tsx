import { Outlet } from 'react-router-dom';
import { Main } from './components/Main';

export default function PublicLayout() {
    return (
        <Main>
            <Outlet />
        </Main>
    );
}
