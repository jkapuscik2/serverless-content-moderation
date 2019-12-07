## Serverless content moderation app 

Goal of this application is to present example of serverless content moderation with usage of AWS services. Details and motivation was described in the following [article](https://medium.com/@j.kapuscik2/building-serverless-content-moderation-app-with-aws-7907fbed513)

#### Installation

1. Install project dependecies `pip3 install -r requirements.txt`
2. Customize parameters in template.yaml file (e.g. target bucket name or DynamoDB table name)
3. Create new AWS S3 bucket 
4. Change `BUCKET_NAME` parameter in "build.sh" to name of created bucket
5. Execute building script with `sh build.sh` 
6. Change `STACK_NAME` parameter in "deploy.sh" script to desired CloudFormation Stack name
7. Deploy application with `sh deploy.sh`
