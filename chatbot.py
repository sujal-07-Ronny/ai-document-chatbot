
import boto3
from botocore.exceptions import ClientError

import os

REGION = os.getenv("AWS_REGION", "ap-south-1")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
MODEL_ARN = os.getenv("BEDROCK_MODEL_ARN")

if not KNOWLEDGE_BASE_ID or not MODEL_ARN:
    raise ValueError(
        "Set KNOWLEDGE_BASE_ID and BEDROCK_MODEL_ARN environment variables."
    )

client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)


def ask_question(question):
    try:
        response = client.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN
                }
            }
        )

        print("\nAnswer:")
        print(response["output"]["text"])

        citations = response.get("citations", [])
        sources = set()

        for citation in citations:
            for reference in citation.get("retrievedReferences", []):
                location = reference.get("location", {})
                s3_location = location.get("s3Location", {})
                uri = s3_location.get("uri")

                if uri:
                    sources.add(uri)

        if sources:
            print("\nSources:")
            for uri in sorted(sources):
                print("-", uri)
        else:
            print("\nNo source references returned.")

    except ClientError as error:
        print("AWS Error:", error.response["Error"]["Message"])


print("AI Document Chatbot")
print("Type 'exit' to quit.")

while True:
    question = input("\nAsk a question: ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        print("Please enter a question.")
        continue

    ask_question(question)
