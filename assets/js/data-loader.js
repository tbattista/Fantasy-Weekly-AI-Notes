/**
 * NFL Data Manager
 * Handles loading and parsing of NFL game data
 */
class NFLDataManager {
  constructor() {
    this.data = null;
    this.games = [];
    this.dfsPlayers = {
      qb: [],
      rb: [],
      wr: [],
      te: []
    };
  }

  /**
   * Load data from JSON file
   */
  async loadData() {
    try {
      const response = await fetch('../data/week10-data.json');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      this.data = await response.json();
      this.games = this.data.games || [];
      this.dfsPlayers = this.data.dfs_player_pool || { qb: [], rb: [], wr: [], te: [] };
      return this.data;
    } catch (error) {
      console.error('Error loading NFL data:', error);
      throw error;
    }
  }

  /**
   * Get all games
   */
  getAllGames() {
    return this.games;
  }

  /**
   * Get game by ID
   */
  getGameById(gameId) {
    return this.games.find(game => game.game_id === gameId);
  }

  /**
   * Get games with weather alerts
   */
  getWeatherAlertGames() {
    return this.data?.weather_watch || [];
  }

  /**
   * Get DFS players by position
   */
  getPlayersByPosition(position) {
    return this.dfsPlayers[position.toLowerCase()] || [];
  }

  /**
   * Get all DFS players (flattened)
   */
  getAllDFSPlayers() {
    const allPlayers = [];
    ['qb', 'rb', 'wr', 'te'].forEach(pos => {
      const players = this.dfsPlayers[pos] || [];
      players.forEach(player => {
        allPlayers.push({
          ...player,
          position: pos.toUpperCase()
        });
      });
    });
    return allPlayers;
  }

  /**
   * Get injury report for a specific game
   */
  getInjuriesForGame(gameId) {
    const game = this.getGameById(gameId);
    return game?.injuries || [];
  }

  /**
   * Get over/under trends for a game
   */
  getTrendsForGame(gameId) {
    const game = this.getGameById(gameId);
    return game?.over_under_trends || null;
  }

  /**
   * Format kickoff time
   */
  formatKickoffTime(kickoffString) {
    const date = new Date(kickoffString);
    return date.toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      timeZoneName: 'short'
    });
  }

  /**
   * Get team abbreviation from game ID
   */
  getTeamsFromGameId(gameId) {
    const parts = gameId.split('_')[0].split('@');
    return {
      away: parts[0],
      home: parts[1]
    };
  }

  /**
   * Get weather impact level
   */
  getWeatherImpact(weather) {
    if (!weather) return 'none';
    
    const { precip_chance_pct, wind_mph_sustained, temp_f } = weather;
    
    // High impact conditions
    if (precip_chance_pct > 60 || wind_mph_sustained > 20 || temp_f < 32) {
      return 'high';
    }
    
    // Medium impact conditions
    if (precip_chance_pct > 30 || wind_mph_sustained > 15 || temp_f < 40) {
      return 'medium';
    }
    
    return 'low';
  }

  /**
   * Get weather icon class
   */
  getWeatherIcon(conditions) {
    const conditionsLower = (conditions || '').toLowerCase();
    
    if (conditionsLower.includes('rain')) return 'bx-cloud-rain';
    if (conditionsLower.includes('snow')) return 'bx-cloud-snow';
    if (conditionsLower.includes('thunder')) return 'bx-cloud-lightning';
    if (conditionsLower.includes('cloud')) return 'bx-cloud';
    if (conditionsLower.includes('clear') || conditionsLower.includes('sunny')) return 'bx-sun';
    
    return 'bx-cloud';
  }

  /**
   * Calculate over/under percentage
   */
  calculateOverPercentage(trends) {
    if (!trends) return 0;
    
    const awayOvers = trends.away_team?.summary?.overs || 0;
    const awayTotal = (trends.away_team?.summary?.overs || 0) + 
                      (trends.away_team?.summary?.unders || 0);
    
    const homeOvers = trends.home_team?.summary?.overs || 0;
    const homeTotal = (trends.home_team?.summary?.overs || 0) + 
                      (trends.home_team?.summary?.unders || 0);
    
    const totalOvers = awayOvers + homeOvers;
    const totalGames = awayTotal + homeTotal;
    
    return totalGames > 0 ? Math.round((totalOvers / totalGames) * 100) : 0;
  }

  /**
   * Get risk tag color class
   */
  getRiskTagClass(riskTag) {
    const tagMap = {
      'stud': 'bg-label-success',
      'cash': 'bg-label-primary',
      'gpp': 'bg-label-warning',
      'value': 'bg-label-info',
      'n/a': 'bg-label-secondary'
    };
    return tagMap[riskTag?.toLowerCase()] || 'bg-label-secondary';
  }

  /**
   * Format salary
   */
  formatSalary(salary) {
    if (!salary) return 'N/A';
    return `$${salary.toLocaleString()}`;
  }

  /**
   * Get summary statistics
   */
  getSummaryStats() {
    const totalGames = this.games.length;
    const weatherAlerts = this.getWeatherAlertGames().length;
    
    let totalOverUnder = 0;
    let gamesWithTotal = 0;
    
    this.games.forEach(game => {
      const total = parseFloat(game.vegas?.total?.split(' ')[0]);
      if (!isNaN(total)) {
        totalOverUnder += total;
        gamesWithTotal++;
      }
    });
    
    const avgOverUnder = gamesWithTotal > 0 ? 
      (totalOverUnder / gamesWithTotal).toFixed(1) : 0;
    
    return {
      totalGames,
      weatherAlerts,
      avgOverUnder,
      week: this.data?.week || 0
    };
  }
}

// Create global instance
const nflData = new NFLDataManager();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = NFLDataManager;
}