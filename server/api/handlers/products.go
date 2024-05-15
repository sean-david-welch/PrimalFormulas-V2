package handlers

import (
	"encoding/json"
	"github.com/aws/aws-lambda-go/events"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/services"
	"github.com/sean-david-welch/primal-formulas/types"
	"net/http"
)

type ProductHandler interface {
	GetProducts(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
	GetProductByID(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
	CreateProduct(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
	UpdateProduct(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
	DeleteProduct(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
}

type ProductHandlerImpl struct {
	service  services.ProductService
	response lib.ResponseHandler[interface{}]
}

func NewProductHandler(service services.ProductService, response lib.ResponseHandler[interface{}]) *ProductHandlerImpl {
	return &ProductHandlerImpl{service: service, response: response}
}

func (handler *ProductHandlerImpl) GetProducts(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	products, err := handler.service.GetProducts()
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	if products == nil {
		return handler.response.ErrorResponse(err, http.StatusNotFound)
	}

	return handler.response.SuccessResponse(products, http.StatusOK)
}

func (handler *ProductHandlerImpl) GetProductByID(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	id := request.PathParameters["id"]

	product, err := handler.service.GetProductByID(id)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	if product == nil {
		return handler.response.ErrorResponse(err, http.StatusNotFound)
	}

	return handler.response.SuccessResponse(product, http.StatusOK)
}

func (handler *ProductHandlerImpl) CreateProduct(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	var product *types.Product
	if err := json.Unmarshal([]byte(request.Body), &product); err != nil {
		return handler.response.ErrorResponse(err, http.StatusBadRequest)
	}

	result, err := handler.service.CreateProduct(product)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	return handler.response.SuccessResponse(result, http.StatusCreated)
}

func (handler *ProductHandlerImpl) UpdateProduct(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	var product *types.Product
	id := request.PathParameters["id"]

	if err := json.Unmarshal([]byte(request.Body), &product); err != nil {
		return handler.response.ErrorResponse(err, http.StatusBadRequest)
	}

	result, err := handler.service.UpdateProduct(id, product)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}
	return handler.response.SuccessResponse(result, http.StatusAccepted)
}

func (handler *ProductHandlerImpl) DeleteProduct(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	id := request.PathParameters["id"]

	if err := handler.service.DeleteProduct(id); err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	response := lib.GenerateResponseMessage(id, lib.DeleteAction)
	return handler.response.SuccessResponse(response, http.StatusOK)
}
