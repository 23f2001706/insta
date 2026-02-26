# Deployment Guide 🚀

Deploy your Instagram Gemini Bot to production.

## Platform Comparison

| Platform | Cost | Ease | Uptime | Auto-Scale |
|----------|------|------|--------|-----------|
| **Azure App Service** | $13+/month | ⭐⭐⭐ | 99.95% | ✅ |
| **AWS Lambda** | Pay per use | ⭐⭐ | 99.99% | ✅ |
| **Heroku** | $7+/month | ⭐⭐⭐⭐ | 99.9% | ✅ |
| **DigitalOcean App Platform** | $5+/month | ⭐⭐⭐ | 99.9% | ✅ |
| **Render** | Free/5+$ | ⭐⭐⭐⭐ | 99.9% | ✅ |

## 1. Azure App Service (Recommended)

### Step 1: Create App Service

```bash
#create resource group
az group create --name myResourceGroup --location eastus

# Create App Service Plan
az appservice plan create \
  --name myAppServicePlan \
  --resource-group myResourceGroup \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name insta-gemini-bot \
  --runtime "python|3.10"
```

### Step 2: Configure Environment Variables

Via Azure Portal:
1. Go to **Configuration** → **Application Settings**
2. Click **+ New application setting**
3. Add each variable from `.env`:

```
GEMINI_API_KEY = your_key_here
INSTAGRAM_APP_ID = your_app_id
INSTAGRAM_APP_SECRET = your_secret
INSTAGRAM_ACCESS_TOKEN = your_token
VERIFY_TOKEN = your_verify_token
BOT_PAGE_ID = your_page_id
BOT_INSTAGRAM_ID = your_instagram_id
GEMINI_MODEL = gemini-2.5-flash-lite
BOT_NAME = MyBot
BOT_INSTRUCTIONS = Your instructions here
```

### Step 3: Set Startup Command

1. Still in **Configuration** → **General Settings**
2. Find **Startup command**
3. Enter:
   ```
   gunicorn -w 4 -b 0.0.0.0:8000 --timeout 60 main:bot.app
   ```

### Step 4: Deploy Code

Option A: Deploy from Git

```bash
# Configure deployment user
az webapp deployment user set --user-name myUsername --user-password myPassword

# Set Git remote
git remote add azure https://myUsername@insta-gemini-bot.scm.azurewebsites.net:443/insta-gemini-bot.git

# Push to deploy
git push azure main
```

Option B: Deploy from GitHub

1. Go to **Deployment Center**
2. Select **GitHub**
3. Authorize and select your repository
4. Select branch: `main`
5. Click **Save**

### Step 5: Test Deployment

Your app will be at: `https://insta-gemini-bot.azurewebsites.net`

Test health endpoint:
```bash
curl https://insta-gemini-bot.azurewebsites.net/health
```

Response:
```json
{"status": "healthy", "bot": "MyBot"}
```

## 2. Heroku

### Step 1: Create App

```bash
heroku login
heroku create insta-gemini-bot
```

### Step 2: Set Environment Variables

```bash
heroku config:set GEMINI_API_KEY=your_key
heroku config:set INSTAGRAM_APP_ID=your_id
heroku config:set INSTAGRAM_APP_SECRET=your_secret
heroku config:set INSTAGRAM_ACCESS_TOKEN=your_token
heroku config:set VERIFY_TOKEN=your_token
heroku config:set BOT_PAGE_ID=your_page_id
heroku config:set BOT_INSTAGRAM_ID=your_instagram_id
```

### Step 3: Deploy

```bash
git push heroku main
```

Your app will be at: `https://insta-gemini-bot.herokuapp.com`

### Step 4: Monitor

```bash
heroku logs --tail
```

## 3. AWS Lambda + API Gateway

### Step 1: Create Lambda Function

```bash
# Create zip file
zip -r lambda_function.zip .

# Create IAM role
aws iam create-role --role-name instagram-bot-role \
  --assume-role-policy-document file://trust-policy.json

# Create Lambda function
aws lambda create-function \
  --function-name insta-gemini-bot \
  --runtime python3.10 \
  --role arn:aws:iam::ACCOUNT_ID:role/instagram-bot-role \
  --handler main:bot.app \
  --zip-file fileb://lambda_function.zip
```

### Step 2: Set Environment Variables

