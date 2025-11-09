/**
 * Dashboard JavaScript
 * Handles rendering of games on the main dashboard
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', async function() {
  try {
    // Load data
    await nflData.loadData();
    
    // Update summary stats
    updateSummaryStats();
    
    // Render games
    renderGames();
    
    // Update header info
    updateHeaderInfo();
    
  } catch (error) {
    console.error('Error initializing dashboard:', error);
    showError('Failed to load NFL data. Please refresh the page.');
  }
});

/**
 * Update summary statistics cards
 */
function updateSummaryStats() {
  const stats = nflData.getSummaryStats();
  
  document.getElementById('total-games').textContent = stats.totalGames;
  document.getElementById('weather-alerts').textContent = stats.weatherAlerts;
  document.getElementById('avg-over-under').textContent = stats.avgOverUnder;
  document.getElementById('week-number').textContent = stats.week;
  
  // Count DFS players
  const dfsCount = nflData.getAllDFSPlayers().length;
  document.getElementById('dfs-count').textContent = dfsCount;
}

/**
 * Update header information
 */
function updateHeaderInfo() {
  const asOfDate = new Date(nflData.data.as_of_date_et);
  const formattedDate = asOfDate.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  });
  document.getElementById('as-of-date').textContent = formattedDate;
}

/**
 * Render all games
 */
function renderGames() {
  const games = nflData.getAllGames();
  const container = document.getElementById('games-container');
  
  if (games.length === 0) {
    container.innerHTML = '<div class="col-12 text-center py-5"><p>No games available</p></div>';
    return;
  }
  
  // Clear loading spinner
  container.innerHTML = '';
  
  // Render each game
  games.forEach(game => {
    const gameCard = createGameCard(game);
    container.appendChild(gameCard);
  });
}

/**
 * Create a game card element
 */
function createGameCard(game) {
  const col = document.createElement('div');
  col.className = 'col-lg-4 col-md-6 mb-6';
  
  const teams = nflData.getTeamsFromGameId(game.game_id);
  const kickoffTime = nflData.formatKickoffTime(game.kickoff_et);
  const weatherImpact = nflData.getWeatherImpact(game.weather);
  const weatherIcon = nflData.getWeatherIcon(game.weather?.conditions);
  const overPercentage = nflData.calculateOverPercentage(game.over_under_trends);
  
  // Extract spread and total
  const spread = game.vegas?.spread || 'N/A';
  const total = game.vegas?.total || 'N/A';
  const awayImplied = game.vegas?.implied_totals?.away || 0;
  const homeImplied = game.vegas?.implied_totals?.home || 0;
  
  // Weather badge
  let weatherBadge = '';
  if (weatherImpact === 'high') {
    weatherBadge = '<span class="badge bg-label-danger ms-2"><i class="bx bx-error-circle"></i> High Impact</span>';
  } else if (weatherImpact === 'medium') {
    weatherBadge = '<span class="badge bg-label-warning ms-2"><i class="bx bx-error"></i> Medium Impact</span>';
  }
  
  col.innerHTML = `
    <div class="card h-100">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-start mb-3">
          <div>
            <h5 class="card-title mb-1">
              <span class="badge bg-label-primary">${teams.away}</span>
              <span class="mx-2">@</span>
              <span class="badge bg-label-success">${teams.home}</span>
            </h5>
            <small class="text-body-secondary">
              <i class="bx bx-time-five"></i> ${kickoffTime}
            </small>
          </div>
          <div class="dropdown">
            <button class="btn p-0" type="button" data-bs-toggle="dropdown">
              <i class="bx bx-dots-vertical-rounded"></i>
            </button>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="pages/game-details.html?game=${encodeURIComponent(game.game_id)}">View Details</a></li>
            </ul>
          </div>
        </div>
        
        <!-- Vegas Lines -->
        <div class="mb-3">
          <div class="d-flex justify-content-between mb-2">
            <span class="text-body-secondary">Spread:</span>
            <strong>${spread}</strong>
          </div>
          <div class="d-flex justify-content-between mb-2">
            <span class="text-body-secondary">Total:</span>
            <strong>${total}</strong>
          </div>
          <div class="d-flex justify-content-between">
            <span class="text-body-secondary">Implied:</span>
            <span class="badge bg-label-info">${awayImplied} - ${homeImplied}</span>
          </div>
        </div>
        
        <!-- Weather Info -->
        <div class="mb-3 p-2 bg-label-secondary rounded">
          <div class="d-flex align-items-center">
            <i class="bx ${weatherIcon} icon-lg me-2"></i>
            <div class="flex-grow-1">
              <small class="d-block">${game.weather?.conditions || 'N/A'}</small>
              <small class="text-body-secondary">${game.weather?.temp_f || 'N/A'}°F, Wind: ${game.weather?.wind_mph_sustained || 0} mph</small>
            </div>
            ${weatherBadge}
          </div>
        </div>
        
        <!-- Over/Under Trend -->
        <div class="mb-3">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <small class="text-body-secondary">O/U Trend (L5):</small>
            <span class="badge ${overPercentage >= 60 ? 'bg-label-success' : overPercentage >= 40 ? 'bg-label-warning' : 'bg-label-danger'}">
              ${overPercentage}% Over
            </span>
          </div>
          <div class="progress" style="height: 6px;">
            <div class="progress-bar ${overPercentage >= 60 ? 'bg-success' : overPercentage >= 40 ? 'bg-warning' : 'bg-danger'}" 
                 style="width: ${overPercentage}%"></div>
          </div>
        </div>
        
        <!-- Venue Info -->
        <div class="d-flex justify-content-between align-items-center">
          <small class="text-body-secondary">
            <i class="bx bx-map"></i> ${game.venue}
          </small>
          <small class="text-body-secondary">
            ${game.is_dome ? '<i class="bx bx-home"></i> Dome' : '<i class="bx bx-sun"></i> Outdoor'}
          </small>
        </div>
        
        <!-- Injuries Badge -->
        ${game.injuries && game.injuries.length > 0 ? `
          <div class="mt-3">
            <span class="badge bg-label-warning">
              <i class="bx bx-first-aid"></i> ${game.injuries.length} Injury Report${game.injuries.length > 1 ? 's' : ''}
            </span>
          </div>
        ` : ''}
        
        <!-- Action Button -->
        <div class="mt-3">
          <a href="pages/game-details.html?game=${encodeURIComponent(game.game_id)}" 
             class="btn btn-sm btn-outline-primary w-100">
            View Full Analysis
          </a>
        </div>
      </div>
    </div>
  `;
  
  return col;
}

/**
 * Show error message
 */
function showError(message) {
  const container = document.getElementById('games-container');
  container.innerHTML = `
    <div class="col-12">
      <div class="alert alert-danger" role="alert">
        <h6 class="alert-heading mb-1">Error Loading Data</h6>
        <p class="mb-0">${message}</p>
      </div>
    </div>
  `;
}