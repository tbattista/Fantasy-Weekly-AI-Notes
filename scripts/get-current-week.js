/**
 * Calculate current NFL week based on the date
 * NFL season typically starts first Thursday of September
 * Week 1 = First full week of games (Sunday after opening Thursday)
 */

function getCurrentNFLWeek() {
  const now = new Date();
  const year = now.getFullYear();
  
  // NFL 2025 Season starts September 4, 2025 (Week 1)
  // Adjust this date each season
  const seasonStart = new Date('2025-09-04T00:00:00-05:00');
  
  // Calculate weeks since season start
  const diffTime = now - seasonStart;
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  const weekNumber = Math.floor(diffDays / 7) + 1;
  
  // NFL regular season is weeks 1-18
  // Playoffs are weeks 19-22
  if (weekNumber < 1) return 1;
  if (weekNumber > 22) return 22;
  
  return weekNumber;
}

// Allow override from environment variable
const weekOverride = process.env.WEEK_OVERRIDE;
const currentWeek = weekOverride ? parseInt(weekOverride) : getCurrentNFLWeek();

// Export for use in other scripts
if (require.main === module) {
  console.log(currentWeek);
} else {
  module.exports = currentWeek;
}