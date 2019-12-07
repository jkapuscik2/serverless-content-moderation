## Serverless content moderation app 

Goal of this application is to present example of serverless content moderation with usage of AWS services. Details and motivation was described in the following [article](https://medium.com/@j.kapuscik2/building-serverless-content-moderation-app-with-aws-7907fbed513)

#### Installation

1. Customize parameters in template.yaml file (e.g. target bucket name or DynamoDB table name)
2. Create new AWS S3 bucket 
3. Change `BUCKET_NAME` parameter in "build.sh" to name of created bucket
4. Execute building script with `sh build.sh` 
5. Change `STACK_NAME` parameter in "deploy.sh" script to desired CloudFormation Stack name
6. Deploy application with `sh deploy.sh`
