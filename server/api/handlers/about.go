package handlers

import (
	"encoding/json"
	"github.com/aws/aws-lambda-go/events"
	"github.com/sean-david-welch/primal-formulas/services"
	"net/http"
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

func (handler AboutHandlerImpl) GetAbouts(request events.APIGatewayProxyRequest) events.APIGatewayProxyResponse {
	abouts, err := handler.service.GetAbouts()
	if err != nil {
		return events.APIGatewayProxyResponse{
			StatusCode: http.StatusInternalServerError,
			Body:       err.Error(),
		}
	}

	if abouts == nil {
		return events.APIGatewayProxyResponse{
			StatusCode: http.StatusNotFound,
			Body:       "No about information found",
		}
	}

	body, err := json.Marshal(abouts)
	if err != nil {
		return events.APIGatewayProxyResponse{
			StatusCode: http.StatusInternalServerError,
			Body:       "Failed to parse abouts data",
		}
	}

	return events.APIGatewayProxyResponse{
		StatusCode: http.StatusOK,
		Headers:    map[string]string{"Content-Type": "application/json"},
		Body:       string(body),
	}
}
