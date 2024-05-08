package services

import (
	"errors"
	"github.com/sean-david-welch/primal-formulas/database"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/types"
)

type AboutService interface {
	GetAbouts() ([]*types.About, error)
	GetAboutByID(id string) (*types.About, error)
	CreateAbout(about *types.About) (*types.About, error)
	UpdateAbout(id string, about *types.About) (*types.About, error)
	DeleteAbout(id string) error
}

type AboutServiceImpl struct {
	store  database.AboutStore
	client lib.S3Client
}

func NewAboutService(store database.AboutStore, client lib.S3Client) *AboutServiceImpl {
	return &AboutServiceImpl{store: store, client: client}
}

func (service *AboutServiceImpl) GetAbouts() ([]*types.About, error) {
	abouts, err := service.store.GetAbouts()
	if err != nil {
		return nil, err
	}

	if len(abouts) == 0 {
		return nil, nil
	}

	return abouts, nil
}

func (service *AboutServiceImpl) GetAboutById(id string) (*types.About, error) {
	about, err := service.store.GetAboutByID(id)
	if err != nil {
		return nil, err
	}

	if about == nil {
		return nil, nil
	}

	return about, nil
}

func (service *AboutServiceImpl) CreateAbout(about *types.About) (*types.About, error) {
	image := about.Image

	if image == "" || image == "null" {
		return nil, errors.New("image is empty")
	}

	presignedUrl, ImageUrl, err := service.client.GeneratePresignedUrl(image)

	about.Image = ImageUrl

	if err := service.store.CreateAbout(about); err != nil {
		return nil, err
	}
}
