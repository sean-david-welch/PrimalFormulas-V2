package handlers

import (
	"github.com/aws/aws-lambda-go/events"
	"github.com/sean-david-welch/primal-formulas/database"
)

type AboutHanlder interface {
	GetAbouts()
}

type AboutHandlerImpl struct {
	store database.AboutStore
}

func NewAboutHandler(store *database.AboutStoreImpl) AboutHandlerImpl {
	return AboutHandlerImpl{store: store}
}

func (handler AboutHandlerImpl) GetAbouts(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	return events.APIGatewayProxyResponse{}, nil
}
