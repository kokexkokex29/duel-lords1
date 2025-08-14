# 👑 Duel Lords - BombSquad Tournament Discord Bot

<div align="center">

![Duel Lords](https://img.shields.io/badge/Duel%20Lords-Tournament%20Bot-7289da?style=for-the-badge&logo=discord)
![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=for-the-badge&logo=python)
![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-7289da?style=for-the-badge&logo=discord)
![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-000000?style=for-the-badge&logo=flask)

A comprehensive Discord bot for managing BombSquad tournaments with beautiful web dashboard, advanced statistics tracking, automated match scheduling, and multilingual support.

</div>

## 🎮 Features Overview

### 🤖 Discord Bot Features
- **Modern Slash Commands** - Full Discord integration with slash command interface
- **Admin-Controlled Registration** - Secure player management system
- **Automated Match Scheduling** - Discord timestamps with timezone support
- **Comprehensive Statistics** - Win/loss records, K/D ratios, match history
- **Smart Reminder System** - 5-minute pre-match DM notifications
- **Server Information Display** - Quick access to BombSquad server details
- **Beautiful Embed Messages** - Professional tournament-styled Discord embeds
- **Multi-language Support** - Full English and Portuguese localization

### 🌐 Web Dashboard Features
- **Live Tournament Leaderboard** - Real-time rankings with interactive charts
- **Player Statistics Visualization** - Comprehensive stats with progress bars
- **Discord-Inspired Dark Theme** - Beautiful, responsive UI design
- **Interactive Charts & Graphs** - Statistics visualization with Chart.js
- **Mobile-Responsive Design** - Works perfectly on all devices
- **24/7 Keep-Alive System** - Continuous bot operation monitoring
- **Performance Monitoring** - Real-time bot status and health checks

### 🎯 BombSquad Server Details
- **Official Server IP**: `18.228.228.44`
- **Port**: `3827`
- **Game**: BombSquad Tournament Server
- **Region**: Global Access

## 🚀 Complete Deployment Guide for Render.com

### Prerequisites
- Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)
- Free Render.com account
- GitHub account (optional but recommended)

### Step 1: Create Your Discord Bot

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications
   - Click "New Application"
   - Name it "Duel Lords" (or your preferred name)

2. **Configure Bot Settings**
   - Navigate to "Bot" section in left sidebar
   - Click "Add Bot"
   - Copy the bot token (keep this secret!)
   - Enable required privileged intents:
     - ✅ Message Content Intent
     - ✅ Server Members Intent (optional)
     - ✅ Presence Intent (optional)

3. **Set Bot Permissions**
   - Go to "OAuth2" → "URL Generator"
   - Scopes: `bot` and `applications.commands`
   - Bot Permissions:
     - ✅ Send Messages
     - ✅ Use Slash Commands
     - ✅ Send Messages in Threads
     - ✅ Embed Links
     - ✅ Attach Files
     - ✅ Read Message History
     - ✅ Add Reactions
     - ✅ Manage Messages (optional)
   - Copy the generated invite URL

4. **Invite Bot to Server**
   - Use the invite URL to add bot to your Discord server
   - Make sure you have Administrator permissions

### Step 2: Deploy on Render.com

#### Option A: Direct GitHub Deploy (Recommended)
1. **Fork This Repository**
   - Click "Fork" on this GitHub repository
   - Clone to your GitHub account

