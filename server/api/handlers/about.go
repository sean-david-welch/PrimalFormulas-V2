package handlers

import (
	"encoding/json"
	"github.com/aws/aws-lambda-go/events"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/services"
	"github.com/sean-david-welch/primal-formulas/types"
	"net/http"
)

type AboutHandler interface {
	GetAbouts(request events.APIGatewayProxyRequest) events.APIGatewayProxyResponse
}

type AboutHandlerImpl struct {
	service  services.AboutService
	response lib.ResponseHandler[interface{}]
}

func NewAboutHandler(service services.AboutService, response *lib.ResponseHandlerImpl[interface{}]) *AboutHandlerImpl {
	return &AboutHandlerImpl{service: service, response: response}
}

func (handler *AboutHandlerImpl) GetAbouts(_ events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	abouts, err := handler.service.GetAbouts()
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	if abouts == nil {
		return handler.response.ErrorResponse(err, http.StatusNotFound)
	}

	return handler.response.SuccessResponse(abouts, http.StatusOK)
}

func (handler *AboutHandlerImpl) GetAboutByID(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	id := request.PathParameters["id"]

	about, err := handler.service.GetAboutByID(id)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	if about == nil {
		return handler.response.ErrorResponse(err, http.StatusNotFound)
	}

	return handler.response.SuccessResponse(about, http.StatusOK)
}

func (handler *AboutHandlerImpl) CreateAbout(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	var about *types.About
	if err := json.Unmarshal([]byte(request.Body), &about); err != nil {
		return handler.response.ErrorResponse(err, http.StatusBadRequest)
	}

	result, err := handler.service.CreateAbout(about)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	return handler.response.SuccessResponse(result, http.StatusCreated)
}

func (handler *AboutHandlerImpl) UpdateAbout(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	var about *types.About
	id := request.PathParameters["id"]

	if err := json.Unmarshal([]byte(request.Body), &about); err != nil {
		return handler.response.ErrorResponse(err, http.StatusBadRequest)
	}

	result, err := handler.service.UpdateAbout(id, about)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	return handler.response.SuccessResponse(result, http.StatusAccepted)
}

func (handler *AboutHandlerImpl) DeleteAbout(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	id := request.PathParameters["id"]

	if err := handler.service.DeleteAbout(id); err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	response := lib.GenerateResponseMessage(id, "update")
	return handler.response.SuccessResponse(response, http.StatusOK)
}
