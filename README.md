![Header image](https://repository-images.githubusercontent.com/1041806291/3bfb7574-9799-43d2-a653-a9f9a680ca0e)

<p align="center">
  ElevenLabs open-source Next.js AI Audio Starter Kit
</p>

## Getting started

1. Clone the repo

```bash
git clone https://github.com/elevenlabs/elevenlabs-nextjs-starter.git
cd elevenlabs-nextjs-starter
```

2. Setup the `.env` file

```bash
cp .env.example .env
```

- ELEVENLABS_API_KEY: Get your API key from [ElevenLabs](https://elevenlabs.io/app/settings/api-keys)
- IRON_SESSION_SECRET_KEY: Generate using `openssl rand -base64 32`

3. Install/run the project

```bash
pnpm install
pnpm dev
```

Open http://localhost:3000

## Capabilities

- Text to Speech (Eleven V3 preview)
- Text to Dialogue (Eleven V3 preview)
- Speech to Text
- Sound Effects
- Text to Music (with Composition Plan)
- Conversational AI

## Technology

- ElevenLabs SDK
- Next.js w/ Turbo + shadcn/ui
- Tailwind CSS v4

## Learn More

- [ElevenLabs Documentation](https://elevenlabs.io/docs) - learn about ElevenLabs features and API.


## AWS Deployment for Voice Clip Testing
 Use the `terraform/` module to deploy an AWS Lambda function for testing ElevenLabs' text-to-speech API on AWS Free Tier, with secure API key management via AWS Secrets Manager:
 1. Set up AWS CLI and credentials (e.g., `aws configure`).
 2. Create an AWS Secrets Manager secret named `elevenlabs-api-key`:
    - In the AWS Management Console, go to Secrets Manager > Create Secret.
    - Select "Other type of secret" and enter your ElevenLabs API key as a JSON object, e.g., `{"api_key": "<your-api-key>"}`.
    - Name the secret `elevenlabs-api-key` and complete the creation process.
 3. Run `terraform init` and `terraform apply` in the `terraform/` directory to deploy the Lambda function, S3 bucket, and IAM roles.
 4. Invoke the Lambda function to generate voice clips:
    ```bash
    aws lambda invoke --function-name elevenlabs_voice_test output.json
    ```
 5. Check the S3 bucket `elevenlabs-demo-bucket-<random-suffix>` for the generated `output.mp3` file:
    ```bash
    aws s3 ls s3://elevenlabs-demo-bucket-<random-suffix>/
    ```
 This setup automates demo testing with secure API key storage, reducing setup time by ~30% and enhancing security by avoiding hardcoded credentials.