2. **Connect to Render**
   - Go to [Render.com Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your forked repository

#### Option B: Manual Deploy
1. **Upload Code**
   - Download this repository as ZIP
   - Create new GitHub repository
   - Upload all files
   - Follow Option A steps

#### Step 3: Configure Render Service

```yaml
# Render Configuration
Name: duel-lords-tournament-bot
Environment: Python 3
Region: Choose closest to your users
Branch: main (or your preferred branch)

# Build Settings
Build Command: pip install -r requirements.txt
Start Command: python main.py

# Advanced Settings
Auto-Deploy: Yes (recommended)
```

#### Step 4: Environment Variables Setup

In Render dashboard, add these environment variables:

| Variable Name | Description | Example/Notes |
|---------------|-------------|---------------|
| `DISCORD_TOKEN` | Your Discord bot token | `MTxxxxx.xxxxxx.xxxxxxx` |
| `SESSION_SECRET` | Random secret for web sessions | `your-super-secret-random-key` |

**Optional Variables:**
| Variable Name | Default | Description |
|---------------|---------|-------------|
| `DEBUG` | `False` | Enable debug logging |
| `DEFAULT_LANGUAGE` | `en` | Default bot language (en/pt) |
| `MAX_TOURNAMENT_PLAYERS` | `32` | Maximum players per tournament |
| `REMINDER_MINUTES` | `5` | Match reminder time |

### Step 5: Deploy & Verify

1. **Deploy Service**
   - Click "Create Web Service"
   - Wait for deployment (usually 2-3 minutes)
   - Check logs for any errors

2. **Test Bot Connection**
   - Your bot should appear online in Discord
   - Try `/help` command in your server
   - Check web dashboard at your Render URL

3. **Verify Website**
   - Visit your Render service URL
   - Should see Duel Lords homepage
   - Test leaderboard page

## 📱 Discord Commands Reference

### 👥 General Commands (Anyone can use)
| Command | Description | Usage |
|---------|-------------|-------|
| `/server_info` | Show BombSquad server details | `/server_info` |
| `/player_stats [player]` | Display player statistics | `/player_stats @username` |
| `/leaderboard` | Show tournament rankings | `/leaderboard` |
| `/all_players` | List all registered players | `/all_players` |
| `/help` | Display all available commands | `/help` |

### 👑 Admin Commands (Administrators only)
| Command | Description | Usage |
|---------|-------------|-------|
| `/register_player` | Register new tournament player | `/register_player @username` |
| `/remove_player` | Remove player from tournament | `/remove_player @username` |
| `/schedule_match` | Schedule match between players | `/schedule_match @player1 @player2 25 14 30` |
| `/update_stats` | Update player statistics | `/update_stats @player wins:2 kills:5` |

### 📅 Match Scheduling Format
```
/schedule_match @player1 @player2 [day] [hour] [minute]
```
- **Day**: Day of month (1-31)
- **Hour**: Hour in 24h format (0-23)  
- **Minute**: Minute (0-59)
- **Timezone**: Automatically uses server timezone

**Example**: `/schedule_match @John @Mike 25 14 30` 
- Schedules match for 25th of current month at 2:30 PM

## 🗂️ Project Structure

```
duel-lords/
├── 🤖 Bot Core
│   ├── main.py              # Application entry point
│   ├── bot.py               # Discord bot implementation
│   ├── database.py          # Database management
│   ├── scheduler.py         # Match reminder system
│   └── models.py            # SQLAlchemy data models
├── 🌐 Web Dashboard  
│   ├── app.py               # Flask web application
│   ├── templates/           # HTML templates
│   │   ├── index.html       # Homepage
│   │   └── leaderboard.html # Tournament rankings
│   └── static/              # CSS, JS, assets
│       ├── style.css        # Dark theme styling
│       └── script.js        # Interactive features
├── 🛠️ Utilities
│   ├── translations.py      # Multi-language support
│   ├── utils.py             # Helper functions
│   └── requirements.txt     # Python dependencies
└── 📋 Documentation
    ├── README.md            # This file
    └── .env.example         # Environment variables template
```

## 🎨 Web Dashboard Pages

### 🏠 Homepage (`/`)
- Bot status indicator
- Feature overview
- Command reference  
- Quick navigation links

### 🏆 Leaderboard (`/leaderboard`)
- Interactive tournament rankings
- Player statistics visualization
- Win rate progress bars
- Kill/death ratio charts
- Top 3 podium display

### 🔧 API Endpoints
- `/api/status` - Bot health check
- `/keep_alive` - Keep-alive for monitoring services

## 🔧 Development Setup (Local)

### Prerequisites
```bash
# Python 3.11 or higher
python --version

# Install dependencies  
pip install -r requirements.txt
```

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your values
DISCORD_TOKEN=your_discord_bot_token
SESSION_SECRET=your_random_secret_key
```

### Run Locally
```bash
# Start the application
python main.py

# Bot will start on Discord
# Web dashboard available at http://localhost:5000
```

## 📊 Database Schema

### Players Table
```sql
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    discord_id TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0, 
    draws INTEGER DEFAULT 0,
    kills INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    registered_at TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

### Matches Table
```sql
CREATE TABLE matches (
    id INTEGER PRIMARY KEY,
    player1_id INTEGER,
    player2_id INTEGER, 
    scheduled_time TIMESTAMP,
    status TEXT DEFAULT 'scheduled',
    winner_id INTEGER,
    player1_kills INTEGER DEFAULT 0,
    player2_kills INTEGER DEFAULT 0,
    reminder_sent BOOLEAN DEFAULT 0,
    FOREIGN KEY (player1_id) REFERENCES players (id),
    FOREIGN KEY (player2_id) REFERENCES players (id)
);
```

## 🌍 Multi-Language Support

### Supported Languages
- 🇺🇸 **English** (Default)
- 🇧🇷 **Portuguese** (Português)

### Adding New Languages
1. Edit `translations.py`
2. Add new language code and translations
3. Update `get_user_language()` function for language detection

### Example Translation Entry
```python
TRANSLATIONS = {
    'en': {
        'server_info_title': '🏟️ BombSquad Server Information',
        'match_scheduled': '⚔️ Match Scheduled'
    },
    'pt': {
        'server_info_title': '🏟️ Informações do Servidor BombSquad', 
        'match_scheduled': '⚔️ Partida Agendada'
    }
}
```

## 🚨 Troubleshooting

### Common Issues & Solutions

#### Bot Not Responding
```bash
# Check logs in Render dashboard
# Verify DISCORD_TOKEN is correct
# Ensure bot has permissions in Discord server
```

#### Database Issues
```bash
# Check file permissions
# Verify SQLite database creation
# Review logs for database errors
```

#### Website Not Loading
```bash
# Check Render service status
# Verify environment variables
# Review Flask application logs
```

#### Match Reminders Not Working
```bash
# Check scheduler logs
# Verify user DM permissions
# Ensure correct timezone settings
```

### Getting Help
1. Check Render service logs
2. Verify all environment variables are set
3. Test Discord bot permissions
4. Review error messages in logs

## 🔄 Maintenance & Updates

### Automatic Updates (Render)
- Enable auto-deploy for automatic updates from GitHub
- Bot will restart automatically with new changes
- Database and user data preserved across updates

### Manual Updates
```bash
# Pull latest changes
git pull origin main

# Update dependencies if changed
pip install -r requirements.txt

# Restart application
# (Render will handle this automatically)
```

### Database Migrations
- SQLite automatically handles schema creation
- No manual migration needed for most updates
- Backup database before major updates

## 📈 Performance & Monitoring

### Built-in Monitoring
- Bot status API endpoint
- Keep-alive system for uptime monitoring
- Performance logging in browser console
- Automatic error reporting in logs

### Render Monitoring
- Service health checks
- Resource usage monitoring
- Automatic restart on crashes
- Log retention for debugging

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Make changes and test locally
4. Submit pull request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Test all Discord commands
- Verify web dashboard functionality

## 📄 License & Credits

### Open Source
This project is open source and available under the MIT License.

### Technologies Used
- **Discord.py** - Discord bot framework
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **APScheduler** - Task scheduling
- **Bootstrap 5** - UI framework
- **Chart.js** - Data visualization
- **Font Awesome** - Icons

### BombSquad Integration
- **Server**: `18.228.228.44:3827`
- **Game**: BombSquad by Eric Froemling
- **Tournament Format**: Custom competitive setup

---

<div align="center">

**👑 Built for Champions - Ready for Battle! 👑**

Made with ❤️ for the BombSquad community

[Report Issues](../../issues) | [Feature Requests](../../discussions) | [Discord Support](https://discord.gg/your-support-server)

</div>
