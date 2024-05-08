package handlers

import (
	"github.com/aws/aws-lambda-go/events"
	"github.com/sean-david-welch/primal-formulas/services"
)

type AboutHandler interface {
	GetAbouts()
}

type AboutHandlerImpl struct {
	service services.AboutService
}

func NewAboutHandler(service services.AboutService) AboutHandlerImpl {
	return AboutHandlerImpl{service: service}
}

func (handler AboutHandlerImpl) GetAbouts(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	return events.APIGatewayProxyResponse{}, nil
}
