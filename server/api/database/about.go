package database

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/models"
)

const (
	AboutTable = "about"
)

type AboutStore interface {
	GetAbouts() ([]*models.About, error)
	GetAboutByID(string) (*models.About, error)
	CreateAbout(about *models.About) (*models.About, error)
	UpdateAbout(id string, about *models.About) (*models.About, error)
	DeleteAbout(id string) (*models.About, error)
}

type AboutStoreImpl struct {
	db *lib.DynamoDBClient
}

func NewAboutStore(db *lib.DynamoDBClient) *AboutStoreImpl {
	return &AboutStoreImpl{db: db}
}

func (store *AboutStoreImpl) GetAbouts() ([]*models.About, error) {
	input := &dynamodb.ScanInput{TableName: aws.String(AboutTable)}
	result, err := store.db.Database.Scan(input)
	if err != nil {
		return nil, err
	}

	var abouts []*models.About
	err = dynamodbattribute.UnmarshalListOfMaps(result.Items, &abouts)
	if err != nil {
		return nil, err
	}

	return abouts, nil
}

func (store *AboutStoreImpl) GetAboutByID(id string) (*models.About, error) {
	input := &dynamodb.GetItemInput{TableName: aws.String(AboutTable), Key: map[string]*dynamodb.AttributeValue{
		"id": {
			S: aws.String(id),
		},
	}}

	result, err := store.db.Database.GetItem(input)
	if err != nil {
		return nil, err
	}

	if result.Item == nil {
		return nil, nil
	}

	var about *models.About
	err = dynamodbattribute.UnmarshalMap(result.Item, &about)
	if err != nil {
		return nil, err
	}

	return about, nil
}

func (store *AboutStoreImpl) CreateAbout(about *models.About) (*models.About, error) {
	item, err := dynamodbattribute.MarshalMap(about)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.PutItemInput{
		TableName: aws.String(AboutTable),
		Item:      item,
	}

	_, err = store.db.Database.PutItem(input)
	if err != nil {
		return nil, err
	}

	return about, nil
}

func (store *AboutStoreImpl) UpdateAbout(id string, about *models.About) (*models.About, error) {
	updateExpression := "SET Title = :title, Description = : desc, Image = : img"
	input := &dynamodb.UpdateItemInput{
		TableName: aws.String(AboutTable),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {
				S: aws.String(id),
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

	_, err := store.db.Database.UpdateItem(input)
	if err != nil {
		return nil, err
	}

	return about, nil
}

func (store *AboutStoreImpl) DeleteAbout(id string) (*models.About, error) {
	about, err := store.GetAboutByID(id)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.DeleteItemInput{
		TableName: aws.String(AboutTable),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {
				S: aws.String(id),
			},
		},
	}

	if _, err = store.db.Database.DeleteItem(input); err != nil {
		return nil, err
	}

	return about, nil
}
