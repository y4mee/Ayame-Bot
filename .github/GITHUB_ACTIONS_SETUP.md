# GitHub Actions Setup Guide

## Step 1: Add Bot Token as Secret

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `BOT_TOKEN`
5. Value: Paste your Discord bot token from `.env`
6. Click **Add secret**

## Step 2: Verify Workflow

1. Go to **Actions** tab in your repository
2. You should see "Scheduled Bot Tasks" workflow
3. The workflow will run automatically every 14 minutes
4. You can also manually trigger it by clicking "Run workflow"

## Step 3: Monitor Execution

- Click on the workflow run to see logs
- Check the "Run scheduled tasks" step for output
- GitHub Actions provides free minutes for public repos (2000/month for private)

## Customizing the Schedule

Edit `.github/workflows/scheduled-tasks.yml` and change the cron expression:

- `*/14 * * * *` - Every 14 minutes (current)
- `0 * * * *` - Every hour
- `0 0 * * *` - Daily at midnight UTC
- `0 */6 * * *` - Every 6 hours

[Cron expression reference](https://crontab.guru/)

## Adding More Tasks

Edit `backend/scheduled_tasks.py` to add more periodic tasks:

```python
async def run_scheduled_tasks():
    # ... existing code ...
    
    @bot.event
    async def on_ready():
        # ... existing code ...
        
        # Add your tasks here
        await my_custom_task()
        
        await bot.close()

async def my_custom_task():
    logger.info("Running custom task...")
    # Your task logic here
```

## Troubleshooting

- **Workflow not running**: Check that the `.github/workflows/scheduled-tasks.yml` file is in the main branch
- **Token error**: Verify the `BOT_TOKEN` secret is set correctly in Settings
- **Rate limiting**: GitHub Actions has rate limits; adjust cron frequency if needed
