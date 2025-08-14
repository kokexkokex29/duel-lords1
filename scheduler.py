import asyncio
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from utils import create_embed
import discord

logger = logging.getLogger(__name__)

class SchedulerManager:
    """Manages scheduled tasks like match reminders"""
    
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        
    async def start(self):
        """Start the scheduler"""
        self.scheduler.start()
        logger.info("Scheduler started successfully")
        
        # Schedule existing matches that need reminders
        await self.schedule_existing_reminders()
    
    async def schedule_existing_reminders(self):
        """Schedule reminders for existing matches"""
        try:
            upcoming_matches = self.bot.db.get_upcoming_matches()
            
            for match in upcoming_matches:
                if not match['reminder_sent']:
                    match_time = datetime.fromisoformat(match['scheduled_time'])
                    reminder_time = match_time - timedelta(minutes=5)
                    
                    if reminder_time > datetime.now():
                        await self.schedule_reminder(
                            int(match['player1_discord_id']),
                            int(match['player2_discord_id']),
                            match_time,
                            None,  # guild_id not needed for existing matches
                            match['id']
                        )
                        
        except Exception as e:
            logger.error(f"Error scheduling existing reminders: {e}")
    
    async def schedule_reminder(self, player1_id: int, player2_id: int, match_time: datetime, 
                              guild_id: int = None, match_id: int = None):
        """Schedule a match reminder"""
        try:
            reminder_time = match_time - timedelta(minutes=5)
            
            # Only schedule if reminder time is in the future
            if reminder_time <= datetime.now():
                logger.warning("Reminder time is in the past, skipping")
                return
            
            self.scheduler.add_job(
                self.send_match_reminder,
                DateTrigger(run_date=reminder_time),
                args=[player1_id, player2_id, match_time, match_id],
                id=f"reminder_{player1_id}_{player2_id}_{int(match_time.timestamp())}",
                replace_existing=True
            )
            
            logger.info(f"Scheduled reminder for {reminder_time}")
            
        except Exception as e:
            logger.error(f"Error scheduling reminder: {e}")
    
    async def send_match_reminder(self, player1_id: int, player2_id: int, 
                                match_time: datetime, match_id: int = None):
        """Send match reminder to both players"""
        try:
            # Get user objects
            player1 = self.bot.get_user(player1_id)
            player2 = self.bot.get_user(player2_id)
            
            if not player1 or not player2:
                logger.error("Could not find one or both players for reminder")
                return
            
            # Create beautiful reminder embed
            embed = create_embed(
                title="⏰ Match Reminder",
                description="**Your duel starts in 5 minutes!**",
                color=discord.Color.red()
            )
            
            # Player 1 embed
            player1_embed = embed.copy()
            player1_embed.add_field(
                name="🥊 Your Opponent", 
                value=f"**{player2.display_name}**", 
                inline=True
            )
            player1_embed.add_field(
                name="📅 Match Time", 
                value=f"<t:{int(match_time.timestamp())}:F>", 
                inline=True
            )
            player1_embed.add_field(
                name="🎯 Server", 
                value="IP: `18.228.228.44:3827`", 
                inline=False
            )
            player1_embed.add_field(
                name="⚡ Get Ready!", 
                value="Join the server and prepare for battle!", 
                inline=False
            )
            player1_embed.set_footer(text="Good luck, warrior!")
            
            # Player 2 embed  
            player2_embed = embed.copy()
            player2_embed.add_field(
                name="🥊 Your Opponent", 
                value=f"**{player1.display_name}**", 
                inline=True
            )
            player2_embed.add_field(
                name="📅 Match Time", 
                value=f"<t:{int(match_time.timestamp())}:F>", 
                inline=True
            )
            player2_embed.add_field(
                name="🎯 Server", 
                value="IP: `18.228.228.44:3827`", 
                inline=False
            )
            player2_embed.add_field(
                name="⚡ Get Ready!", 
                value="Join the server and prepare for battle!", 
                inline=False
            )
            player2_embed.set_footer(text="Good luck, warrior!")
            
            # Send DMs
            try:
                await player1.send(embed=player1_embed)
                logger.info(f"Sent reminder to {player1.display_name}")
            except discord.Forbidden:
                logger.warning(f"Could not send DM to {player1.display_name}")
            
            try:
                await player2.send(embed=player2_embed)
                logger.info(f"Sent reminder to {player2.display_name}")
            except discord.Forbidden:
                logger.warning(f"Could not send DM to {player2.display_name}")
            
            # Mark reminder as sent in database
            if match_id:
                self.bot.db.mark_reminder_sent(match_id)
                
        except Exception as e:
            logger.error(f"Error sending match reminder: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
