package database

import (
	"context"
	"fmt"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb/types"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/models"
)

const (
	ProductsTable = "products"
)

type ProductStore interface {
	GetProducts() ([]*models.Product, error)
	GetProductByID(id string) (*models.Product, error)
	CreateProduct(product *models.Product) (*models.Product, error)
	UpdateProduct(id string, product *models.Product) (*models.Product, error)
	DeleteProduct(id string) (*models.Product, error)
}

type ProductStoreImpl struct {
	db *lib.DynamoDBClient
}

func NewProductStore(db *lib.DynamoDBClient) *ProductStoreImpl {
	return &ProductStoreImpl{
		db: db,
	}
}

func (store *ProductStoreImpl) GetProducts() ([]*models.Product, error) {
	input := &dynamodb.ScanInput{TableName: aws.String(ProductsTable)}
	result, err := store.db.Database.Scan(context.TODO(), input)
	if err != nil {
		return nil, err
	}

	var products []*models.Product
	err = attributevalue.UnmarshalListOfMaps(result.Items, &products)
	if err != nil {
		return nil, err
	}

	return products, nil
}

func (store *ProductStoreImpl) GetProductByID(id string) (*models.Product, error) {
	input := &dynamodb.GetItemInput{
		TableName: aws.String(ProductsTable),
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

	var product *models.Product
	err = attributevalue.UnmarshalMap(result.Item, &product)
	if err != nil {
		return nil, err
	}

	return product, nil
}

func (store *ProductStoreImpl) CreateProduct(product *models.Product) (*models.Product, error) {
	item, err := attributevalue.MarshalMap(product)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.PutItemInput{
		TableName: aws.String(ProductsTable),
		Item:      item,
	}

	if _, err = store.db.Database.PutItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return product, nil
}

func (store *ProductStoreImpl) UpdateProduct(id string, product *models.Product) (*models.Product, error) {
	updateExpression := "SET Name = : name, Description = : desc, Image = : img, Price = : price"
	input := &dynamodb.UpdateItemInput{
		TableName: aws.String(ProductsTable),
		Key: map[string]types.AttributeValue{
			"id": &types.AttributeValueMemberS{Value: id},
		},
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":name":        &types.AttributeValueMemberS{Value: product.Name},
			":description": &types.AttributeValueMemberS{Value: product.Description},
			":image":       &types.AttributeValueMemberS{Value: product.Image},
			":price":       &types.AttributeValueMemberN{Value: fmt.Sprintf("%f", product.Price)},
		},
		UpdateExpression: aws.String(updateExpression),
		ReturnValues:     types.ReturnValueUpdatedNew,
	}

	if _, err := store.db.Database.UpdateItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return product, nil
}

func (store *ProductStoreImpl) DeleteProduct(id string) (*models.Product, error) {
	product, err := store.GetProductByID(id)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.DeleteItemInput{
		TableName: aws.String(ProductsTable),
		Key: map[string]types.AttributeValue{
			"id": &types.AttributeValueMemberS{Value: id},
		},
	}

	if _, err := store.db.Database.DeleteItem(context.TODO(), input); err != nil {
		return nil, err
	}

	return product, nil
}
