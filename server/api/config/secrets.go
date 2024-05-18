package config

import (
	"encoding/json"
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/secretsmanager"
	"github.com/joho/godotenv"
	"os"
)

type Secrets struct {
	DatabaseURL         string
	AwsRegionName       string
	AwsAccessKey        string
	AwsSecret           string
	StripeSecretKey     string
	StripeSecretKeyTest string
}

func getSecrets(secretName string) (*Secrets, error) {
	region := os.Getenv("eu-west-1")
	sess := session.Must(session.NewSession(&aws.Config{
		Region: aws.String(region),
	}))

	svc := secretsmanager.New(sess)
	input := &secretsmanager.GetSecretValueInput{
		SecretId: aws.String(secretName),
	}

	result, err := svc.GetSecretValue(input)
	if err != nil {
		return nil, err
	}

	var secrets Secrets
	err = json.Unmarshal([]byte(*result.SecretString), &secrets)
	if err != nil {
		return nil, err
	}

	return &secrets, nil
}

func NewSecrets() (*Secrets, error) {
	env := os.Getenv("ENV")
	if env != "production" {
		if err := godotenv.Load(".env"); err != nil {
			return nil, fmt.Errorf("failed to load configurations file: %w", err)
		}

		return &Secrets{
			// Database
			DatabaseURL: os.Getenv("DATABASE_URL"),
			// AWS
			AwsRegionName: os.Getenv("AWS_REGION_NAME"),
			AwsAccessKey:  os.Getenv("AWS_ACCESS_KEY"),
			AwsSecret:     os.Getenv("AWS_SECRET_KEY"),
			// Stripe
			StripeSecretKey:     os.Getenv("STRIPE_SECRET_KEY"),
			StripeSecretKeyTest: os.Getenv("TEST_SECRET_KEY"),
		}, nil
	}

	secrets, err := getSecrets("your-secret-id")
	if err != nil {
		return nil, fmt.Errorf("failed to get secrets: %w", err)
	}

	return secrets, nil
}
