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

func (store *AboutStoreImpl) GetAboutByID(id string) (*types.About, error) {
	input := &dynamodb.GetItemInput{TableName: aws.String(TABLE_NAME), Key: map[string]*dynamodb.AttributeValue{
		"id": {
			S: aws.String(id),
		},
	}}

	result, err := store.database.Database.GetItem(input)
	if err != nil {
		return nil, err
	}

	if result.Item == nil {
		return nil, nil
	}

	var about *types.About
	err = dynamodbattribute.UnmarshalMap(result.Item, &about)
	if err != nil {
		return nil, err
	}

	return about, nil
}

func (store *AboutStoreImpl) CreateAbout(about *types.About) (*types.About, error) {
	item, err := dynamodbattribute.MarshalMap(about)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.PutItemInput{
		TableName: aws.String(TABLE_NAME),
		Item:      item,
	}

	_, err = store.database.Database.PutItem(input)
	if err != nil {
		return nil, err
	}

	return about, nil
}

func (store *AboutStoreImpl) UpdateAbout(about *types.About) (*types.About, error) {
	updateExpression := "SET Title = :title, Description = : desc, Image = : img"
	input := &dynamodb.UpdateItemInput{
		TableName: aws.String(TABLE_NAME),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {
				S: aws.String(about.ID),
			},
		},
		ExpressionAttributeValues: map[string]*dynamodb.AttributeValue{
			":title":       {S: aws.String(about.Title)},
			":description": {S: aws.String(about.Description)},
			":img":         {S: aws.String(about.Image)},
		},
		UpdateExpression: aws.String(updateExpression),
		ReturnValues:     aws.String("UPDATED_NEW"),
	}

	_, err := store.database.Database.UpdateItem(input)
	if err != nil {
		return nil, err
	}

	return about, nil
}

func (store *AboutStoreImpl) DeleteAbout(about *types.About) error {
	input := &dynamodb.DeleteItemInput{
		TableName: aws.String(TABLE_NAME),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {
				S: aws.String(about.ID),
			},
		},
	}

	_, err := store.database.Database.DeleteItem(input)
	if err != nil {
		return err
	}

	return nil
}
