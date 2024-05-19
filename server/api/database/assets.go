package database

import (
	"context"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb/types"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/models"
)

const (
	AssetsTable = "assets"
)

type AssetStore interface {
	GetAssets() ([]*models.Asset, error)
	GetAssetByID(id string) (*models.Asset, error)
	CreateAsset(asset *models.Asset) (*models.Asset, error)
	UpdateAsset(id string, asset *models.Asset) (*models.Asset, error)
	DeleteAsset(id string) (*models.Asset, error)
}

type AssetStoreImpl struct {
	db *lib.DynamoDBClient
}

func NewAssetStore(db *lib.DynamoDBClient) *AssetStoreImpl {
	return &AssetStoreImpl{db: db}
}

func (store *AssetStoreImpl) GetAssets() ([]*models.Asset, error) {
	input := &dynamodb.ScanInput{TableName: aws.String(AssetsTable)}

	result, err := store.db.Database.Scan(context.TODO(), input)
	if err != nil {
		return nil, err
	}

	var assets []*models.Asset
	err = attributevalue.UnmarshalListOfMaps(result.Items, &assets)
	if err != nil {
		return nil, err
	}

	return assets, nil
}

func (store *AssetStoreImpl) GetAssetByID(id string) (*models.Asset, error) {
	input := &dynamodb.GetItemInput{
		TableName: aws.String(AssetsTable),
		Key: map[string]types.AttributeValue{
			"id": &types.AttributeValueMemberS{Value: id},
		},
	}

	result, err := store.db.Database.GetItem(context.TODO(), input)
	if err != nil {
		return nil, err
	}

	var asset models.Asset
	err = attributevalue.UnmarshalMap(result.Item, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

func (store *AssetStoreImpl) CreateAsset(asset *models.Asset) (*models.Asset, error) {
	item, err := attributevalue.MarshalMap(asset)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.PutItemInput{
		TableName: aws.String(AssetsTable),
		Item:      item,
	}

	if _, err = store.db.Database.PutItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return asset, nil
}

func (store *AssetStoreImpl) UpdateAsset(id string, asset *models.Asset) (*models.Asset, error) {
	updateExpression := "SET Name = :name, Content = :content"
	input := &dynamodb.UpdateItemInput{
		TableName: aws.String(AssetsTable),
		Key: map[string]types.AttributeValue{
			"id": &types.AttributeValueMemberS{Value: id},
		},
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":name":    &types.AttributeValueMemberS{Value: asset.Name},
			":content": &types.AttributeValueMemberS{Value: asset.Content},
		},
		UpdateExpression: aws.String(updateExpression),
		ReturnValues:     types.ReturnValueUpdatedNew,
	}

	if _, err := store.db.Database.UpdateItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return asset, nil
}

func (store *AssetStoreImpl) DeleteAsset(id string) (*models.Asset, error) {
	asset, err := store.GetAssetByID(id)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.DeleteItemInput{
		TableName: aws.String(AssetsTable),
		Key: map[string]types.AttributeValue{
			"id": &types.AttributeValueMemberS{Value: id},
		},
	}

	if _, err := store.db.Database.DeleteItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return asset, nil
}
