# AI Document Chatbot using Amazon Bedrock

## Project Overview

This project is a Python-based AI Document Chatbot that answers questions using information from PDF documents stored in Amazon S3.

It uses Amazon Bedrock Knowledge Bases for Retrieval-Augmented Generation (RAG), Amazon Titan Text Embeddings V2 for embeddings, and Amazon Nova Micro for answer generation.

The chatbot returns answers with source document references and handles questions when the uploaded documents do not contain sufficient information.

## Architecture

1. PDF documents are stored in Amazon S3.
2. Amazon Bedrock Knowledge Bases processes and indexes the documents.
3. Titan Text Embeddings V2 generates embeddings for document retrieval.
4. Amazon S3 Vectors stores the vector data.
5. Python and Boto3 send user questions to the Knowledge Base.
6. Amazon Nova Micro generates answers using retrieved document content.
7. The chatbot displays the answer and unique source document paths.

## AWS Services and Tools

- Amazon S3
- Amazon Bedrock Knowledge Bases
- Amazon Titan Text Embeddings V2
- Amazon Nova Micro
- Amazon S3 Vectors
- AWS IAM
- Python
- Boto3

## Project Structure

```text
Chat LLM/
├── chatbot.py
├── create_sample_pdfs.py
├── sample_documents/
│   ├── employee_leave_policy.pdf
│   ├── it_support_policy.pdf
│   └── expense_policy.pdf
└── README.md
```

The `.venv` directory contains the local Python virtual environment and should not be uploaded to GitHub.

## Prerequisites

- Python
- AWS CLI
- Boto3
- An AWS account with the required IAM permissions
- An Amazon Bedrock Knowledge Base with documents synced
- Access to the selected Bedrock inference profile

## Setup and Execution

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows CMD:

```cmd
.venv\Scripts\activate
```

4. Install Boto3:

```bash
pip install boto3
```

5. Configure AWS CLI credentials securely:

```bash
aws configure
```

6. Verify AWS identity:

```bash
aws sts get-caller-identity
```

7. Update the AWS Region, Knowledge Base ID, and inference profile ARN in `chatbot.py` for your own AWS environment.
8. Run the chatbot:

```bash
python chatbot.py
```

Type `exit` to stop the chatbot.

## Sample Questions

| Question | Expected result |
|---|---|
| What is the annual casual leave allowance? | 12 days per calendar year |
| How many sick leave days are available annually? | 8 days per year |
| What is the maximum meal expense? | INR 500 |
| What is the employee's maternity leave policy? | Reports that the documents do not contain sufficient information |
| Who is the Prime Minister of Japan? | Reports that the documents do not contain sufficient information |

## Testing

The chatbot was tested with:

- Questions answered by the uploaded policy documents
- Questions unrelated to the uploaded documents
- Questions about policies not present in the documents
- Source reference display
- Duplicate source removal

## Security and Cost Considerations

- Do not commit AWS access keys, secret keys, passwords, or other credentials.
- Use an IAM identity with only the permissions required for the project.
- AWS charges may apply for Amazon Bedrock parsing, embeddings, model inference, S3 storage, and S3 Vectors usage.
- Review AWS billing and delete unused resources when the project is no longer needed.

## Learning Outcomes

- Understanding Retrieval-Augmented Generation (RAG)
- Creating and syncing an Amazon Bedrock Knowledge Base
- Using embeddings and vector search
- Calling Amazon Bedrock through Boto3
- Displaying source references
- Testing document-grounded answers
