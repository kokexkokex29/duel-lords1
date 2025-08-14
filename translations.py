"""
Multi-language support for Duel Lords bot
Supports English (default) and Portuguese
"""

TRANSLATIONS = {
    'en': {
        'server_info_title': '🏟️ BombSquad Server Information',
        'server_info_desc': 'Connect to our official tournament server!',
        'server_ip': '🌐 Server IP',
        'server_port': '🔌 Port',
        'game': '🎮 Game',
        'copy_info': 'Copy the IP and port to connect!',
        'access_denied': '❌ Access Denied',
        'admin_only': 'Only administrators can register players.',
        'player_registered': '✅ Player Registered',
        'registration_failed': '❌ Registration Failed',
        'match_scheduled': '⚔️ Match Scheduled',
        'new_duel': 'A new duel has been arranged!',
        'fighters': '🥊 Fighters',
        'match_time': '📅 Match Time',
        'countdown': '⏰ Countdown',
        'reminder_note': 'Players will receive a reminder 5 minutes before the match',
        'stats_title': '📊 Tournament Statistics',
        'match_record': '🏆 Match Record',
        'win_rate': '📈 Win Rate',
        'kd_ratio': '⚔️ K/D Ratio',
        'total_kills': '🎯 Total Kills',
        'total_deaths': '💀 Total Deaths',
        'total_matches': '🎮 Total Matches',
        'leaderboard_title': '🏆 Tournament Leaderboard',
        'top_fighters': 'Top fighters in the Duel Lords tournament',
        'fight_to_top': 'Fight your way to the top!',
        'match_reminder': '⏰ Match Reminder',
        'duel_starts': '**Your duel starts in 5 minutes!**',
        'your_opponent': '🥊 Your Opponent',
        'get_ready': '⚡ Get Ready!',
        'join_server': 'Join the server and prepare for battle!',
        'good_luck': 'Good luck, warrior!'
    },
    'pt': {
        'server_info_title': '🏟️ Informações do Servidor BombSquad',
        'server_info_desc': 'Conecte-se ao nosso servidor oficial do torneio!',
        'server_ip': '🌐 IP do Servidor',
        'server_port': '🔌 Porta',
        'game': '🎮 Jogo',
        'copy_info': 'Copie o IP e a porta para conectar!',
        'access_denied': '❌ Acesso Negado',
        'admin_only': 'Apenas administradores podem registrar jogadores.',
        'player_registered': '✅ Jogador Registrado',
        'registration_failed': '❌ Falha no Registro',
        'match_scheduled': '⚔️ Partida Agendada',
        'new_duel': 'Um novo duelo foi marcado!',
        'fighters': '🥊 Lutadores',
        'match_time': '📅 Horário da Partida',
        'countdown': '⏰ Contagem Regressiva',
        'reminder_note': 'Os jogadores receberão um lembrete 5 minutos antes da partida',
        'stats_title': '📊 Estatísticas do Torneio',
        'match_record': '🏆 Histórico de Partidas',
        'win_rate': '📈 Taxa de Vitória',
        'kd_ratio': '⚔️ Proporção K/D',
        'total_kills': '🎯 Total de Mortes',
        'total_deaths': '💀 Total de Mortes Sofridas',
        'total_matches': '🎮 Total de Partidas',
        'leaderboard_title': '🏆 Classificação do Torneio',
        'top_fighters': 'Melhores lutadores no torneio Duel Lords',
        'fight_to_top': 'Lute para chegar ao topo!',
        'match_reminder': '⏰ Lembrete de Partida',
        'duel_starts': '**Seu duelo começa em 5 minutos!**',
        'your_opponent': '🥊 Seu Oponente',
        'get_ready': '⚡ Prepare-se!',
        'join_server': 'Entre no servidor e prepare-se para a batalha!',
        'good_luck': 'Boa sorte, guerreiro!'
    }
}

def get_text(key: str, lang: str = 'en') -> str:
    """Get translated text for the given key and language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

def get_user_language(user_id: int) -> str:
    """Get user's preferred language (placeholder for future implementation)"""
    # TODO: Implement database storage for user language preferences
    return 'en'  # Default to English for now
