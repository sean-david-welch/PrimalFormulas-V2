package api

import (
	"encoding/json"
	"github.com/aws/aws-lambda-go/events"
	"github.com/sean-david-welch/primal-formulas/config"
	"github.com/sean-david-welch/primal-formulas/database"
	"github.com/sean-david-welch/primal-formulas/handlers"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/services"
	"log"
	"net/http"
)

func Handler(request events.APIGatewayProxyRequest) (*events.APIGatewayProxyResponse, error) {
	secrets, err := config.NewSecrets()
	if err != nil {
		log.Fatalf("Error loading configuration: %v", err)
	}

	s3Client, err := lib.NewS3Client(secrets.AwsRegionName, secrets.AwsAccessKey, secrets.AwsSecret)
	if err != nil {
		log.Fatalf("Failed to create S3 client: %v", err)
	}

	dbClient := lib.NewDynamoDBClient()
	aboutStore := database.NewAboutStore(dbClient)
	aboutService := services.NewAboutService(aboutStore, s3Client)

	responseHandler := lib.NewResponseHandler[interface{}]()
	aboutHandler := handlers.NewAboutHandler(aboutService, responseHandler)

	handlersMap := map[string]func(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse{
		"GET": func(request events.APIGatewayProxyRequest) *events.APIGatewayProxyResponse {
			if _, ok := request.PathParameters["id"]; ok {
				return aboutHandler.GetAboutByID(request)
			}
			return aboutHandler.GetAbouts(request)
		},
		"POST":   aboutHandler.CreateAbout,
		"PUT":    aboutHandler.UpdateAbout,
		"DELETE": aboutHandler.DeleteAbout,
	}

	if handler, exists := handlersMap[request.HTTPMethod]; exists {
		return handler(request), nil
	}

	message := map[string]string{
		"message": "method not allowed",
	}
	msg, _ := json.Marshal(message)
	return &events.APIGatewayProxyResponse{
		StatusCode: http.StatusMethodNotAllowed,
		Body:       string(msg),
	}, nil
}
