# Ollama + Med-Gemma Installation Guide

## Step 1: Install Ollama

### Windows Installation
1. Download Ollama for Windows from: https://ollama.ai/download/windows
2. Run the installer (`OllamaSetup.exe`)
3. Follow the installation wizard
4. Ollama will start automatically after installation

### Verify Installation
Open PowerShell and run:
```powershell
ollama --version
```

You should see output like: `ollama version 0.1.x`

## Step 2: Pull Med-Gemma 2B Model

In PowerShell, run:
```powershell
ollama pull medgemma:2b
```

This will download the Med-Gemma 2B model (~1.5GB). It may take a few minutes depending on your internet speed.

### Verify Model Installation
```powershell
ollama list
```

You should see `medgemma:2b` in the list of installed models.

## Step 3: Test Med-Gemma

Test the model directly:
```powershell
ollama run medgemma:2b
```

Try asking a medical question:
```
>>> I have diabetes, what should I eat?
```

Type `/bye` to exit the interactive mode.

## Step 4: Install Python Dependencies

Navigate to your backend directory:
```powershell
cd C:\Users\LENOVO\OneDrive\Desktop\Ayursutra\backend
```

Install new dependencies:
```powershell
pip install ollama chromadb sentence-transformers
```

## Step 5: Configure Environment Variables

Create or update `.env` file in the backend directory:
```env
# Existing
GEMINI_API_KEY=your_gemini_api_key_here

# New Med-Gemma Configuration
MED_GEMMA_DEPLOYMENT=ollama
MED_GEMMA_MODEL=medgemma:2b
MED_GEMMA_ENDPOINT=http://localhost:11434
```

## Step 6: Run Tests

Test the hybrid system:
```powershell
cd backend
python -m pytest test_hybrid_model.py -v
```

All tests should pass (using mock Med-Gemma for now).

## Step 7: Start Backend Server

Start the FastAPI backend:
```powershell
cd backend
uvicorn main:app --reload --port 8001
```

## Step 8: Test in Browser

1. Open browser: `http://localhost:3000`
2. Login as a patient
3. Open Health Agent Chat (bottom-right floating button)
4. Test queries:
   - **Medical Query**: "I have diabetes, what should I eat?"
     - Should use Med-Gemma
     - Check browser console for `ai_model_used: "med-gemma"`
   
   - **Ayurvedic Query**: "What is my dosha type?"
     - Should use Gemini Pro
     - Check browser console for `ai_model_used: "gemini-pro"`

## Troubleshooting

### Ollama Not Running
If you get connection errors, make sure Ollama is running:
```powershell
# Check if Ollama is running
Get-Process ollama

# If not running, start it
ollama serve
```

### Model Not Found
If Med-Gemma model is not found:
```powershell
# List installed models
ollama list

# Pull the model again if missing
ollama pull medgemma:2b
```

### Port Conflicts
If port 11434 is in use:
1. Find the process using the port:
   ```powershell
   netstat -ano | findstr :11434
   ```
2. Kill the process or change the port in `.env`

### GPU Issues
If you get GPU-related errors:
- Med-Gemma 2B should work on CPU, but it will be slower
- Make sure you have at least 4GB RAM available
- Close other applications to free up memory

## Performance Expectations

- **Med-Gemma 2B (GPU)**: ~1-2 seconds response time
- **Med-Gemma 2B (CPU)**: ~3-5 seconds response time
- **Gemini Pro (API)**: ~1-3 seconds response time

## Next Steps

Once everything is working:
1. Test with various medical and Ayurvedic queries
2. Monitor the logs to see which model is being used
3. Adjust query classification keywords if needed
4. Consider adding more medical conditions to the classifier

## Switching to HuggingFace (Optional)

If Ollama doesn't work well, you can switch to HuggingFace:

1. Get HuggingFace API key from: https://huggingface.co/settings/tokens
2. Update `.env`:
   ```env
   MED_GEMMA_DEPLOYMENT=huggingface
   HUGGINGFACE_API_KEY=your_hf_api_key_here
   ```
3. Install HuggingFace hub:
   ```powershell
   pip install huggingface-hub
   ```
4. Restart the backend server

## Using Mock Mode (For Testing)

To test without installing Ollama:
```env
MED_GEMMA_DEPLOYMENT=mock
```

This will use pre-defined responses for common medical queries.
