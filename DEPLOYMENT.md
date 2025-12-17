# Deployment Guide

## Vercel Deployment

This application is ready to deploy on Vercel. Follow these steps:

### Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. A Neon PostgreSQL database (sign up at https://neon.tech)
3. GitHub repository connected to Vercel

### Frontend Deployment (Next.js)

1. **Import Repository to Vercel**
   - Go to https://vercel.com/new
   - Select your GitHub repository
   - Framework Preset: Next.js
   - Root Directory: `frontend`

2. **Configure Environment Variables**

   Add these environment variables in Vercel dashboard:

   ```env
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   NEXT_PUBLIC_APP_URL=https://your-frontend-url.vercel.app
   ```

3. **Deploy**
   - Click "Deploy"
   - Vercel will automatically build and deploy your frontend

### Backend Deployment Options

#### Option 1: Railway (Recommended for FastAPI)

1. Go to https://railway.app
2. Create new project from GitHub repository
3. Select the `backend` directory as root
4. Add environment variables:
   ```env
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   JWT_SECRET=your-secret-key-here
   BETTER_AUTH_SECRET=your-better-auth-secret
   BETTER_AUTH_URL=https://your-frontend-url.vercel.app
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   ```
5. Railway will auto-detect Python and deploy

#### Option 2: Render

1. Go to https://render.com
2. Create new Web Service
3. Connect your GitHub repository
4. Root Directory: `backend`
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables (same as Railway)

#### Option 3: Docker (Any Platform)

Use the included `docker-compose.yml` for containerized deployment:

```bash
docker-compose up -d
```

### Database Setup (Neon PostgreSQL)

1. **Create Neon Database**
   - Sign up at https://neon.tech
   - Create a new project
   - Copy the connection string

2. **Run Migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

3. **Update Environment Variables**
   - Add your Neon connection string to both frontend and backend env vars

### Environment Variables Summary

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET=your-secret-key-minimum-32-characters
BETTER_AUTH_SECRET=your-better-auth-secret-minimum-32-characters
BETTER_AUTH_URL=https://your-app.vercel.app
CORS_ORIGINS=https://your-app.vercel.app
ENVIRONMENT=production
LOG_LEVEL=info
```

### Post-Deployment Checklist

- [ ] Frontend accessible at Vercel URL
- [ ] Backend API responding (check /health endpoint)
- [ ] Database migrations applied
- [ ] Authentication working (login/register)
- [ ] CORS configured correctly
- [ ] Environment variables set properly
- [ ] SSL/HTTPS enabled

### Troubleshooting

#### CORS Errors
- Ensure `CORS_ORIGINS` includes your frontend URL
- Check that URLs don't have trailing slashes

#### Database Connection Issues
- Verify DATABASE_URL format
- Check Neon database is active
- Ensure IP allowlist includes your backend host

#### Build Failures
- Check Node.js version (should be 18+)
- Verify all dependencies in package.json
- Check build logs in Vercel dashboard

### Monitoring

- **Vercel Analytics**: Built-in analytics for frontend
- **Railway Logs**: Real-time logs for backend
- **Neon Monitoring**: Database performance metrics

### Scaling

- **Frontend**: Vercel automatically scales
- **Backend**:
  - Railway: Scale in dashboard
  - Render: Choose instance type
- **Database**: Neon auto-scales storage

## Local Development

```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Support

For issues, check:
- Vercel documentation: https://vercel.com/docs
- Railway documentation: https://docs.railway.app
- Neon documentation: https://neon.tech/docs
