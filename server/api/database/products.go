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
	GetProductByID(id string) (*types.Product, error)
	CreateProduct(product *types.Product) (*types.Product, error)
	UpdateProduct(id string, product *types.Product) (*types.Product, error)
	DeleteProduct(id string) (*types.Product, error)
}

type ProductStoreImpl struct {
	db *lib.DynamoDBClient
}

func NewProductStore(db *lib.DynamoDBClient) *ProductStoreImpl {
	return &ProductStoreImpl{
		db: db,
	}
}

func (store *ProductStoreImpl) GetProducts() ([]*types.Product, error) {
	input := &dynamodb.ScanInput{TableName: aws.String(ProductsTable)}
	result, err := store.db.Database.Scan(input)
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

	result, err := store.db.Database.GetItem(input)
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

	input := &dynamodb.PutItemInput{
		TableName: aws.String(ProductsTable),
		Item:      item,
	}

	_, err = store.db.Database.PutItem(input)
	if err != nil {
		return nil, err
	}

	return product, nil
}

func (store *ProductStoreImpl) UpdateProduct(id string, product *types.Product) (*types.Product, error) {
	updateExpression := "SET Name = : name, Description = : desc, Image = : img, Price = : price"
	input := &dynamodb.UpdateItemInput{
		TableName: aws.String(ProductsTable),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {
				S: aws.String(id),
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

	_, err := store.db.Database.UpdateItem(input)
	if err != nil {
		return nil, err
	}

	return product, nil
}

func (store *ProductStoreImpl) DeleteProduct(id string) (*types.Product, error) {
	product, err := store.GetProductByID(id)
	if err != nil {
		return nil, err
	}

	input := &dynamodb.DeleteItemInput{
		TableName: aws.String(ProductsTable),
		Key: map[string]*dynamodb.AttributeValue{
			"id": {
				S: aws.String(id),
			},
		},
	}

	if _, err := store.db.Database.DeleteItem(input); err != nil {
		return nil, err
	}

	return product, nil
}
