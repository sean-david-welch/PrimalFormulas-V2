package lib

import (
	"encoding/json"
	"fmt"
	"github.com/aws/aws-lambda-go/events"
	"net/http"
)

type ActionType string

const (
	CreateAction ActionType = "create"
	UpdateAction ActionType = "update"
	DeleteAction ActionType = "delete"
)

type ResponseHandler[T any] interface {
	ErrorResponse(err error, statusCode int) *events.APIGatewayProxyResponse
	SuccessResponse(data interface{}, statusCode int) *events.APIGatewayProxyResponse
}

type ResponseHandlerImpl[T any] struct{}

func NewResponseHandler[T any]() *ResponseHandlerImpl[T] {
	return &ResponseHandlerImpl[T]{}
}
func GenerateResponseMessage(id string, action ActionType) map[string]string {
	switch action {
	case CreateAction:
		return map[string]string{
			"message": fmt.Sprintf("Successfully created resource with ID: %s", id),
		}
	case UpdateAction:
		return map[string]string{
			"message": fmt.Sprintf("Successfully updated resource with ID: %s", id),
		}
	case DeleteAction:
		return map[string]string{
			"message": fmt.Sprintf("successfully deleted resource with ID: %s", id),
		}
	default:
		return map[string]string{
			"message": fmt.Sprintf("unsupported action"),
		}
	}
}

func (response *ResponseHandlerImpl[T]) ErrorResponse(err error, statusCode int) *events.APIGatewayProxyResponse {
	return &events.APIGatewayProxyResponse{
		StatusCode: statusCode,
		Body:       err.Error(),
	}
}

func (response *ResponseHandlerImpl[T]) SuccessResponse(data T, statusCode int) *events.APIGatewayProxyResponse {
	body, err := json.Marshal(data)
	if err != nil {
		return response.ErrorResponse(
			fmt.Errorf("failed to marshal data: %v", err), http.StatusInternalServerError)
	}

	return &events.APIGatewayProxyResponse{
		StatusCode: statusCode,
		Headers:    map[string]string{"Content-Type": "application/json"},
		Body:       string(body),
	}
}
