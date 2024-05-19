package database

import (
	"context"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/types"
)

const (
	AssetsTable = "assets"
)

type AssetStore interface {
	GetAssets() ([]*types.Asset, error)
	GetAssetByID(id string) (*types.Asset, error)
	CreateAsset(asset *types.Asset) (*types.Asset, error)
	UpdateAsset(id string, asset *types.Asset) (*types.Asset, error)
	DeleteAsset(id string) (*types.Asset, error)
}

type AssetStoreImpl struct {
	db *lib.DynamoDBClient
}

func NewAssetStore(db *lib.DynamoDBClient) *AssetStoreImpl {
	return &AssetStoreImpl{db: db}
}

func (store *AssetStoreImpl) GetAssets() ([]*types.Asset, error) {
	input := &dynamodb.ScanInput{TableName: aws.String(AssetsTable)}

	result, err := store.db.Database.Scan(context.TODO(), input)
	if err != nil {
		return nil, err
	}

	var assets []*types.Asset
	err = attributevalue.UnmarshalListOfMaps(result.Items, &assets)
	if err != nil {
		return nil, err
	}

	return assets, nil
}

func (store *AssetStoreImpl) GetAssetByID(id string) (*types.Asset, error) {
	input := &dynamodb.GetItemInput{
		TableName: aws.String(AssetsTable),
		Key: map[string]dynamodb.At{
			"id": &dynamodb.AttributeValueMemberS{Value: id},
		},
	}

	result, err := store.db.Database.GetItem(context.TODO(), input)
	if err != nil {
		return nil, err
	}

	var asset types.Asset
	err = attributevalue.UnmarshalMap(result.Item, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

func (store *AssetStoreImpl) CreateAsset(asset *types.Asset) (*types.Asset, error) {
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

func (store *AssetStoreImpl) UpdateAsset(id string, asset *types.Asset) (*types.Asset, error) {
	updateExpression := "SET Name = :name, Content = :content"
	input := &dynamodb.UpdateItemInput{
		TableName: aws.String(AssetsTable),
		Key: map[string]dynamodb.AttributeValue{
			"id": {
				S: aws.String(id),
			},
		},
		ExpressionAttributeValues: map[string]dynamodb.AttributeValue{
			":name":    {S: aws.String(asset.Name)},
			":content": {S: aws.String(asset.Content)},
		},
		UpdateExpression: aws.String(updateExpression),
		ReturnValues:     dynamodb.ReturnValueUpdatedNew,
	}

	if _, err := store.db.Database.UpdateItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return asset, nil
}

func (store *AssetStoreImpl) DeleteAsset(id string) (*types.Asset, error) {
	asset, err := store.GetAssetByID(id)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.DeleteItemInput{
		TableName: aws.String(AssetsTable),
		Key: map[string]dynamodb.AttributeValue{
			"id": {
				S: aws.String(id),
			},
		},
	}

	if _, err := store.db.Database.DeleteItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return asset, nil
}
