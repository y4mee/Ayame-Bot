# Bot Recovery System

## What It Does

When your bot restarts (after a crash or Render spin-down), the recovery system automatically:

✅ **Restores all guild configurations** - XP system settings are preserved  
✅ **Verifies reward roles** - Checks that all roles still exist  
✅ **Validates log channels** - Ensures channels are still accessible  
✅ **Removes invalid roles** - Cleans up deleted roles from database  
✅ **Sends recovery notifications** - Notifies admins that bot is back online  
✅ **Runs periodic health checks** - Every 30 minutes to catch issues early  

## How It Works

1. **On Startup**: `restore_guild_configs()` runs automatically
   - Loads all guild settings from database
   - Verifies channels and roles still exist
   - Removes any deleted roles
   - Sends notification to log channels

2. **Periodic Health Checks**: Every 30 minutes
   - Checks database connectivity
   - Verifies bot connection
   - Scans for corrupted data
   - Logs any issues found

3. **Error Handling**: All commands have error handlers
   - Slash command errors are caught and reported
   - Users get helpful error messages
   - Errors are logged for debugging

## What Gets Preserved

✅ **User XP Data** - All XP and levels are stored in database  
✅ **Guild Settings** - Log channel, auto-roles setting  
✅ **Reward Roles** - All level-to-role mappings  
✅ **Activity Streaks** - User activity tracking  

## What Happens on Crash

**Before Recovery System:**
- Bot goes offline
- Guild settings lost
- Users need to run `/setxpsystem` again
- Reward roles need to be reconfigured

**After Recovery System:**
- Bot goes offline
- Recovery system restores everything on restart
- Users see recovery notification
- Everything works immediately

## Testing Recovery

To test the recovery system:

1. Run the bot normally
2. Set up XP system: `/setxpsystem #channel create_roles:true theme:anime`
3. Stop the bot (Ctrl+C)
4. Start it again
5. Check the log channel for recovery notification
6. Verify roles are still assigned with `/rank`

## Monitoring

Check logs for recovery status:

```
🔄 Starting guild configuration recovery...
📋 Restoring config for YourServer (ID: 123456)
✅ Log channel verified: xp-logs
✅ Level 1: 🌸 Sakura Seed
✅ Recovery complete: 1 guilds restored
📢 Recovery notifications sent to 1 channels
```

## Troubleshooting

**Recovery notification not appearing?**
- Check that log channel still exists
- Verify bot has permission to send messages
- Check bot logs for errors

**Roles not restored?**
- Verify roles weren't deleted
- Check bot has permission to manage roles
- Run `/rewardslist` to see current roles

**Health check warnings?**
- Invalid roles are automatically removed
- Check bot logs for specific issues
- Restart bot to trigger full recovery
