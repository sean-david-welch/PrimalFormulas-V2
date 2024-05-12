package lib

import (
	"encoding/json"
	"fmt"
	"github.com/aws/aws-lambda-go/events"
	"net/http"
)

type ResponseHandler[T any] interface {
	ErrorResponse(err error, statusCode int) *events.APIGatewayProxyResponse
	SuccessResponse(data interface{}) *events.APIGatewayProxyResponse
}

type ResponseHandlerImpl[T any] struct{}

func (response *ResponseHandlerImpl[T]) ErrorResponse(err error, statusCode int) *events.APIGatewayProxyResponse {
	return &events.APIGatewayProxyResponse{
		StatusCode: statusCode,
		Body:       err.Error(),
	}
}

func (response *ResponseHandlerImpl[T]) SuccessResponse(data T) *events.APIGatewayProxyResponse {
	body, err := json.Marshal(data)
	if err != nil {
		return response.ErrorResponse(
			fmt.Errorf("failed to marshal data: %v", err), http.StatusInternalServerError)
	}

	return &events.APIGatewayProxyResponse{
		StatusCode: http.StatusOK,
		Headers:    map[string]string{"Content-Type": "application/json"},
		Body:       string(body),
	}
}
