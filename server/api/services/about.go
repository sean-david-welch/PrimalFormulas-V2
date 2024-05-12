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
	CreateAbout(about *types.About) (*types.ModelResult, error)
	UpdateAbout(id string, about *types.About) (*types.ModelResult, error)
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

func (service *AboutServiceImpl) CreateAbout(about *types.About) (*types.ModelResult, error) {
	image := about.Image

	if image == "" || image == "null" {
		return nil, errors.New("image is empty")
	}

	presignedUrl, imageUrl, err := service.client.GeneratePresignedUrl(image)
	if err != nil {
		return nil, err
	}
	about.Image = imageUrl

	if err = service.store.CreateAbout(about); err != nil {
		return nil, err
	}

	result := &types.ModelResult{PresignedUrl: presignedUrl, ImageUrl: imageUrl}

	return result, nil
}

func (service *AboutServiceImpl) UpdateAbout(id string, about *types.About) (*types.ModelResult, error) {
	image := about.Image

	var presignedUrl, imageUrl string
	var err error

	if image != "null" && image != "" {
		presignedUrl, imageUrl, err = service.client.GeneratePresignedUrl(image)
		if err != nil {
			return nil, err
		}
		about.Image = imageUrl
	}

	if err := service.store.UpdateAbout(id, about); err != nil {
		return nil, err
	}

	result := &types.ModelResult{PresignedUrl: presignedUrl, ImageUrl: imageUrl}

	return result, nil
}

func (service *AboutServiceImpl) DeleteAbout(id string) error {
	about, err := service.store.DeleteAbout(id)
	if err != nil {
		return nil
	}

	if err := service.client.DeleteImageFromS3(about.Image); err != nil {
		return err
	}

	return nil
}
