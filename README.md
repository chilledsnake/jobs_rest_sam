# Jobs Rest API (with IaaC)

This project deploys a RESTful API using the FastAPI framework, leveraging AWS SAM (Serverless Application Model) to define the infrastructure as code and DynamoDB Table as a database.

## Infrastructure: AWS SAM

AWS SAM is a framework for building serverless applications. It provides a way to define your application's resources and dependencies using YAML or JSON templates. The template.yaml file in this project defines the necessary AWS resources, such as API Gateway, Lambda functions, and IAM roles.

## Database: DynamoDB Table

DynamoDB is a fully managed NoSQL database service provided by Amazon Web Services. It offers fast and predictable performance with seamless scalability. The API uses DynamoDB to store job data.

* This repository does not contain local DynamoDB setup, if You want to run locally, you need to setup local DynamoDB instance.
* For pytest setup, I use `moto` library to mock DynamoDB locally.

## Project Structure

- **app/**: Contains the FastAPI application code.
- **layers/fastapi/**: Directory containing dependencies for the FastAPI layer.
- **tests/**: Unit tests for the application.
- **poetry.lock**: Poetry lock file to manage Python dependencies.
- **pyproject.toml**: Poetry configuration file.
- **template.yaml**: AWS SAM template defining the infrastructure.

## Local Development

### Prerequisites
- Install AWS SAM CLI: [AWS SAM CLI Installation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Install Python 3.13
- Install Poetry: [Poetry Installation](https://python-poetry.org/docs/#installation)

### Using Makefile

The `Makefile` provides targets to help with local development:

```sh
make all       # Runs imports, format, typecheck, and test
make test      # Runs all tests
make format    # Formats code using ruff
make imports   # Sorts imports using isort
make typecheck # Checks for type errors using mypy
```

### Running the API Locally

# Create a virtual environment
```sh
python -m venv .venv  #Make sure that you are creating the virtual environment with Python 3.13.
```

# Activate the virtual environment
```sh
source .venv/bin/activate
```

# Install dependencies using Poetry
```sh
pip install poetry
```

# Install dependencies using Poetry
```sh
poetry install --no-root
```

## Adding New Packages

The project uses **Poetry** with two dependency groups:

| Group | Purpose | File entry |
|-------|---------|------------|
| `fastapi` | Packages needed **at runtime** (included in the Lambda layer). | `[tool.poetry.group.fastapi.dependencies]` |
| `dev`     | Development‑only tools (linters, test frameworks, type checkers). | `[tool.poetry.group.dev.dependencies]` |

### 1️⃣ Add a package to the **FastAPI runtime** group

```bash
# Example: add `httpx` (HTTP client)
poetry add httpx --group fastapi
```

- The dependency will appear under `[tool.poetry.group.fastapi.dependencies]` in `pyproject.toml`.
- **After adding** a runtime package you must rebuild the Lambda layer (see *Updating the FastAPI Lambda Layer* above).

### 2️⃣ Add a package to the **dev** group

```bash
# Example: add `black` as a formatter
poetry add black --group dev
```

- The dependency will be listed under `[tool.poetry.group.dev.dependencies]`.
- Dev packages are **not** shipped with the Lambda layer, so no extra build step is required.

### 3️⃣ Re‑build the Lambda layer (if you added to `fastapi`)

```bash
poetry export \
    -f requirements.txt \
    --without-hashes \
    --only fastapi \
    -o layers/fastapi/requirements.txt

sam build          # rebuilds the layer with the new deps
```

### 4️⃣ Verify the layer size (recommended)

```bash
du -sh .aws-sam/build/FastApiLayer/python
# Aim for ≤ 250 MB (uncompressed) to stay under Lambda limits.
```

### 5️⃣ Deploy (if you want the new version in the cloud)

```bash
sam deploy
```

> **Tip:** Add `layers/fastapi/requirements.txt` to version control so the CI pipeline can rebuild the layer automatically whenever a PR modifies the `fastapi` dependency group.

There are two ways to run the API locally:

1. **Using AWS SAM:**
   ```sh
   sam build && sam local start-api
   ```

2. **Using Uvicorn:**
   ```sh
   uvicorn app.main:app --reload
   ```

## Deployment

To deploy the API using AWS SAM, follow these steps:

1. Ensure you have the necessary permissions to create and manage AWS resources.
2. Configure your AWS credentials.
3. Deploy the stack:
   ```sh
   sam build
   sam deploy --guided
   ```

Follow the prompts to provide required parameters such as the environment, API domain, certificate ARN, and hosted zone ID.

## Public API

- **API Endpoint:** `https://jobs-rest-api.ownspace.cloud`
- **Interactive OpenAPI Documentation:**
  - Swagger UI: `https://jobs-rest-api.ownspace.cloud/docs`
  - ReDoc: `https://jobs-rest-api.ownspace.cloud/redoc`

## API Endpoints

- **v1:info:** `/v1/info/`
- **v1:jobs:get** `/v1/jobs/{company}/{time_stamp}/`
- **v1:jobs:list** `/v1/jobs/`
- **v1:jobs:post** `/v1/jobs/`
- **v1:jobs:update** `/v1/jobs/{company}/{time_stamp}/`
- **v1:jobs:delete** `/v1/jobs/{company}/{time_stamp}/`

## Contributions

Contributions to this project are welcome. Please ensure that your code adheres to the formatting and type-checking standards defined in the Makefile.

## License

This project is licensed under the MIT License.
