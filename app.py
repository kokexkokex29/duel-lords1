import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///duel_lords.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

@app.route('/')
def index():
    """Homepage showing leaderboard and players"""
    from models import Player
    
    with app.app_context():
        # Get top players by wins
        top_players = Player.query.order_by(
            Player.wins.desc(), 
            Player.kills.desc()
        ).limit(10).all()
        
        # Get total player count
        total_players = Player.query.count()
        
        return render_template('index.html', players=top_players, total_players=total_players)

@app.route('/leaderboard')
def leaderboard():
    """Leaderboard page"""
    from models import Player
    
    with app.app_context():
        # Get top players by wins
        top_players = Player.query.order_by(
            Player.wins.desc(), 
            Player.kills.desc()
        ).limit(20).all()
        
        return render_template('leaderboard.html', players=top_players)

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    return jsonify({
        'status': 'online',
        'bot': 'Duel Lords',
        'message': 'Bot is running successfully!'
    })

@app.route('/keep_alive')
def keep_alive():
    """Keep-alive endpoint for monitoring services"""
    return jsonify({'status': 'alive', 'message': 'Duel Lords bot is running!'})

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
