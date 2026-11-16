package backend

import (
	"context"

	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App est la structure de notre pont Go <-> React
type App struct {
	ctx context.Context
}

// NewApp crée une nouvelle application
func NewApp() *App {
	return &App{}
}

// Startup sauvegarde le contexte au démarrage
func (a *App) Startup(ctx context.Context) {
	a.ctx = ctx
}

// QuitApplication est la fonction appelée par le bouton rouge pour fermer l'app
func (a *App) QuitApplication() {
	runtime.Quit(a.ctx)
}
