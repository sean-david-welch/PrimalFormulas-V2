package services

import (
	"errors"
	"github.com/sean-david-welch/primal-formulas/database"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/types"
)

type ProductService interface {
	GetProducts() ([]*types.Product, error)
	GetProductByID(id string) (*types.Product, error)
	CreateProduct(product *types.Product) (*types.ModelResult, error)
	UpdateProduct(id string, product *types.Product) (*types.ModelResult, error)
	DeleteProduct(id string) error
}

type ProductServiceImpl struct {
	store  database.ProductStore
	client lib.S3Client
}

func NewProductService(store database.ProductStore, client lib.S3Client) *ProductServiceImpl {
	return &ProductServiceImpl{store: store, client: client}
}

func (service *ProductServiceImpl) GetProducts() ([]*types.Product, error) {
	products, err := service.store.GetProducts()
	if err != nil {
		return nil, err
	}

	if len(products) == 0 {
		return nil, nil
	}

	return products, nil
}

func (service *ProductServiceImpl) GetProductByID(id string) (*types.Product, error) {
	product, err := service.store.GetProductByID(id)
	if err != nil {
		return nil, err
	}

	if product == nil {
		return nil, nil
	}

	return product, nil
}

func (service *ProductServiceImpl) CreateProduct(product *types.Product) (*types.ModelResult, error) {
	image := product.Image

	if image == "" || image == "null" {
		return nil, errors.New("image is empty")
	}

	presignedUrl, imageUrl, err := service.client.GeneratePresignedUrl(image)
	if err != nil {
		return nil, err
	}
	product.Image = imageUrl

	if _, err := service.store.CreateProduct(product); err != nil {
		return nil, err
	}

	result := &types.ModelResult{PresignedUrl: presignedUrl, ImageUrl: imageUrl}

	return result, nil
}

func (service *ProductServiceImpl) UpdateProduct(id string, product *types.Product) (*types.ModelResult, error) {
	image := product.Image

	var presignedUrl, imageUrl string
	var err error

	if image != "" && image != "null" {
		presignedUrl, imageUrl, err = service.client.GeneratePresignedUrl(image)
		if err != nil {
			return nil, err
		}
		product.Image = imageUrl
	}

	if _, err := service.store.UpdateProduct(id, product); err != nil {
		return nil, err
	}

	result := &types.ModelResult{PresignedUrl: presignedUrl, ImageUrl: imageUrl}

	return result, nil
}

func (service *ProductServiceImpl) DeleteProduct(id string) error {
	product, err := service.store.DeleteProduct(id)
	if err != nil {
		return err
	}

	if err := service.client.DeleteImageFromS3(product.Image); err != nil {
		return err
	}

	return nil
}
