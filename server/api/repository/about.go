package repository

import "github.com/sean-david-welch/primal-formulas/types"

type AboutStore interface{}

type AboutStoreImpl struct {
	database *types.DynamoDBClient
}
