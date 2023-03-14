import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';
import { AuthProvider } from './context/AuthContext';

const rootElement = document.getElementById('root');
const root = createRoot(rootElement);

root.render(
    <AuthProvider>
        <App />
    </AuthProvider>
);
