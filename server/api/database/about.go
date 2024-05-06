package database

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
	"github.com/sean-david-welch/primal-formulas/types"
)

const (
	TABLE_NAME = "about"
)

type AboutStore interface {
	GetAbouts() ([]*types.About, error)
	GetAboutByID(string) (*types.About, error)
	CreateAbout(*types.About) (*types.About, error)
	UpdateAbout(*types.About) (*types.About, error)
	DeleteAbout(*types.About) error
}

type AboutStoreImpl struct {
	database *types.DynamoDBClient
}

func NewAboutStore(database *types.DynamoDBClient) *AboutStoreImpl {
	return &AboutStoreImpl{database: database}
}

func (store *AboutStoreImpl) GetAbouts() ([]*types.About, error) {
	input := &dynamodb.ScanInput{TableName: aws.String(TABLE_NAME)}
	result, err := store.database.Database.Scan(input)
	if err != nil {
		return nil, err
	}

	var abouts []*types.About
	err = dynamodbattribute.UnmarshalListOfMaps(result.Items, &abouts)
	if err != nil {
		return nil, err
	}

	return abouts, nil
}
