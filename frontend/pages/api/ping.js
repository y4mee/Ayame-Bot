export default async function handler(req, res) {
  const BOT_URL = 'https://ayame-bot.onrender.com/health';
  
  try {
    console.log(`[${new Date().toISOString()}] Pinging bot...`);
    
    const response = await fetch(BOT_URL, {
      method: 'GET',
      headers: {
        'User-Agent': 'Ayame-Bot-KeepAlive/1.0'
      }
    });
    
    if (response.ok) {
      const data = await response.text();
      console.log(`[${new Date().toISOString()}] ✅ Bot is awake: ${data}`);
      
      return res.status(200).json({
        success: true,
        message: 'Bot pinged successfully',
        botStatus: 'online',
        timestamp: new Date().toISOString()
      });
    } else {
      console.log(`[${new Date().toISOString()}] ⚠️ Bot responded with status: ${response.status}`);
      
      return res.status(200).json({
        success: true,
        message: 'Bot pinged but returned non-200 status',
        botStatus: 'slow',
        statusCode: response.status,
        timestamp: new Date().toISOString()
      });
    }
  } catch (error) {
    console.error(`[${new Date().toISOString()}] ❌ Failed to ping bot:`, error.message);
    
    return res.status(200).json({
      success: false,
      message: 'Failed to ping bot',
      botStatus: 'offline',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
}
