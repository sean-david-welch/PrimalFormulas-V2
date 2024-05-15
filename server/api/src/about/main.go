package main

import (
	"encoding/json"
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

	switch request.HTTPMethod {
	case "GET":
		if _, ok := request.PathParameters["id"]; ok {
			return aboutHandler.GetAboutByID(request), nil
		}
		return aboutHandler.GetAbouts(request), nil
	case "POST":
		return aboutHandler.CreateAbout(request), nil
	case "PUT":
		return aboutHandler.UpdateAbout(request), nil
	case "DELETE":
		return aboutHandler.DeleteAbout(request), nil
	default:
		message := map[string]string{
			"message": "method not allowed",
		}
		msg, _ := json.Marshal(message)
		return &events.APIGatewayProxyResponse{
			StatusCode: http.StatusMethodNotAllowed,
			Body:       string(msg),
		}, nil
	}
}
