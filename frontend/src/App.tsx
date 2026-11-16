import { useState } from 'react';
import './index.css';
import GameCard from './components/GameCard';

import { 
    QuitApplication, 
    LaunchMahjong, 
    LaunchMotsFleches, 
    LaunchSolitaire 
} from "../wailsjs/go/backend/App";

function App() {
    // On crée un état pour le thème (faux = clair, vrai = sombre)
    const [isDarkMode, setIsDarkMode] = useState(false);

    // Fonction pour inverser le thème
    const toggleTheme = () => {
        setIsDarkMode(!isDarkMode);
    };

    return (
        // La div principale change de classe selon le thème choisi
        <div className={`app-wrapper ${isDarkMode ? 'theme-sombre' : 'theme-clair'}`}>
            
            {/* Bouton pour changer de thème (Haut Droite) */}
            <button className="btn-theme" onClick={toggleTheme}>
                {isDarkMode ? '☀️ Passer en Thème Clair' : '🌙 Passer en Thème Sombre'}
            </button>

            <div className="menu-container">
                <h1 className="titre">La plateforme à jeux</h1>
                
                <GameCard title="Mahjong" emoji="🀄" colorClass="btn-mahjong" onClick={LaunchMahjong} />
                <GameCard title="Mots Fléchés" emoji="📝" colorClass="btn-mots" onClick={LaunchMotsFleches} />
                <GameCard title="Solitaire" emoji="🃏" colorClass="btn-solitaire" onClick={LaunchSolitaire} />
                
                <button className="gros-bouton btn-quitter" onClick={QuitApplication}>
                    ❌ Quitter
                </button>
            </div>
        </div>
    );
}

export default App;