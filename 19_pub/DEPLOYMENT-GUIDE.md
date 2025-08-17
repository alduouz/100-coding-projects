# Deployment Platform Guide

## Platform Comparison

| Platform | Free Tier | Persistent Storage | Auto-Sleep | Best For |
|----------|-----------|-------------------|------------|----------|
| **Railway** | 500 hrs/month | ✅ Volumes (1GB) | ❌ | Small apps, databases |
| **Render** | 750 hrs/month | ❌ Free tier | ✅ After 15min | Static/simple apps |
| **Fly.io** | 160 hrs/month | ✅ Volumes (3GB) | ✅ Configurable | Production apps |
| **Heroku** | Deprecated | ❌ | ✅ | Legacy (not recommended) |

## Recommended Choice Decision Tree

```
Do you need persistent data storage?
├── YES → Use Railway or Fly.io
│   ├── Simple app → Railway
│   └── Production app → Fly.io
└── NO → Use Render (simple & reliable)
```

## Pre-Deployment Checklist

Run this command before deploying:
```bash
./test-deployment.sh
```

## Common Pitfalls

1. **Virtual Environment**: Always exclude with `.dockerignore`
2. **Database Init**: Call `init_database()` at module level, not in `if __name__ == '__main__'`
3. **Port Binding**: Use `host='0.0.0.0'` and `PORT` environment variable
4. **File Paths**: Use absolute paths and environment variables
5. **Platform Config**: Start minimal, add config only if needed

## Emergency Debugging

If deployment fails:
1. Check platform logs for exact error
2. Verify all files in checklist exist
3. Test gunicorn locally: `gunicorn app:app --bind 0.0.0.0:8000`
4. Check environment variables are set
5. Verify database initialization runs without errors