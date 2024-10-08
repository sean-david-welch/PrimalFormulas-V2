package main

import (
	"encoding/json"
	"fmt"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/sean-david-welch/primal-formulas/config"
	"github.com/sean-david-welch/primal-formulas/database"
	"github.com/sean-david-welch/primal-formulas/handlers"
	"github.com/sean-david-welch/primal-formulas/lib"
	"github.com/sean-david-welch/primal-formulas/services"
	"log"
	"net/http"
)

func main() {
	lambda.Start(Handler)
}

func Handler(request events.APIGatewayProxyRequest) (*events.APIGatewayProxyResponse, error) {
	secrets, err := config.NewSecrets()
	if err != nil {
		log.Printf("Error loading configurationsL %v", err)
		return &events.APIGatewayProxyResponse{
			StatusCode: http.StatusMethodNotAllowed,
			Body:       fmt.Sprintf("Error loading secrets configurations: %v", err),
		}, nil
	}

	s3Client, err := lib.NewS3Client(secrets.AwsRegionName, secrets.AwsAccessKey, secrets.AwsSecret)
	if err != nil {
		log.Printf("Failed to create s3 client: %v", err)
		return &events.APIGatewayProxyResponse{
			StatusCode: http.StatusMethodNotAllowed,
			Body:       fmt.Sprintf("Error loading s3 configurations: %v", err),
		}, nil
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

	msg, _ := json.Marshal(map[string]string{
		"message": "method not allowed",
	})

	return &events.APIGatewayProxyResponse{
		StatusCode: http.StatusMethodNotAllowed,
		Body:       string(msg),
	}, nil
}
