import os
import re
import boto3
from botocore.config import Config
from langchain_aws import BedrockEmbeddings, ChatBedrock

aws_region = os.getenv("AWS_REGION", "us-east-1")
bedrock_config = Config(
    connect_timeout=120, read_timeout=120, retries={"max_attempts": 0}
)

def get_bedrock_run_time():
    session = boto3.Session(profile_name="ba-dev")
    bedrock_rt = session.client(
        "bedrock-runtime", region_name=aws_region, config=bedrock_config
    )
    return bedrock_rt


def get_chat_bedrock_llm():
    model_kwargs = {
        "max_tokens": 512,
        "temperature": 0.0,
    }
    llm = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        config=bedrock_config,
        region_name=aws_region,
        verbose=True,
        credentials_profile_name="ba-dev",
        client=get_bedrock_run_time(),
        model_kwargs=model_kwargs,
    )
    return llm

def get_bedrock_embeddings():
    bedrock_embeddings = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0", client=get_bedrock_run_time()
    )
    return bedrock_embeddings