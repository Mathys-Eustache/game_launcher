// Importation des bibliothèques principales de React
import React from 'react'
import ReactDOM from 'react-dom/client'

// Importation de notre menu principal et de nos styles
import App from './App'
import './index.css'

// On cherche la div "root" dans le fichier index.html
const rootElement = document.getElementById('root');

// On demande à React de prendre le contrôle de cette div et d'y afficher notre <App />
if (rootElement) {
    ReactDOM.createRoot(rootElement).render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
    )
}