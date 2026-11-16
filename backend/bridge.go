package backend

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
)

func (a *App) runPythonGame(gameFolder string) {
	scriptPath := filepath.Join("games_logic", gameFolder, "engine.py")

	// On affiche le chemin exact que Go essaie d'utiliser
	fmt.Printf("🔍 Tentative d'ouverture du fichier : %s\n", scriptPath)

	cmd := exec.Command("python", scriptPath)

	// 🔴 LA MODIFICATION MAGIQUE : On dit à Go d'afficher les erreurs de Python dans notre terminal
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	err := cmd.Start()
	if err != nil {
		fmt.Printf("❌ Erreur critique de Go : %v\n", err)
		return
	}

	fmt.Printf("✅ Commande envoyée avec succès pour %s !\n", gameFolder)
}

// ... garde tes fonctions LaunchMahjong, LaunchMotsFleches et LaunchSolitaire en dessous
func (a *App) LaunchMahjong() {
	a.runPythonGame("mahjong")
}

func (a *App) LaunchMotsFleches() {
	a.runPythonGame("mots_fleches")
}

func (a *App) LaunchSolitaire() {
	a.runPythonGame("solitaire")
}
