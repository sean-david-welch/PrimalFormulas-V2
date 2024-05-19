package handlers

import (
	"encoding/json"
	"github.com/aws/aws-lambda-go/events"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/models"
	"github.com/sean-david-welch/primal-formulas/services"
	"net/http"
)

type AssetHandler interface {
	GetAssets(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
	GetAssetByID(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
	CreateAsset(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
	UpdateAsset(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
	DeleteAsset(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse
}

type AssetHandlerImpl struct {
	service  services.AssetService
	response lib.ResponseHandler[interface{}]
}

func NewAssetHandler(service services.AssetService, response lib.ResponseHandler[interface{}]) *AssetHandlerImpl {
	return &AssetHandlerImpl{
		service:  service,
		response: response,
	}
}

func (handler *AssetHandlerImpl) GetAssets(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	assets, err := handler.service.GetAssets()
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	if assets == nil {
		return handler.response.ErrorResponse(err, http.StatusNotFound)
	}

	return handler.response.SuccessResponse(assets, http.StatusOK)
}

func (handler *AssetHandlerImpl) GetAssetByID(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	id := request.PathParameters["id"]
	asset, err := handler.service.GetAssetByID(id)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	if asset == nil {
		return handler.response.ErrorResponse(err, http.StatusNotFound)
	}

	return handler.response.SuccessResponse(asset, http.StatusOK)
}

func (handler *AssetHandlerImpl) CreateAsset(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	var asset *models.Asset
	if err := json.Unmarshal([]byte(request.Body), &asset); err != nil {
		return handler.response.ErrorResponse(err, http.StatusBadRequest)
	}

	result, err := handler.service.CreateAsset(asset)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	return handler.response.SuccessResponse(result, http.StatusCreated)
}

func (handler *AssetHandlerImpl) UpdateAsset(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	var asset *models.Asset
	id := request.PathParameters["id"]

	if err := json.Unmarshal([]byte(request.Body), &asset); err != nil {
		return handler.response.ErrorResponse(err, http.StatusBadRequest)
	}

	result, err := handler.service.UpdateAsset(id, asset)
	if err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	return handler.response.SuccessResponse(result, http.StatusAccepted)
}

func (handler *AssetHandlerImpl) DeleteAsset(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
	id := request.PathParameters["id"]

	if err := handler.service.DeleteAsset(id); err != nil {
		return handler.response.ErrorResponse(err, http.StatusInternalServerError)
	}

	response := lib.GenerateResponseMessage(id, lib.DeleteAction)
	return handler.response.SuccessResponse(response, http.StatusOK)
}
