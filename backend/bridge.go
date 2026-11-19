package backend

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
)

func (a *App) runPythonGame(gameFolder string) {
	scriptPath := filepath.Join("games_logic", gameFolder, "engine.py")

	fmt.Printf("🔍 Tentative d'ouverture du fichier : %s\n", scriptPath)

	pythonCmd := "python3"
	if runtime.GOOS == "windows" {
		pythonCmd = "python"
	}

	cmd := exec.Command(pythonCmd, scriptPath)

	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	err := cmd.Start()
	if err != nil {
		fmt.Printf("❌ Erreur critique de Go : %v\n", err)
		return
	}

	fmt.Printf("✅ Commande envoyée avec succès pour %s !\n", gameFolder)
}

func (a *App) LaunchMahjong() {
	a.runPythonGame("mahjong")
}

func (a *App) LaunchMotsFleches() {
	a.runPythonGame("mots_fleches")
}

func (a *App) LaunchSolitaire() {
	a.runPythonGame("solitaire")
}
