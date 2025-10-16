# Using Google Gemini API

This chatbot now uses **Google Gemini 2.0 Flash** - a powerful and **FREE** AI model!

## 🎉 Why Gemini?

-   ✅ **Completely Free** - No credit card required
-   ✅ **Fast** - Optimized for speed
-   ✅ **Powerful** - Great at understanding context
-   ✅ **Generous Rate Limits** - 1500 requests per day on free tier
-   ✅ **Long Context** - Can handle large amounts of information

## 🔑 Getting Your Free API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (it looks like: `AIzaSyD...`)

## ⚙️ Configuration

Add your API key to `.env`:

```env
GOOGLE_API_KEY=AIzaSyD-your-actual-key-here
```

## 📊 Available Models

You can choose different Gemini models in your `.env` file:

| Model                  | Description                               | Best For                    |
| ---------------------- | ----------------------------------------- | --------------------------- |
| `gemini-2.0-flash-exp` | Latest experimental flash model (default) | Fast responses, general use |
| `gemini-1.5-flash`     | Stable flash model                        | Production use              |
| `gemini-1.5-pro`       | More powerful model                       | Complex queries             |

To change the model, edit `.env`:

```env
LLM_MODEL=gemini-1.5-pro
```

## 🆚 Gemini vs OpenAI

| Feature               | Gemini 2.0 Flash | GPT-3.5-turbo       |
| --------------------- | ---------------- | ------------------- |
| **Cost**              | FREE             | ~$0.001 per request |
| **Speed**             | Very Fast        | Fast                |
| **Context Length**    | 1M tokens        | 16K tokens          |
| **Rate Limit (Free)** | 1500/day         | N/A (paid only)     |
| **Quality**           | Excellent        | Excellent           |

## 💡 Tips for Best Results

1. **Be Specific**: Ask clear, specific questions about calendar events
2. **Use Context**: Reference dates, semesters, or event types
3. **Check Sources**: The chatbot returns source documents for verification

## 🔧 Troubleshooting

### Rate Limit Errors

If you hit rate limits (1500 requests/day on free tier):

-   Wait 24 hours for reset
-   Or upgrade to paid tier for higher limits
-   Consider caching common queries

### API Key Issues

**Error**: "Invalid API key"

**Solution**:

-   Double-check your key in `.env`
-   Make sure there are no extra spaces
-   Regenerate key if needed at https://aistudio.google.com/app/apikey

### Model Not Found

**Error**: "Model not found"

**Solution**: Use one of these supported models:

-   `gemini-2.0-flash-exp`
-   `gemini-1.5-flash`
-   `gemini-1.5-pro`

## 📚 Additional Resources

-   [Google AI Studio](https://aistudio.google.com/)
-   [Gemini API Documentation](https://ai.google.dev/docs)
-   [Gemini Pricing](https://ai.google.dev/pricing)
-   [LangChain Gemini Integration](https://python.langchain.com/docs/integrations/chat/google_generative_ai)

## 🚀 Quick Start

```bash
# 1. Get your free API key
# Visit: https://aistudio.google.com/app/apikey

# 2. Add to .env
echo "GOOGLE_API_KEY=your-key-here" > backend/.env

# 3. Run the app
cd backend
./setup.sh
./run.sh

# 4. Test it!
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "When are exams?"}'
```

## 🎓 Example Queries

The chatbot works great with natural language:

-   "When is Spring break?"
-   "What holidays do we have in Fall semester?"
-   "Tell me about examination dates"
-   "When does the academic year start?"
-   "Are there any events in March?"

Happy chatting! 🎉
