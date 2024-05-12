// ResponseHandler defines the interface for handling API responses
type ResponseHandler interface {
ErrorResponse(err error, statusCode int) events.APIGatewayProxyResponse
SuccessResponse(data interface{}) events.APIGatewayProxyResponse
}

// DefaultResponseHandler implements the ResponseHandler interface
type DefaultResponseHandler struct{}

func (h *DefaultResponseHandler) ErrorResponse(err error, statusCode int) events.APIGatewayProxyResponse {
return events.APIGatewayProxyResponse{
StatusCode: statusCode,
Body:       err.Error(),
}
}

func (h *DefaultResponseHandler) SuccessResponse(data interface{}) events.APIGatewayProxyResponse {
body, err := json.Marshal(data)
if err != nil {
return h.ErrorResponse(fmt.Errorf("failed to marshal data: %v", err), http.StatusInternalServerError)
}
return events.APIGatewayProxyResponse{
StatusCode: http.StatusOK,
Headers:    map[string]string{"Content-Type": "application/json"},
Body:       string(body),
}
}

// Usage in handlers
func (handler AboutHandlerImpl) GetAbouts(request events.APIGatewayProxyRequest, respHandler ResponseHandler) events.APIGatewayProxyResponse {
abouts, err := handler.service.GetAbouts()
if err != nil {
return respHandler.ErrorResponse(err, http.StatusInternalServerError)
}
if abouts == nil {
return respHandler.ErrorResponse(errors.New("No about information found"), http.StatusNotFound)
}
return respHandler.SuccessResponse(abouts)
}
