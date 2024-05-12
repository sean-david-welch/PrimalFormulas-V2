package handlers

import (
	"github.com/aws/aws-lambda-go/events"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/services"
	"net/http"
)

type AboutHandler interface {
	GetAbouts(request events.APIGatewayProxyRequest) events.APIGatewayProxyResponse
}

type AboutHandlerImpl struct {
	service  services.AboutService
	response lib.ResponseHandler[interface{}]
}

func NewAboutHandler(service services.AboutService, response *lib.ResponseHandlerImpl[interface{}]) AboutHandlerImpl {
	return AboutHandlerImpl{service: service, response: response}
}

func (handler AboutHandlerImpl) GetAbouts(_ events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	abouts, err := handler.service.GetAbouts()
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	if abouts == nil {
		return handler.response.ErrorResponse(err, http.StatusNotFound)
	}

	return handler.response.SuccessResponse(abouts)
}

func (handler AboutHandlerImpl) GetAboutByID(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	id := request.PathParameters["id"]

	about, err := handler.service.GetAboutByID(id)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	if about == nil {
		return handler.response.ErrorResponse(err, http.StatusNotFound)
	}

	return handler.response.SuccessResponse(about)
}
