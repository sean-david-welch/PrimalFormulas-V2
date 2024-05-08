package types

import (
	"context"
	"fmt"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/credentials"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go/aws"
	"net/url"
	"strings"
	"time"
)

type S3Client interface {
	GeneratePresignedUrl(folder, image string) (string, string, error)
	DeleteImageFromS3(imageUrl string) error
}

type S3ClientImpl struct {
	Client *s3.Client
}

func NewS3Client(region, accessKey, secretKey string) (*S3ClientImpl, error) {
	conf, err := config.LoadDefaultConfig(context.TODO(),
		config.WithRegion(region),
		config.WithCredentialsProvider(credentials.
			NewStaticCredentialsProvider(accessKey, secretKey, "session")),
	)
	if err != nil {
		return nil, err
	}

	return &S3ClientImpl{
		Client: s3.NewFromConfig(conf),
	}, nil
}

func (client *S3ClientImpl) GeneratePresignedUrl(image string) (string, string, error) {
	const bucketName = "primalformulas.ie"
	const cloudfrontDomain = "https://www.primalformulas.ie"

	imageKey := fmt.Sprintf("images/%s", image)
	imageUrl := fmt.Sprintf("%s/%s", cloudfrontDomain, imageKey)

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	presignedClient := s3.NewPresignClient(client.Client)

	req, err := presignedClient.PresignPutObject(ctx, &s3.PutObjectInput{
		Bucket: aws.String(bucketName),
		Key:    aws.String(imageKey),
	}, s3.WithPresignExpires(5*time.Minute))

	if err != nil {
		return "", "", fmt.Errorf("error generating presigned URL: %w", err)
	}

	return req.URL, imageUrl, nil
}

func (client *S3ClientImpl) DeleteImageFromS3(imageUrl string) error {
	const bucketName = "primalformulas.ie"

	parsedUrl, err := url.Parse(imageUrl)
	if err != nil {
		return fmt.Errorf("error parsing URL: %w", err)
	}
	key := strings.TrimPrefix(parsedUrl.Path, "/")

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	_, err = client.Client.DeleteObject(ctx, &s3.DeleteObjectInput{
		Bucket: aws.String(bucketName),
		Key:    aws.String(key),
	})

	if err != nil {
		return fmt.Errorf("error deleting object from s3: %w", err)
	}

	return nil
}
