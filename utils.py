import discord
from datetime import datetime
import re

def create_embed(title: str, description: str = "", color: discord.Color = discord.Color.blue()) -> discord.Embed:
    """Create a beautiful embed with consistent styling"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.utcnow()
    )
    
    # Add Duel Lords branding
    embed.set_author(
        name="Duel Lords Tournament",
        icon_url="https://cdn.discordapp.com/attachments/placeholder/duel_lords_icon.png"
    )
    
    return embed

def parse_time(time_str: str) -> datetime:
    """Parse time string in various formats"""
    # This is a placeholder - implement time parsing logic
    # Examples: "2023-12-25 15:30", "25/12 15:30", etc.
    pass

def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime("%Y-%m-%d %H:%M UTC")

def calculate_win_rate(wins: int, losses: int, draws: int) -> float:
    """Calculate win rate percentage"""
    total_matches = wins + losses + draws
    if total_matches == 0:
        return 0.0
    return round((wins / total_matches) * 100, 2)

def calculate_kd_ratio(kills: int, deaths: int) -> float:
    """Calculate kill/death ratio"""
    if deaths == 0:
        return float(kills) if kills > 0 else 0.0
    return round(kills / deaths, 2)

def format_match_record(wins: int, losses: int, draws: int) -> str:
    """Format match record as W-L-D"""
    return f"{wins}W-{losses}L-{draws}D"

def validate_discord_id(discord_id: str) -> bool:
    """Validate Discord ID format"""
    return discord_id.isdigit() and len(discord_id) >= 15 and len(discord_id) <= 21

def sanitize_username(username: str) -> str:
    """Sanitize username for database storage"""
    # Remove any potentially harmful characters
    return re.sub(r'[^\w\s\-_.]', '', username)[:100]

def get_rank_emoji(position: int) -> str:
    """Get appropriate emoji for leaderboard position"""
    if position == 1:
        return "🥇"
    elif position == 2:
        return "🥈" 
    elif position == 3:
        return "🥉"
    else:
        return f"#{position}"

def format_time_until(target_time: datetime) -> str:
    """Format time remaining until target time"""
    now = datetime.utcnow()
    if target_time <= now:
        return "Started"
    
    delta = target_time - now
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def create_progress_bar(current: int, total: int, length: int = 10) -> str:
    """Create a text-based progress bar"""
    if total == 0:
        return "░" * length
    
    filled = int((current / total) * length)
    bar = "█" * filled + "░" * (length - filled)
    return f"{bar} {current}/{total}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def is_valid_date_time(day: int, hour: int, minute: int) -> bool:
    """Validate date/time input"""
    return (1 <= day <= 31 and 
            0 <= hour <= 23 and 
            0 <= minute <= 59)

def get_server_info() -> dict:
    """Get BombSquad server information"""
    return {
        'ip': '18.228.228.44',
        'port': '3827',
        'game': 'BombSquad'
    }
