from app import db
from datetime import datetime
from sqlalchemy import func

class Player(db.Model):
    """Player model for storing tournament participant data"""
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    kills = db.Column(db.Integer, default=0)
    deaths = db.Column(db.Integer, default=0)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with matches
    matches_as_player1 = db.relationship('Match', foreign_keys='Match.player1_id', backref='player1_obj')
    matches_as_player2 = db.relationship('Match', foreign_keys='Match.player2_id', backref='player2_obj')
    
    def __repr__(self):
        return f'<Player {self.username}>'
    
    @property
    def total_matches(self):
        """Calculate total matches played"""
        return self.wins + self.losses + self.draws
    
    @property
    def win_rate(self):
        """Calculate win rate percentage"""
        if self.total_matches == 0:
            return 0
        return round((self.wins / self.total_matches) * 100, 2)
    
    @property
    def kd_ratio(self):
        """Calculate kill/death ratio"""
        if self.deaths == 0:
            return float(self.kills) if self.kills > 0 else 0
        return round(self.kills / self.deaths, 2)

class Match(db.Model):
    """Match model for storing scheduled and completed matches"""
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    player1_kills = db.Column(db.Integer, default=0)
    player2_kills = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    reminder_sent = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Match {self.id}: {self.player1_obj.username} vs {self.player2_obj.username}>'

class Tournament(db.Model):
    """Tournament model for organizing multiple matches"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, active, completed
    max_players = db.Column(db.Integer, default=16)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tournament {self.name}>'
