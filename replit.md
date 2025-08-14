# Duel Lords - Discord Tournament Bot

## Overview

Duel Lords is a comprehensive Discord bot designed for managing BombSquad tournaments. The system combines a Discord bot with a Flask web dashboard to provide tournament management capabilities including player registration, match scheduling, statistics tracking, and automated reminders. The bot supports multi-language functionality (English and Portuguese) and features a live web leaderboard with interactive statistics visualization.

## User Preferences

Preferred communication style: Simple, everyday language (Arabic/English).
Language support: Arabic user interface with English and Portuguese bot languages.
Focus on comprehensive tournament management with beautiful visual design.

## System Architecture

### Hybrid Application Structure
The application uses a dual-server architecture running both Discord bot and web server concurrently through threading. The main.py orchestrates both services, with the Flask server running in a daemon thread while the Discord bot operates in the main thread for proper event handling.

### Database Design
- **ORM Choice**: Uses both SQLAlchemy (Flask) and raw SQLite (Discord bot) for data persistence
- **Schema**: Implements Player and Match models with relationship mapping
- **Data Storage**: SQLite database for simplicity and portability
- **Statistics Tracking**: Comprehensive player metrics including wins, losses, draws, kills, deaths, and calculated ratios

### Discord Bot Architecture
- **Command System**: Modern slash command implementation using discord.py
- **Permission Management**: Admin-only player registration with role-based access control
- **Scheduling System**: AsyncIO scheduler for match reminders and automated tasks
- **Multi-language Support**: Translation system with English and Portuguese localization

### Web Dashboard Architecture
- **Framework**: Flask with Jinja2 templating
- **Frontend**: Bootstrap 5 with custom CSS for Discord-inspired dark theme
- **Real-time Features**: Live leaderboard updates and bot status monitoring
- **Responsive Design**: Mobile-friendly interface with interactive charts

### Match Management System
- **Scheduling**: DateTime-based match scheduling with timezone support
- **Reminders**: Automated 5-minute pre-match notifications via Discord DMs
- **State Management**: Match status tracking from scheduled to completed
- **Statistics Calculation**: Automatic player stat updates upon match completion

### External Integration Points
- **BombSquad Server**: Direct server information display (IP: 18.228.228.44, Port: 3827)
- **Discord API**: Full integration with Discord's slash command and embed systems
- **Deployment Ready**: Configured for Render.com deployment with proxy handling

### Error Handling and Logging
- **Comprehensive Logging**: Debug-level logging across all components
- **Database Transactions**: Context managers for safe database operations
- **Graceful Degradation**: Fallback mechanisms for external service failures

## External Dependencies

### Core Framework Dependencies
- **Discord.py**: Modern Discord bot framework with slash command support
- **Flask**: Lightweight web framework for dashboard functionality  
- **SQLAlchemy**: ORM for database modeling and relationships
- **APScheduler**: Asynchronous task scheduling for match reminders

### Frontend Dependencies
- **Bootstrap 5**: Responsive CSS framework for modern UI components
- **Font Awesome 6**: Icon library for consistent visual elements
- **Chart.js**: Interactive charting library for statistics visualization

### Database
- **SQLite**: Embedded database for data persistence and portability

### Deployment Infrastructure
- **Render.com**: Cloud platform for hosting both bot and web services
- **ProxyFix**: Werkzeug middleware for proper proxy header handling

### Discord Integration
- **Discord Developer Portal**: Bot token management and application configuration
- **Discord Gateway**: Real-time event handling and message processing
- **Discord Slash Commands**: Modern command interface with type validation

### Game Server Integration  
- **BombSquad Server**: Direct connection information for tournament matches
- **Custom Server Configuration**: Predefined server details for consistent gameplay