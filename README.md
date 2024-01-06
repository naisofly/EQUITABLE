# streamlit-llm-chat-aws

Streamlit LLM Chat App on AWS

## reserve

create a Cognito user pool and a user pool client.

```bash
aws cloudformation deploy --template-file cloudformation/userpool.yaml --stack-name streamlit-chatgpt-userpool
```

The following three values are obtained.

* userpool id
* app client id
* client secret

1. userpool id:  
To obtain a list of user pools, execute the following command.

```bash
$ aws cognito-idp list-user-pools --max-results 20 | jq ".UserPools[] | {Id, Name}"
```
The value of `--max-results` can be adjusted accordingly to define the maximum number of user pools to be displayed.  
The results of the run will show a list of available Cognito user pools, including the ID of each.

2. app client id:  
Retrieve a list of app clients in the user pool using the retrieved user pool ID.

```bash
$ aws cognito-idp list-user-pool-clients --user-pool-id <userPoolId>
```

Replace `userPoolId` with the user pool ID obtained earlier. This command will list the ID for each client.

3. client secret:  
Once you know the app client ID, use the following command to obtain the client secret.

```bash
$ aws cognito-idp describe-user-pool-client --user-pool-id <userPoolId> --client-id <AppClientId>
```

Replace `userPoolId` with the user pool ID and `AppClientId` with the app client ID.
That is the client secret.

### environment setting

Write the OpenAPI access key, the model to be used, the user pool ID you just created, the app client ID, and the client secret in the `.env` file.


```
OPENAI_API_KEY=XX-XXXXX...
OPENAI_MODEL=gpt-4-1106-preview
POOL_ID=us-east-1_XXXXXX
APP_CLIENT_ID=XXXXX
APP_CLIENT_SECRET=XXXXXXX
```

## execute

### build a container

```bash
docker build ./ -t streamlit-app
```

### deploy on local

```bash
docker compose up -d
```

## deploy on AWS

