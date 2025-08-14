import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timedelta
import asyncio
import logging
from database import DatabaseManager
from scheduler import SchedulerManager
from translations import get_text
from utils import create_embed, parse_time, format_datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

class DuelLordsBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.db = DatabaseManager()
        self.scheduler = SchedulerManager(self)
        
    async def setup_hook(self):
        """Called when the bot is starting up"""
        logger.info("Setting up Duel Lords bot...")
        await self.scheduler.start()
        
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'{self.user} has logged in!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")

bot = DuelLordsBot()

@bot.tree.command(name="server_info", description="Show BombSquad server information")
async def server_info(interaction: discord.Interaction):
    """Display server IP and port information"""
    embed = create_embed(
        title="🏟️ BombSquad Server Information",
        description="Connect to our official tournament server!",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🌐 Server IP", 
        value="`18.228.228.44`", 
        inline=True
    )
    embed.add_field(
        name="🔌 Port", 
        value="`3827`", 
        inline=True
    )
    embed.add_field(
        name="🎮 Game", 
        value="BombSquad", 
        inline=True
    )
    
    embed.set_footer(text="Copy the IP and port to connect!")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="register_player", description="Register a new player (Admin only)")
@app_commands.describe(player="The player to register")
async def register_player(interaction: discord.Interaction, player: discord.Member):
    """Register a new player for the tournament"""
    # Check if user has admin permissions
    if not hasattr(interaction.user, 'guild_permissions') or not interaction.user.guild_permissions.administrator:
        embed = create_embed(
            title="❌ Access Denied",
            description="Only administrators can register players.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    success, message = bot.db.register_player(str(player.id), player.display_name)
    
    if success:
        embed = create_embed(
            title="✅ Player Registered",
            description=f"{player.mention} has been successfully registered for the tournament!",
            color=discord.Color.green()
        )
        embed.add_field(name="Player", value=player.display_name, inline=True)
        embed.add_field(name="Discord ID", value=str(player.id), inline=True)
        embed.set_thumbnail(url=player.display_avatar.url)
    else:
        embed = create_embed(
            title="❌ Registration Failed",
            description=message,
            color=discord.Color.red()
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="remove_player", description="Remove a player from tournament (Admin only)")
@app_commands.describe(player="The player to remove")
async def remove_player(interaction: discord.Interaction, player: discord.Member):
    """Remove a player from the tournament"""
    if not hasattr(interaction.user, 'guild_permissions') or not interaction.user.guild_permissions.administrator:
        embed = create_embed(
            title="❌ Access Denied",
            description="Only administrators can remove players.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    success, message = bot.db.remove_player(str(player.id))
    
    if success:
        embed = create_embed(
            title="✅ Player Removed",
            description=f"{player.mention} has been removed from the tournament.",
            color=discord.Color.orange()
        )
    else:
        embed = create_embed(
            title="❌ Removal Failed",
            description=message,
            color=discord.Color.red()
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="schedule_match", description="Schedule a match between two players")
@app_commands.describe(
    player1="First player",
    player2="Second player", 
    day="Day (DD)",
    hour="Hour (HH)",
    minute="Minute (MM)"
)
async def schedule_match(
    interaction: discord.Interaction, 
    player1: discord.Member, 
    player2: discord.Member,
    day: int,
    hour: int,
    minute: int
):
    """Schedule a match between two players"""
    try:
        # Create datetime object
        now = datetime.now()
        match_time = datetime(now.year, now.month, day, hour, minute)
        
        # If the date has passed this month, schedule for next month
        if match_time < now:
            if now.month == 12:
                match_time = match_time.replace(year=now.year + 1, month=1)
            else:
                match_time = match_time.replace(month=now.month + 1)
        
        success, message = bot.db.schedule_match(
            str(player1.id), 
            str(player2.id), 
            match_time
        )
        
        if success:
            # Create beautiful match embed
            embed = create_embed(
                title="⚔️ Match Scheduled",
                description="A new duel has been arranged!",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="🥊 Fighters", 
                value=f"{player1.mention} **VS** {player2.mention}", 
                inline=False
            )
            
            discord_timestamp = f"<t:{int(match_time.timestamp())}:F>"
            embed.add_field(
                name="📅 Match Time", 
                value=discord_timestamp, 
                inline=False
            )
            
            embed.add_field(
                name="⏰ Countdown", 
                value=f"<t:{int(match_time.timestamp())}:R>", 
                inline=True
            )
            
            embed.set_footer(text="Players will receive a reminder 5 minutes before the match")
            
            # Schedule reminder
            await bot.scheduler.schedule_reminder(
                player1.id, player2.id, match_time, interaction.guild_id
            )
            
            # Send DMs to both players
            try:
                dm_embed = create_embed(
                    title="🔥 You Have a Scheduled Match!",
                    description=f"Your duel against **{player2.display_name if player1.id == player1.id else player1.display_name}** has been scheduled!",
                    color=discord.Color.blue()
                )
                dm_embed.add_field(name="📅 Date & Time", value=discord_timestamp, inline=False)
                dm_embed.add_field(name="🎯 Server", value="IP: `18.228.228.44:3827`", inline=False)
                
                await player1.send(embed=dm_embed)
                await player2.send(embed=dm_embed)
            except discord.Forbidden:
                embed.add_field(name="⚠️ Note", value="Could not send DM to one or both players", inline=False)
                
        else:
            embed = create_embed(
                title="❌ Scheduling Failed",
                description=message,
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)
        
    except ValueError as e:
        embed = create_embed(
            title="❌ Invalid Date/Time",
            description="Please provide valid day, hour, and minute values.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="player_stats", description="Show detailed player statistics")
@app_commands.describe(player="The player to show stats for (optional)")
async def player_stats(interaction: discord.Interaction, player: discord.Member = None):
    """Display detailed player statistics"""
    target_player = player or interaction.user
    
    player_data = bot.db.get_player(str(target_player.id))
    
    if not player_data:
        embed = create_embed(
            title="❌ Player Not Found",
            description=f"{target_player.mention} is not registered for the tournament.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    # Create beautiful stats embed
    embed = create_embed(
        title=f"📊 Tournament Statistics",
        description=f"**{target_player.display_name}**",
        color=discord.Color.purple()
    )
    
    embed.set_thumbnail(url=target_player.display_avatar.url)
    
    # Match Statistics
    embed.add_field(
        name="🏆 Match Record", 
        value=f"**{player_data['wins']}**W - **{player_data['losses']}**L - **{player_data['draws']}**D", 
        inline=True
    )
    
    # Win Rate
    total_matches = player_data['wins'] + player_data['losses'] + player_data['draws']
    win_rate = (player_data['wins'] / total_matches * 100) if total_matches > 0 else 0
    embed.add_field(
        name="📈 Win Rate", 
        value=f"**{win_rate:.1f}%**", 
        inline=True
    )
    
    # Kill/Death Stats
    kd_ratio = player_data['kills'] / max(player_data['deaths'], 1)
    embed.add_field(
        name="⚔️ K/D Ratio", 
        value=f"**{kd_ratio:.2f}**", 
        inline=True
    )
    
    embed.add_field(
        name="🎯 Total Kills", 
        value=f"**{player_data['kills']}**", 
        inline=True
    )
    
    embed.add_field(
        name="💀 Total Deaths", 
        value=f"**{player_data['deaths']}**", 
        inline=True
    )
    
    embed.add_field(
        name="🎮 Total Matches", 
        value=f"**{total_matches}**", 
        inline=True
    )
    
    embed.set_footer(text=f"Registered: {player_data['registered_at']}")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="leaderboard", description="Show tournament leaderboard")
async def leaderboard(interaction: discord.Interaction):
    """Display tournament leaderboard"""
    players = bot.db.get_leaderboard()
    
    if not players:
        embed = create_embed(
            title="📊 Tournament Leaderboard",
            description="No players registered yet!",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    embed = create_embed(
        title="🏆 Tournament Leaderboard",
        description="Top fighters in the Duel Lords tournament",
        color=discord.Color.gold()
    )
    
    leaderboard_text = ""
    medals = ["🥇", "🥈", "🥉"]
    
    for i, player in enumerate(players[:10]):  # Top 10 players
        medal = medals[i] if i < 3 else f"#{i+1}"
        total_matches = player['wins'] + player['losses'] + player['draws']
        win_rate = (player['wins'] / total_matches * 100) if total_matches > 0 else 0
        
        leaderboard_text += f"{medal} **{player['username']}**\n"
        leaderboard_text += f"   🏆 {player['wins']}W-{player['losses']}L-{player['draws']}D ({win_rate:.1f}%)\n"
        leaderboard_text += f"   ⚔️ {player['kills']} kills | 💀 {player['deaths']} deaths\n\n"
    
    embed.description = leaderboard_text
    embed.set_footer(text="Fight your way to the top!")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="update_stats", description="Update player match statistics (Admin only)")
@app_commands.describe(
    player="Player to update",
    wins="Number of wins to add",
    losses="Number of losses to add", 
    draws="Number of draws to add",
    kills="Number of kills to add",
    deaths="Number of deaths to add"
)
async def update_stats(
    interaction: discord.Interaction,
    player: discord.Member,
    wins: int = 0,
    losses: int = 0,
    draws: int = 0,
    kills: int = 0,
    deaths: int = 0
):
    """Update player statistics"""
    if not hasattr(interaction.user, 'guild_permissions') or not interaction.user.guild_permissions.administrator:
        embed = create_embed(
            title="❌ Access Denied",
            description="Only administrators can update player statistics.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    success, message = bot.db.update_player_stats(
        str(player.id), wins, losses, draws, kills, deaths
    )
    
    if success:
        embed = create_embed(
            title="✅ Statistics Updated",
            description=f"Updated statistics for {player.mention}",
            color=discord.Color.green()
        )
        
        if wins > 0:
            embed.add_field(name="🏆 Wins", value=f"+{wins}", inline=True)
        if losses > 0:
            embed.add_field(name="💔 Losses", value=f"+{losses}", inline=True)
        if draws > 0:
            embed.add_field(name="🤝 Draws", value=f"+{draws}", inline=True)
        if kills > 0:
            embed.add_field(name="⚔️ Kills", value=f"+{kills}", inline=True)
        if deaths > 0:
            embed.add_field(name="💀 Deaths", value=f"+{deaths}", inline=True)
            
    else:
        embed = create_embed(
            title="❌ Update Failed",
            description=message,
            color=discord.Color.red()
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="all_players", description="Show all registered tournament players")
async def all_players(interaction: discord.Interaction):
    """Display all registered players"""
    players = bot.db.get_all_players()
    
    if not players:
        embed = create_embed(
            title="👥 Tournament Players",
            description="No players registered yet!",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    embed = create_embed(
        title="👥 All Tournament Players",
        description=f"**{len(players)} fighters** registered for combat!",
        color=discord.Color.blue()
    )
    
    players_text = ""
    for i, player in enumerate(players, 1):
        total_matches = player['wins'] + player['losses'] + player['draws']
        players_text += f"**{i}.** {player['username']} "
        players_text += f"({player['wins']}W-{player['losses']}L-{player['draws']}D)\n"
    
    # Split into multiple fields if too long
    if len(players_text) > 1024:
        mid = len(players) // 2
        embed.add_field(
            name="🥊 Fighters (1st Half)", 
            value="\n".join(players_text.split("\n")[:mid]), 
            inline=True
        )
        embed.add_field(
            name="🥊 Fighters (2nd Half)", 
            value="\n".join(players_text.split("\n")[mid:]), 
            inline=True
        )
    else:
        embed.add_field(name="🥊 All Fighters", value=players_text, inline=False)
    
    embed.set_footer(text="Ready for battle!")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    """Display help information"""
    embed = create_embed(
        title="🤖 Duel Lords Bot Commands",
        description="Complete list of available commands for tournament management",
        color=discord.Color.blue()
    )
    
    # General Commands
    embed.add_field(
        name="🎮 General Commands",
        value="`/server_info` - Show BombSquad server details\n"
              "`/help` - Show this help message\n"
              "`/player_stats` - View player statistics\n"
              "`/leaderboard` - Tournament rankings\n"
              "`/all_players` - List all registered players",
        inline=False
    )
    
    # Admin Commands  
    embed.add_field(
        name="👑 Admin Commands",
        value="`/register_player` - Register new player\n"
              "`/remove_player` - Remove player from tournament\n"
              "`/schedule_match` - Schedule player vs player match\n"
              "`/update_stats` - Update player win/loss/kill stats",
        inline=False
    )
    
    # Match Features
    embed.add_field(
        name="⚔️ Match Features",
        value="• Automatic reminders 5 minutes before matches\n"
              "• Private DM notifications to players\n"  
              "• Discord timestamp integration\n"
              "• Beautiful embed styling",
        inline=False
    )
    
    embed.set_footer(text="Duel Lords - BombSquad Tournament Management")
    
    await interaction.response.send_message(embed=embed)

def run_bot():
    """Start the Discord bot"""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        print("ERROR: DISCORD_TOKEN not found! Please add your Discord bot token to the secrets.")
        return
    
    logger.info("Starting Duel Lords Discord Bot...")
    print("Starting Duel Lords Discord Bot...")
    
    try:
        bot.run(token, log_handler=None, log_level=logging.INFO)
    except discord.LoginFailure:
        logger.error("Failed to login to Discord - Invalid token!")
        print("ERROR: Invalid Discord token! Please check your DISCORD_TOKEN in secrets.")
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")
        print(f"ERROR: Bot failed to start: {e}")

if __name__ == "__main__":
    run_bot()
