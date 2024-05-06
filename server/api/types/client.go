package types

import "github.com/aws/aws-sdk-go-v2/service/s3"

type S3Client interface {
	GeneratePresignedUrl(folder, image string) (string, string, error)
	DeleteImageFromS3(imageUrl string) error
}

type S3ClientImpl struct {
	Client *s3.Client
}
