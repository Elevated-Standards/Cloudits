#!/bin/bash

# Define the base AWS profile that has permissions to assume all roles
BASE_PROFILE="default"  # Change this if using a different AWS profile

set_aws_env() {
    ROLE_ARN=$1
    SESSION_NAME=$2

    # Assume the role from the base profile
    CREDS=$(aws sts assume-role --profile "$BASE_PROFILE" --role-arn "$ROLE_ARN" --role-session-name "$SESSION_NAME" --query 'Credentials' --output json)

    if [ $? -ne 0 ]; then
        echo "Failed to assume role: $ROLE_ARN"
        return 1
    fi

    # Extract credentials
    ACCESS_KEY_ID=$(echo $CREDS | jq -r '.AccessKeyId')
    SECRET_ACCESS_KEY=$(echo $CREDS | jq -r '.SecretAccessKey')
    SESSION_TOKEN=$(echo $CREDS | jq -r '.SessionToken')

    # Export credentials
    export AWS_ACCESS_KEY_ID=$ACCESS_KEY_ID
    export AWS_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY
    export AWS_SESSION_TOKEN=$SESSION_TOKEN

    echo "AWS session set for $SESSION_NAME"
    echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID"
    echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY"
    echo "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN"
}

echo "Assuming AWS roles..."

echo "Setting Development Environment..."
set_aws_env "<PLACEHOLDER>" "dev"

echo "Setting Operations Environment..."
set_aws_env "<PLACEHOLDER>" "ops"

echo "Setting Production Environment..."
set_aws_env "<PLACEHOLDER>" "prod"

echo "All AWS environments set!"




