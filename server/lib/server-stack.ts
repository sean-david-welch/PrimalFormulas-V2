import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';

import * as s3 from 'aws-cdk-lib/aws-s3';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class ServerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'primalformulas.ie', {
      versioned: true,
    });

    // Define the Secrets Manager instance
    const secret = new secretsmanager.Secret(this, 'primalformulas.ie', {
      description: 'A secret for my Lambda functions',
    });

    // Define the DynamoDB table
    const table = new dynamodb.Table(this, 'primalformulas.ie', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
    });

    // Define the Lambda function for products
    const productsFunction = new lambda.Function(this, 'ProductsFunction', {
      runtime: lambda.Runtime.PROVIDED_AL2023,
      code: lambda.Code.fromAsset('path/to/products/build/directory'),
      handler: 'productsBinaryName',
    });

    // Define the Lambda function for about
    const aboutFunction = new lambda.Function(this, 'AboutFunction', {
      runtime: lambda.Runtime.PROVIDED_AL2023,
      code: lambda.Code.fromAsset('path/to/about/build/directory'),
      handler: 'aboutBinaryName',
    });

    // Define the Lambda function for assets
    const assetsFunction = new lambda.Function(this, 'AssetsFunction', {
      runtime: lambda.Runtime.PROVIDED_AL2023,
      code: lambda.Code.fromAsset('path/to/assets/build/directory'),
      handler: 'assetsBinaryName',
    });

    bucket.grantReadWrite(productsFunction);
    bucket.grantReadWrite(aboutFunction);
    bucket.grantReadWrite(assetsFunction);

    secret.grantRead(productsFunction);
    secret.grantRead(aboutFunction);
    secret.grantRead(assetsFunction);

    table.grantReadWriteData(productsFunction);
    table.grantReadWriteData(aboutFunction);
    table.grantReadWriteData(assetsFunction);

    // Define a single API Gateway
    const api = new apigateway.RestApi(this, 'MyApi', {
      restApiName: 'MyService',
    });

    // Define API Gateway resources and methods
    const productsResource = api.root.addResource('products');
    productsResource.addMethod('GET', new apigateway.LambdaIntegration(productsFunction));

    const aboutResource = api.root.addResource('about');
    aboutResource.addMethod('GET', new apigateway.LambdaIntegration(aboutFunction));

    const assetsResource = api.root.addResource('assets');
    assetsResource.addMethod('GET', new apigateway.LambdaIntegration(assetsFunction));
  }
}
