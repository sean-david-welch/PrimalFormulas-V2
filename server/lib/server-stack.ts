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
      websiteIndexDocument: 'index.html',
      websiteErrorDocument: 'index.html',
      cors: [
        {
          allowedOrigins: ['*'],
          allowedMethods: [
            s3.HttpMethods.GET,
            s3.HttpMethods.HEAD,
            s3.HttpMethods.POST,
            s3.HttpMethods.PUT,
            s3.HttpMethods.DELETE,
          ],
          allowedHeaders: ['*'],
          maxAge: 3000,
        },
      ],
    });

    const secrets = {
      AWS_REGION_NAME: process.env.AWS_REGION_NAME,
      AWS_ACCESS_KEY: process.env.AWS_ACCESS_KEY,
      AWS_SECRET_KEY: process.env.AWS_SECRET_KEY,
      STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
      TEST_SECRET_KEY: process.env.TEST_SECRET_KEY,
    };

    const secret = new secretsmanager.Secret(this, 'primalformulasSecret', {
      description: 'Environment variables for PrimalFormulas serverless API',
      secretStringValue: cdk.SecretValue.unsafePlainText(JSON.stringify(secrets)),
    });

    const table = new dynamodb.Table(this, 'primalformulasStore', {
      partitionKey: { name: 'pk', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'sk', type: dynamodb.AttributeType.STRING },
    });

    const methods: string[] = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']

    const functions = [
      {
        name: 'ProductsFunction',
        path: './api/bin/products/function.zip',
        handler: 'bootstrap',
      },
      {
        name: 'AboutFunction',
        path: './api/bin/about/function.zip',
        handler: 'bootstrap',
      },
      {
        name: 'AssetsFunction',
        path: './api/bin/assets/function.zip',
        handler: 'bootstrap',
      },
    ];

    const lambdaFunctions = functions.map(func => {
      return new lambda.Function(this, func.name, {
        runtime: lambda.Runtime.PROVIDED_AL2023,
        code: lambda.Code.fromAsset(func.path),
        handler: func.handler,
        environment: {
          BUCKET_NAME: bucket.bucketName,
          SECRET_NAME: secret.secretName,
          TABLE_NAME: table.tableName,
        },
      });
    });

    lambdaFunctions.forEach(func => {
      bucket.grantReadWrite(func);
      secret.grantRead(func);
      table.grantReadWriteData(func);
    });

    const api = new apigateway.RestApi(this, 'PrimalFormulasAPI', {
      restApiName: 'PrimalFormulas',
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: methods,
      },
      deployOptions: {
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
      },
    });

    const resources = [
      {
        path: 'products',
        function: lambdaFunctions[0],
      },
      {
        path: 'about',
        function: lambdaFunctions[1],
      },
      {
        path: 'assets',
        function: lambdaFunctions[2],
      },
    ];

    resources.forEach(resource => {
      const apiResource = api.root.addResource(resource.path);
        methods.forEach(method => {
        apiResource.addMethod(method, new apigateway.LambdaIntegration(resource.function));
      });
    });
  }
}
