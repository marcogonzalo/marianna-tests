import { RouterProvider } from 'react-router-dom';
import router from './router';
import { NavBar } from './layouts/NavBar';

export default function App() {
    return (
        <div className="min-h-full">
            <NavBar />
            <RouterProvider router={router} />
        </div>
    );
}
