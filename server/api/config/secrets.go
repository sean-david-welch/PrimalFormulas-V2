package config

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/secretsmanager"
)

type Secrets struct {
	AwsRegionName       string `json:"AWS_REGION_NAME"`
	AwsAccessKey        string `json:"AWS_ACCESS_KEY"`
	AwsSecret           string `json:"AWS_SECRET_KEY"`
	StripeSecretKey     string `json:"STRIPE_SECRET_KEY"`
	StripeSecretKeyTest string `json:"TEST_SECRET_KEY"`
}

func getSecrets(secretName string) (*Secrets, error) {
	ctx := context.TODO()
	region := "eu-west-1"

	cfg, err := config.LoadDefaultConfig(ctx, config.WithRegion(region))
	if err != nil {
		return nil, fmt.Errorf("failed to load configuration: %w", err)
	}

	svc := secretsmanager.NewFromConfig(cfg)
	input := &secretsmanager.GetSecretValueInput{
		SecretId: aws.String(secretName),
	}

	result, err := svc.GetSecretValue(ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to get secret value: %w", err)
	}

	var secrets Secrets
	err = json.Unmarshal([]byte(*result.SecretString), &secrets)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal secret string: %w", err)
	}

	return &secrets, nil
}

func NewSecrets() (*Secrets, error) {
	secrets, err := getSecrets("primalformulasSecret")
	if err != nil {
		return nil, fmt.Errorf("failed to get secrets: %w", err)
	}

	return secrets, nil
}
