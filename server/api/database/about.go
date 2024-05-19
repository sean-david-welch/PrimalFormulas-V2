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
	result, err := store.db.Database.Scan(context.TODO(), input)
	if err != nil {
		return nil, err
	}

	var abouts []*models.About
	err = attributevalue.UnmarshalListOfMaps(result.Items, &abouts)
	if err != nil {
		return nil, err
	}

	return abouts, nil
}

func (store *AboutStoreImpl) GetAboutByID(id string) (*models.About, error) {
	input := &dynamodb.GetItemInput{
		TableName: aws.String(AboutTable),
		Key: map[string]types.AttributeValue{
			"id": &types.AttributeValueMemberS{Value: id},
		},
	}

	result, err := store.db.Database.GetItem(context.TODO(), input)
	if err != nil {
		return nil, err
	}

	if result.Item == nil {
		return nil, nil
	}

	var about *models.About
	err = attributevalue.UnmarshalMap(result.Item, &about)
	if err != nil {
		return nil, err
	}

	return about, nil
}

func (store *AboutStoreImpl) CreateAbout(about *models.About) (*models.About, error) {
	item, err := attributevalue.MarshalMap(about)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.PutItemInput{
		TableName: aws.String(AboutTable),
		Item:      item,
	}

	if _, err = store.db.Database.PutItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return about, nil
}

func (store *AboutStoreImpl) UpdateAbout(id string, about *models.About) (*models.About, error) {
	updateExpression := "SET Title = :title, Description = : desc, Image = : img"
	input := &dynamodb.UpdateItemInput{
		TableName: aws.String(AboutTable),
		Key: map[string]types.AttributeValue{
			"id": &types.AttributeValueMemberS{Value: id},
		},
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":title":       &types.AttributeValueMemberS{Value: about.Title},
			":description": &types.AttributeValueMemberS{Value: about.Description},
			":img":         &types.AttributeValueMemberS{Value: about.Image},
		},
		UpdateExpression: aws.String(updateExpression),
		ReturnValues:     types.ReturnValueUpdatedNew,
	}

	if _, err := store.db.Database.UpdateItem(context.TODO(), input); err != nil {
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
		Key: map[string]types.AttributeValue{
			"id": &types.AttributeValueMemberS{Value: id},
		},
	}

	if _, err = store.db.Database.DeleteItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return about, nil
}
