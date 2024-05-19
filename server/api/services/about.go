package services

import (
	"errors"
	"github.com/sean-david-welch/primal-formulas/database"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/models"
)

type AboutService interface {
	GetAbouts() ([]*models.About, error)
	GetAboutByID(id string) (*models.About, error)
	CreateAbout(about *models.About) (*models.ModelResult, error)
	UpdateAbout(id string, about *models.About) (*models.ModelResult, error)
	DeleteAbout(id string) error
}

type AboutServiceImpl struct {
	store  database.AboutStore
	client lib.S3Client
}

func NewAboutService(store database.AboutStore, client lib.S3Client) *AboutServiceImpl {
	return &AboutServiceImpl{store: store, client: client}
}

func (service *AboutServiceImpl) GetAbouts() ([]*models.About, error) {
	abouts, err := service.store.GetAbouts()
	if err != nil {
		return nil, err
	}

	if len(abouts) == 0 {
		return nil, nil
	}

	return abouts, nil
}

func (service *AboutServiceImpl) GetAboutByID(id string) (*models.About, error) {
	about, err := service.store.GetAboutByID(id)
	if err != nil {
		return nil, err
	}

	if about == nil {
		return nil, nil
	}

	return about, nil
}

func (service *AboutServiceImpl) CreateAbout(about *models.About) (*models.ModelResult, error) {
	image := about.Image

	if image == "" || image == "null" {
		return nil, errors.New("image is empty")
	}

	presignedUrl, imageUrl, err := service.client.GeneratePresignedUrl(image)
	if err != nil {
		return nil, err
	}
	about.Image = imageUrl

	if _, err = service.store.CreateAbout(about); err != nil {
		return nil, err
	}

	result := &models.ModelResult{PresignedUrl: presignedUrl, ImageUrl: imageUrl}

	return result, nil
}

func (service *AboutServiceImpl) UpdateAbout(id string, about *models.About) (*models.ModelResult, error) {
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

	if _, err := service.store.UpdateAbout(id, about); err != nil {
		return nil, err
	}

	result := &models.ModelResult{PresignedUrl: presignedUrl, ImageUrl: imageUrl}

	return result, nil
}

func (service *AboutServiceImpl) DeleteAbout(id string) error {
	about, err := service.store.DeleteAbout(id)
	if err != nil {
		return err
	}

	if err := service.client.DeleteImageFromS3(about.Image); err != nil {
		return err
	}

	return nil
}
