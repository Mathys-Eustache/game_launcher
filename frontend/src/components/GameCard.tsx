interface GameCardProps {
    title: string;
    emoji: string;
    colorClass: string;
    onClick: () => void; // 👈 Doit être présent ici
}

export default function GameCard({ title, emoji, colorClass, onClick }: GameCardProps) {
    return (
        // 🔴 CRUCIAL : Le onClick={onClick} doit être sur cette ligne :
        <button className={`gros-bouton ${colorClass}`} onClick={onClick}>
            <span>{emoji}</span> {title}
        </button>
    );
}