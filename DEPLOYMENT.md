# Vercel Deployment Guide for MachDatum RAG Chatbot

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Environment Variables**: You'll need to set your Gemini API key in Vercel

## Deployment Steps

### Step 1: Prepare Your Repository

The following files have been added/configured for Vercel deployment:
- `vercel.json` - Vercel configuration
- `.gitignore` - Excludes sensitive files
- Updated `app.py` - Proper environment variable handling

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Configure for Vercel deployment"
git push origin main
```

### Step 3: Deploy to Vercel

1. **Connect Repository**:
   - Go to [vercel.com](https://vercel.com) and log in
   - Click "New Project"
   - Import your GitHub repository: `https://github.com/Danushika06/RAG`

2. **Configure Environment Variables**:
   - In the Vercel dashboard, go to your project settings
   - Navigate to "Environment Variables"
   - Add the following variables:
     ```
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     FLASK_PORT=5000
     FLASK_DEBUG=False
     ```

3. **Deploy**:
   - Click "Deploy"
   - Vercel will automatically build and deploy your application

### Step 4: Access Your Application

Once deployed, Vercel will provide you with a URL like:
`https://your-project-name.vercel.app`

## Important Notes

### Security Considerations
- ❌ **Never commit API keys to GitHub**
- ✅ **Always use Vercel environment variables for sensitive data**
- ✅ **Set FLASK_DEBUG=False in production**

### File Structure for Vercel
```
your-app/
├── app.py              # Main Flask application (entry point)
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
├── .gitignore         # Excludes sensitive files
├── templates/         # Flask templates
└── other files...
```

### Common Issues and Solutions

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **Static Files**: Ensure templates are in the `templates/` folder
3. **Environment Variables**: Set all required env vars in Vercel dashboard
4. **Database Files**: Large files like `machdatum_rag_db.json` should be regenerated or stored elsewhere

### Production Optimizations

Consider these improvements for production:
- Use a proper database (PostgreSQL, MongoDB) instead of JSON files
- Implement caching for document embeddings
- Add rate limiting
- Use a CDN for static assets
- Monitor application performance

## Troubleshooting

If deployment fails:
1. Check Vercel build logs
2. Ensure all dependencies are in `requirements.txt`
3. Verify environment variables are set correctly
4. Check that the database file exists or can be created

## Next Steps After Deployment

1. Test all functionality on the live URL
2. Set up custom domain (optional)
3. Monitor application logs
4. Set up continuous deployment for automatic updates