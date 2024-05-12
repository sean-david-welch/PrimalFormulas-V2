package config

import (
	"fmt"
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

func NewSecrets() (*Secrets, error) {

	env := os.Getenv("ENV")
	if env != "production" {
		if err := godotenv.Load(".env"); err != nil {
			return nil, fmt.Errorf("failed to load configurations file: %w", err)
		}
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
