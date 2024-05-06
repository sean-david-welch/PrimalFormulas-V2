package services

import (
	"github.com/sean-david-welch/primal-formulas/database"
	"github.com/sean-david-welch/primal-formulas/types"
)

type AboutService interface {
	GetAbouts() ([]*types.About, error)
	GetAboutByID(string) (*types.About, error)
	CreateAbout(*types.About) (*types.About, error)
	UpdateAbout(*types.About) (*types.About, error)
	DeleteAbout(*types.About) error
}

type AboutServiceImpl struct {
	store database.AboutStore
	client
}
