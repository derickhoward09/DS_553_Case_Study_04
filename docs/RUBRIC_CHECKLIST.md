# Case Study 4 rubric checklist

## AWS deployment - 20 points

- [x] AWS student/basic account created. (3)
- [x] $1 early-warning and $5 monthly AWS budgets created with actual and
  forecast alerts. (3)
- [x] Docker API product deployed to ECS Express Mode/Fargate in `us-east-2`.
  (10)
- [x] Public URL obtained:
  <https://re-02876f5ce57d49f1a8d0dca2940fbcd9.ecs.us-east-2.on.aws/>
- [ ] Enter the URL in the class Google Sheet and screenshot the row. (4)

## AWS setup process - 4 points

- [x] Document image, port, task size, region, public ingress, runtime variables,
  validation, and the student-account IAM limitation.
- [x] Record commit `cb38c24` and immutable Docker tag.

## Reflection and cloud comparison - 6 points

- [x] Discuss IAM/secret-management, architecture, ports, deployment bake time,
  post-deployment inference smoke testing, and cost cleanup.
- [x] Include the full LLM prompt, model name, full response, and independent
  MLOps provider choice in the report draft.

## Automated deployment - 15 points

- [x] GitHub Action runs 53 tests and automatically builds/publishes the cloud
  Docker image to Docker Hub with immutable SHA and `latest` tags.
- [x] Published digest is verified by the workflow.
- [ ] A workflow-driven deployment to ECS is not implemented. If the instructor
  interprets this item as requiring deployment rather than cloud publication,
  configure the existing Azure deployment workflow or add AWS OIDC + ECS update.

## Vertex AI extra credit - 10 points

- [x] `google-genai` is included in the cloud dependencies.
- [x] ResumeLens implements the Vertex AI Gemini call and returns model text
  when the provider accepts the credentials.
- [x] Express Mode authentication uses
  `genai.Client(vertexai=True, api_key=...)`.
- [x] Vertex routing/error tests pass.
- [ ] Replace the current ECS runtime credential with a valid Express Mode
  Generative Language API key, or configure OAuth/ADC if the Google project was
  upgraded. Revision 6 currently reaches Vertex but receives `401
  UNAUTHENTICATED` requesting OAuth2 credentials.
- [ ] Save a successful live synthetic request and response after fixing the
  provider credential.

## Submission evidence

- [x] AWS budget screenshot
- [x] ECS Active/1 running/Deployment Success screenshot
- [x] Public AWS URL
- [x] Docker image name, immutable tag, digest, Git commit, and successful
  GitHub Action URL/run number
- [ ] Final Vertex sample request/response
- [ ] Class Google Sheet row screenshot
- [ ] Group member names
- [ ] Any GCP and Azure account/deployment evidence required elsewhere in the
  full assignment rubric
