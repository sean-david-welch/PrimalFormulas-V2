package services

import (
	"errors"
	"github.com/sean-david-welch/primal-formulas/database"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/types"
)

type AssetService interface {
	GetAssets() ([]*types.Asset, error)
	GetAssetByID(id string) (*types.Asset, error)
	CreateAsset(asset *types.Asset) (*types.ModelResult, error)
	UpdateAsset(id string, asset *types.Asset) (*types.ModelResult, error)
	DeleteAsset(id string) error
}

type AssetServiceImpl struct {
	store  database.AssetStore
	client lib.S3Client
}

func NewAssetStore(store database.AssetStore, client lib.S3Client) *AssetServiceImpl {
	return &AssetServiceImpl{
		store:  store,
		client: client,
	}
}

func (service *AssetServiceImpl) GetAssets() ([]*types.Asset, error) {
	assets, err := service.store.GetAssets()
	if err != nil {
		return nil, err
	}

	if len(assets) == 0 {
		return nil, nil
	}

	return assets, nil
}

func (service *AssetServiceImpl) GetAssetByID(id string) (*types.Asset, error) {
	asset, err := service.store.GetAssetByID(id)
	if err != nil {
		return nil, err
	}

	if asset == nil {
		return nil, nil
	}

	return asset, nil
}

func (service *AssetServiceImpl) CreateAsset(asset *types.Asset) (*types.ModelResult, error) {
	content := asset.Content

	if content == "" || content == "null" {
		return nil, errors.New("image is empty")
	}

	presignedUrl, imageUrl,

}

func (service *AssetServiceImpl) UpdateAsset(id string, asset *types.Asset) (*types.ModelResult, error) {

}

func (service *AssetServiceImpl) DeleteAsset(id string) error {

}
