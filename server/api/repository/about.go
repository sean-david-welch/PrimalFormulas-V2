package repository

import "github.com/sean-david-welch/primal-formulas/types"

type AboutStore interface {
	GetAbouts()
}

type AboutStoreImpl struct {
	database *types.DynamoDBClient
}

func NewAboutStore(database *types.DynamoDBClient) *AboutStoreImpl {
	return &AboutStoreImpl{database: database}
}
