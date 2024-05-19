package config

import (
	"encoding/json"
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/secretsmanager"
)

type Secrets struct {
	AwsRegionName       string `json:"AWS_REGION_NAME"`
	AwsAccessKey        string `json:"AWS_ACCESS_KEY"`
	AwsSecret           string `json:"AWS_SECRET_KEY"`
	StripeSecretKey     string `json:"STRIPE_SECRET_KEY"`
	StripeSecretKeyTest string `json:"TEST_SECRET_KEY"`
}

func getSecrets(secretName string) (*Secrets, error) {
	region := "eu-west-1"
	sess := session.Must(session.NewSession(&aws.Config{
		Region: aws.String(region),
	}))

	svc := secretsmanager.New(sess)
	input := &secretsmanager.GetSecretValueInput{
		SecretId: aws.String(secretName),
	}

	result, err := svc.GetSecretValue(input)
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
	secrets, err := getSecrets("primalformulas.ie")
	if err != nil {
		return nil, fmt.Errorf("failed to get secrets: %w", err)
	}

	return secrets, nil
}
