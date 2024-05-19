package lib

import (
	"context"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"log"
)

type DynamoDBClient struct {
	Database *dynamodb.Client
}

func NewDynamoDBClient() *DynamoDBClient {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion("us-west-1"))
	if err != nil {
		log.Fatalf("unable to load SDK config, %v", err)
	}

	database := dynamodb.NewFromConfig(cfg)

	return &DynamoDBClient{
		Database: database,
	}
}
