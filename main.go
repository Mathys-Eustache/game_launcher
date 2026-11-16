// Déclaration du package principal obligatoire pour lancer un programme Go
package main

import (
	"embed"
	"log"

	// On importe notre dossier backend qui contient la logique de l'application
	"senior_games_launcher/backend"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {
	// On crée une nouvelle instance de notre application (définie dans app.go)
	app := backend.NewApp()

	// Configuration de la fenêtre de l'application
	err := wails.Run(&options.App{
		Title:  "Mes Jeux", // Le titre affiché en haut de la fenêtre
		Width:  1024,       // Largeur de la fenêtre
		Height: 768,        // Hauteur de la fenêtre
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		OnStartup: app.Startup,
		// C'est ici que l'on relie (Bind) notre code Go à l'interface React
		Bind: []interface{}{
			app,
		},
	})

	if err != nil {
		log.Fatal(err)
	}
}
