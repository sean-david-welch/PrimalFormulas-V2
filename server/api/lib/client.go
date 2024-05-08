package types

import (
	"context"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/credentials"
	"github.com/aws/aws-sdk-go-v2/service/s3"
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
		config.WithCredentialsProvider(credentials.NewStaticCredentialsProvider(accessKey, secretKey, "session")),
	)
	if err != nil {
		return nil, err
	}

	return &S3ClientImpl{
		Client: s3.NewFromConfig(conf),
	}, nil
}
