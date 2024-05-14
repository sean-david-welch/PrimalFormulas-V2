package main

import (
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/sean-david-welch/primal-formulas/routes"
)

func Handler(request events.APIGatewayProxyRequest) (*events.APIGatewayProxyResponse, error) {
	return routes.AboutRouter(request)
}

func main() {
	lambda.Start(Handler)
}
