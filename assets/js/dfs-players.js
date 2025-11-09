/**
 * DFS Players JavaScript
 * Handles rendering and filtering of DFS player data
 */

let currentPosition = 'QB';
let allPlayers = {};

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', async function() {
  try {
    // Load data
    await nflData.loadData();
    
    // Store all players by position
    allPlayers = {
      QB: nflData.getPlayersByPosition('qb'),
      RB: nflData.getPlayersByPosition('rb'),
      WR: nflData.getPlayersByPosition('wr'),
      TE: nflData.getPlayersByPosition('te')
    };
    
    // Render all positions
    renderPlayers('QB');
    renderPlayers('RB');
    renderPlayers('WR');
    renderPlayers('TE');
    
  } catch (error) {
    console.error('Error initializing DFS players page:', error);
    showError('Failed to load player data. Please refresh the page.');
  }
});

/**
 * Render players for a specific position
 */
function renderPlayers(position) {
  const players = allPlayers[position] || [];
  const tbody = document.getElementById(`${position.toLowerCase()}-tbody`);
  
  if (!tbody) return;
  
  if (players.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="text-center py-4">
          <i class="bx bx-info-circle icon-lg text-body-secondary"></i>
          <p class="mb-0 mt-2">No ${position} players available in the pool</p>
        </td>
      </tr>
    `;
    return;
  }
  
  tbody.innerHTML = '';
  
  players.forEach(player => {
    const row = createPlayerRow(player);
    tbody.appendChild(row);
  });
}

/**
 * Create a player table row
 */
function createPlayerRow(player) {
  const tr = document.createElement('tr');
  
  const riskClass = nflData.getRiskTagClass(player.risk_tag);
  const salary = nflData.formatSalary(player.dk_salary);
  
  tr.innerHTML = `
    <td>
      <div class="d-flex flex-column">
        <h6 class="mb-0">${player.name}</h6>
        <small class="text-body-secondary">${player.recent_role_note || 'N/A'}</small>
      </div>
    </td>
    <td>
      <span class="badge bg-label-primary">${player.team}</span>
    </td>
    <td>
      <strong>${salary}</strong>
    </td>
    <td>
      <span class="badge ${riskClass}">${player.risk_tag || 'N/A'}</span>
    </td>
    <td>
      <small class="text-body-secondary">${player.matchup_note || 'N/A'}</small>
    </td>
    <td>
      <div class="d-flex align-items-center">
        <i class="bx bx-trending-up text-success me-1"></i>
        <small>${player.projection_hint || 'N/A'}</small>
      </div>
    </td>
  `;
  
  // Add click handler for row details
  tr.style.cursor = 'pointer';
  tr.addEventListener('click', () => showPlayerDetails(player));
  
  return tr;
}

/**
 * Show player details modal
 */
function showPlayerDetails(player) {
  // Create modal content
  const modalContent = `
    <div class="modal fade" id="playerModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">${player.name} - ${player.team}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6 mb-3">
                <h6>DFS Information</h6>
                <ul class="list-unstyled">
                  <li><strong>Salary:</strong> ${nflData.formatSalary(player.dk_salary)}</li>
                  <li><strong>Risk Tag:</strong> <span class="badge ${nflData.getRiskTagClass(player.risk_tag)}">${player.risk_tag}</span></li>
                </ul>
              </div>
              <div class="col-md-6 mb-3">
                <h6>Projection</h6>
                <p class="text-body-secondary">${player.projection_hint || 'No projection available'}</p>
              </div>
            </div>
            <div class="row">
              <div class="col-12 mb-3">
                <h6>Recent Role</h6>
                <p class="text-body-secondary">${player.recent_role_note || 'No recent role information'}</p>
              </div>
              <div class="col-12">
                <h6>Matchup Analysis</h6>
                <p class="text-body-secondary">${player.matchup_note || 'No matchup analysis available'}</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // Remove existing modal if any
  const existingModal = document.getElementById('playerModal');
  if (existingModal) {
    existingModal.remove();
  }
  
  // Add modal to body
  document.body.insertAdjacentHTML('beforeend', modalContent);
  
  // Show modal
  const modal = new bootstrap.Modal(document.getElementById('playerModal'));
  modal.show();
  
  // Clean up after modal is hidden
  document.getElementById('playerModal').addEventListener('hidden.bs.modal', function() {
    this.remove();
  });
}

/**
 * Switch position tab
 */
function switchPosition(position) {
  currentPosition = position;
}

/**
 * Apply filters
 */
function applyFilters() {
  const positionFilter = document.getElementById('position-filter').value;
  const riskFilter = document.getElementById('risk-filter').value;
  const searchTerm = document.getElementById('player-search').value.toLowerCase();
  
  // Determine which positions to filter
  const positions = positionFilter === 'all' ? ['QB', 'RB', 'WR', 'TE'] : [positionFilter];
  
  positions.forEach(position => {
    let players = allPlayers[position] || [];
    
    // Apply risk filter
    if (riskFilter !== 'all') {
      players = players.filter(p => p.risk_tag?.toLowerCase() === riskFilter.toLowerCase());
    }
    
    // Apply search filter
    if (searchTerm) {
      players = players.filter(p => 
        p.name.toLowerCase().includes(searchTerm) ||
        p.team.toLowerCase().includes(searchTerm)
      );
    }
    
    // Render filtered players
    const tbody = document.getElementById(`${position.toLowerCase()}-tbody`);
    if (!tbody) return;
    
    if (players.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="6" class="text-center py-4">
            <i class="bx bx-search icon-lg text-body-secondary"></i>
            <p class="mb-0 mt-2">No players match your filters</p>
          </td>
        </tr>
      `;
    } else {
      tbody.innerHTML = '';
      players.forEach(player => {
        const row = createPlayerRow(player);
        tbody.appendChild(row);
      });
    }
  });
  
  // Switch to the filtered position if specific position selected
  if (positionFilter !== 'all') {
    const tabButton = document.querySelector(`[data-bs-target="#${positionFilter.toLowerCase()}-tab"]`);
    if (tabButton) {
      tabButton.click();
    }
  }
}

/**
 * Sort table by column
 */
function sortTable(position, sortBy) {
  let players = [...(allPlayers[position] || [])];
  
  if (sortBy === 'salary') {
    players.sort((a, b) => (b.dk_salary || 0) - (a.dk_salary || 0));
  } else if (sortBy === 'name') {
    players.sort((a, b) => a.name.localeCompare(b.name));
  }
  
  // Update the display
  const tbody = document.getElementById(`${position.toLowerCase()}-tbody`);
  if (!tbody) return;
  
  tbody.innerHTML = '';
  players.forEach(player => {
    const row = createPlayerRow(player);
    tbody.appendChild(row);
  });
}

/**
 * Show error message
 */
function showError(message) {
  const positions = ['qb', 'rb', 'wr', 'te'];
  positions.forEach(pos => {
    const tbody = document.getElementById(`${pos}-tbody`);
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="6">
            <div class="alert alert-danger mb-0" role="alert">
              <h6 class="alert-heading mb-1">Error Loading Data</h6>
              <p class="mb-0">${message}</p>
            </div>
          </td>
        </tr>
      `;
    }
  });
}

// Add enter key support for search
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('player-search');
  if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        applyFilters();
      }
    });
  }
});