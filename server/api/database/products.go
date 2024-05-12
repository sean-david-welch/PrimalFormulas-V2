package database

import (
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/types"
)

const (
	ProductsTable = "products"
)

type ProductStore interface {
	GetProducts() ([]*types.Product, error)
	GetProductByID(string) (*types.Product, error)
	CreateProduct(product *types.Product) (*types.Product, error)
	UpdateProduct(product *types.Product) (*types.Product, error)
	DeleteProduct(product *types.Product) error
}

type ProductStoreImpl struct {
	database *lib.DynamoDBClient
}

func NewProductStore(database *lib.DynamoDBClient) *ProductStoreImpl {
	return &ProductStoreImpl{
		database: database,
	}
}

func (store *ProductStoreImpl) GetProducts() ([]*types.Product, error) {
	input := &dynamodb.ScanInput{TableName: aws.String(ProductsTable)}
	result, err := store.database.Database.Scan(input)
	if err != nil {
		return nil, err
	}

	var products []*types.Product
	err = dynamodbattribute.UnmarshalListOfMaps(result.Items, products)
	if err != nil {
		return nil, err
	}

	return products, nil
}

func (store *ProductStoreImpl) GetProductByID(id string) (*types.Product, error) {
	input := &dynamodb.GetItemInput{TableName: aws.String(ProductsTable),
		Key: map[string]*dynamodb.AttributeValue{
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

	var product *types.Product
	err = dynamodbattribute.UnmarshalMap(result.Item, product)
	if err != nil {
		return nil, err
	}

	return product, nil
}

func (store *ProductStoreImpl) CreateProduct(product *types.Product) (*types.Product, error) {
	item, err := dynamodbattribute.MarshalMap(product)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.PutItemInput{TableName: aws.String(ProductsTable), Item: item}

	_, err = store.database.Database.PutItem(input)
	if err != nil {
		return nil, err
	}

	return product, err
}

func (store *ProductStoreImpl) UpdateProduct(product *types.Product) (*types.Product, error) {
	updateExpression := "SET Name = : name, Description = : desc, Image = : img, Price = : price"
	input := &dynamodb.UpdateItemInput{
		TableName: aws.String(ProductsTable),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {
				S: aws.String(product.ID),
			},
		},
		ExpressionAttributeValues: map[string]*dynamodb.AttributeValue{
			":name":        {S: aws.String(product.Name)},
			":description": {S: aws.String(product.Description)},
			":image":       {S: aws.String(product.Image)},
			":price":       {N: aws.String(fmt.Sprintf("%f", product.Price))},
		},
		UpdateExpression: aws.String(updateExpression),
		ReturnValues:     aws.String("UPDATED_NEW"),
	}

	_, err := store.database.Database.UpdateItem(input)
	if err != nil {
		return nil, err
	}

	return product, nil
}

func (store *ProductStoreImpl) DeleteProduct(product *types.Product) error {
	input := &dynamodb.DeleteItemInput{
		TableName: aws.String(ProductsTable),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {
				S: aws.String(product.ID),
			},
		},
	}

	_, err := store.database.Database.DeleteItem(input)
	if err != nil {
		return err
	}

	return nil
}
