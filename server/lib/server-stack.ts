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

    const secret = new secretsmanager.Secret(this, 'primalformulas.ie', {
      description: 'A secret for my Lambda functions',
    });

    const table = new dynamodb.Table(this, 'primalformulas.ie', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
    });

    const methods: string[] = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']

    const functions = [
      {
        name: 'ProductsFunction',
        path: 'bin/products/function.zip',
        handler: 'bootstrap',
      },
      {
        name: 'AboutFunction',
        path: 'bin/about/function.zip',
        handler: 'bootstrap',
      },
      {
        name: 'AssetsFunction',
        path: 'bin/assets/function.zip',
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