```bash
aws lambda update-function-configuration \
  --function-name insta-gemini-bot \
  --environment Variables='{
    GEMINI_API_KEY=your_key,
    INSTAGRAM_ACCESS_TOKEN=your_token,
    VERIFY_TOKEN=your_token
  }'
```

### Step 3: Create API Gateway

```bash
aws apigateway create-rest-api --name insta-bot-api
```

Configure in AWS Console or use SAM.

## 4. Docker Deployment

### Create Docker Image

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:bot.app"]
```

### Build and Run

```bash
# Build
docker build -t insta-bot .

# Run locally
docker run -e GEMINI_API_KEY=your_key \
           -e INSTAGRAM_ACCESS_TOKEN=your_token \
           -p 8000:8000 \
           insta-bot

# Push to Docker Hub
docker tag insta-bot yourusername/insta-bot
docker push yourusername/insta-bot
```

### Deploy to Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  bot:
    image: yourusername/insta-bot
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - INSTAGRAM_ACCESS_TOKEN=${INSTAGRAM_ACCESS_TOKEN}
      - VERIFY_TOKEN=${VERIFY_TOKEN}
      - BOT_PAGE_ID=${BOT_PAGE_ID}
```

Run with:
```bash
docker-compose up
```

## 5. Infrastructure as Code (Terraform)

```hcl
# main.tf
resource "azurerm_app_service" "bot" {
  name                = "insta-gemini-bot"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.plan.id

  app_settings = {
    GEMINI_API_KEY = var.gemini_key
    INSTAGRAM_ACCESS_TOKEN = var.instagram_token
    # ... other settings
  }
}
```

## 6. Configuration Best Practices

### Use Environment Variables (NOT hardcoded)

```python
# ✅ Good
import os
api_key = os.getenv("GEMINI_API_KEY")

# ❌ Bad
api_key = "AIzaSy..."  # Never hardcode!
```

### Secrets Management

- **Azure**: Use Azure Key Vault
- **AWS**: Use AWS Secrets Manager
- **Heroku**: Use config vars
- **General**: Never commit `.env` to git

### .gitignore

```
.env
.env.local
*.db
__pycache__/
venv/
```

## 7. Setting Up Custom Domain

### Azure

1. Go to **Custom domains**
2. Click **Add custom domain**
3. Configure DNS records
4. Verify domain

### Heroku

```bash
heroku domains:add www.mybot.com
```

Then update DNS to point to Heroku.

## 8. SSL/TLS Certificates

- **Azure**: Automatic (free)
- **Heroku**: Automatic (free)
- **AWS**: Use Let's Encrypt or AWS Certificate Manager
- **DigitalOcean**: Automatic with App Platform

## 9. Monitoring & Logging

### Azure

```bash
# View logs
az webapp log tail --name insta-gemini-bot --resource-group myGroup
```

### Heroku

```bash
heroku logs --tail
```

### AWS Lambda

```bash
aws logs tail /aws/lambda/insta-gemini-bot --follow
```

## 10. Auto-Scaling

### Azure

1. Go to **Scale up (App Service plan)**
2. Choose higher tier plan (S1, S2, P1v2)

### Heroku

```bash
heroku ps:scale web=2
```

## Common Issues

### Bot times out (timeout after 30s)

Increase timeout in startup command:

```
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 main:bot.app
```

### 503 Service Unavailable

- Check all environment variables are set
- Restart the app
- Check logs for errors

### Webhook verification fails

- Check VERIFY_TOKEN matches exactly
- Make sure URL is HTTPS
- Ensure domain is publicly accessible

### High memory usage

- Reduce number of gunicorn workers: `-w 2`
- Implement database cleanup
- Use serverless (Lambda) instead

## Cost Optimization

1. **Azure**: Use small B1 tier for low traffic
2. **Heroku**: Use free dyno for testing, Eco tier for low traffic
3. **AWS**: Use Lambda (pay per invocation) for low traffic
4. **DigitalOcean**: Start with $5/month tier

## Scaling Strategy

```
Development → Staging → Production

Development (Local)
  ↓
Staging (Heroku free tier)
  ↓
Production (Azure B1 tier)
  ↓
High Traffic (Azure S1+ / AWS Lambda / Kubernetes)
```

---

**Choose your platform and deploy! 🚀**
