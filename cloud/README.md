# Case Study 4 cloud deployment

This directory deploys the same API-only ResumeLens image to all three required
providers. Account identifiers are supplied as environment variables. Do not
commit credentials, access tokens, subscription secrets, or downloaded key
files.

## Common local validation

```bash
docker build -f Dockerfile.cloud -t resumelens-api:cs4 .
docker run --rm -p 8080:8080 \
  -e PRODUCT_MODE=api \
  -e APP_PORT=8080 \
  resumelens-api:cs4
```

Open <http://localhost:8080>, enter a personal Hugging Face inference token in
the password field, and submit a synthetic resume. The token is used only for
that request and is not stored in the image.

## Vertex AI Gemini image on Docker Hub

After tests pass on a push to `main` or `case-study-4`, including the push
created by merging a pull request, GitHub Actions builds `Dockerfile.cloud`
with `INFERENCE_PROVIDER=vertex` and publishes `latest` and
`sha-<full-commit-sha>`.
To publish manually, run the workflow from `case-study-4`.
Set `DOCKER_REPOSITORY` to the Docker Hub `namespace/image` as a GitHub
repository secret or variable. Set the `DOCKER_API_KEY` repository secret
to a token with image push permission.
If the token belongs to a different Docker Hub account than the repository
namespace, set the repository variable `DOCKER_USERNAME` to that account.

To run the published image locally, set `GOOGLE_AGENT_PLATFORM_API_KEY` in
your local `.env` and replace `namespace/image` with your Docker Hub repository.

```bash
docker run --rm --env-file .env -p 8080:8080 namespace/image:latest
```

The image uses the Google Gen AI SDK in Vertex AI/Agent Platform Express Mode
with `genai.Client(vertexai=True, api_key=...)`, as required for Express Mode
API-key authentication.
Select Gemini 3.5 Flash-Lite or Gemini 3.5 Flash in the sidebar. To run the
image on a hosting platform, map its secret to the container's
`GOOGLE_AGENT_PLATFORM_API_KEY` environment variable. The key must have
access to both models on Agent Platform express mode.

## Provider order

1. Create the provider account and a low budget with email alerts.
2. Run the provider's deployment script from the repository root.
3. Test the printed public URL from a separate browser/network.
4. Save timestamped screenshots of the budget, deployment, public URL, and a
   successful synthetic request.
5. Enter the URL in the class Google Sheet.

The scripts create billable resources. Budgets are alerts, not hard spending
caps. Remove provider resources after grading if they are no longer required.
