# Python JSON File Server

A simple Flask web application that serves JSON files from the `.well-known` folder.

## Features

- Serves JSON files from the `.well-known` directory
- URL pattern: `/well-known/<filename>.json`
- Basic homepage with usage instructions
- Error handling for missing files

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Access the homepage:
```
http://localhost:5000/
```

3. Access JSON files:
```
http://localhost:5000/well-known/example.json
```

## Adding JSON Files

Simply add JSON files to the `.well-known` folder and access them via:
```
http://localhost:5000/well-known/<your-file>.json
```

## Example

The repository includes an `example.json` file in the `.well-known` folder that you can use as a reference.

## Azure Web App Deployment

This application is configured to work with Azure Web Apps. To deploy:

### Option 1: Using Azure CLI
```bash
# Create a resource group (if needed)
az group create --name myResourceGroup --location eastus

# Create an App Service plan
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux

# Create a web app
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name <your-app-name> --runtime "PYTHON|3.11"

# Deploy from local git
az webapp deployment source config-local-git --name <your-app-name> --resource-group myResourceGroup
```

### Option 2: Using Azure Portal
1. Create a new Web App in Azure Portal
2. Select Python 3.11 as the runtime stack
3. Go to **Configuration** → **General settings**
4. Set the startup command: `gunicorn --bind 0.0.0.0:${PORT:-8000} app:app`
5. Deploy your code via Git, GitHub, or ZIP deploy

### Option 3: ZIP Deploy (Recommended if having deployment issues)
```bash
# Create a ZIP file of your project (excluding venv, __pycache__, etc.)
zip -r deploy.zip . -x "*.git*" "*venv*" "*__pycache__*" "*.pyc"

# Deploy using Azure CLI
az webapp deployment source config-zip \
  --resource-group <your-resource-group> \
  --name <your-app-name> \
  --src deploy.zip
```

### Troubleshooting JSON Parse Error
If you encounter "Failed to parse response text: SyntaxError: JSON.parse" error:

1. **Remove any `.deployment` file** - Azure Python apps don't need it
2. **Use ZIP deploy instead** of Git deployment (see Option 3 above)
3. **Set startup command manually** in Azure Portal:
   - Go to Configuration → General settings
   - Set startup command: `gunicorn --bind 0.0.0.0:${PORT:-8000} app:app`
4. **Check Application Settings** in Azure Portal:
   - Ensure `SCM_DO_BUILD_DURING_DEPLOYMENT` is set to `true` (if needed)
   - Ensure `WEBSITES_ENABLE_APP_SERVICE_STORAGE` is set to `false` (default)

### Important Notes:
- Azure automatically detects Flask apps, but explicitly setting the startup command is recommended
- The app uses the `PORT` environment variable that Azure provides
- Make sure the `.well-known` folder is included in your deployment
- For ZIP deploy, ensure `.well-known` folder is included in the ZIP

