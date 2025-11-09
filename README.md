# Fantasy Weekly AI Notes - NFL Dashboard

A comprehensive NFL Week 10 Fantasy Football dashboard built with the Sneat Bootstrap template, featuring DFS player analysis, weather alerts, betting trends, and game breakdowns.

![Dashboard Preview](https://img.shields.io/badge/Status-Ready%20for%20Deployment-success)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🚀 Features

- **📊 Games Dashboard**: Overview of all Week 10 games with spreads, totals, and weather alerts
- **👥 DFS Player Pool**: Sortable and filterable player analysis with salaries and projections
- **🎯 Game Details**: In-depth game breakdowns with trends, injuries, and betting angles
- **🌤️ Weather Impact**: Visual weather alerts and impact analysis for outdoor games
- **📱 Responsive Design**: Mobile-first design using Bootstrap 5
- **⚡ Fast Loading**: Static site with client-side rendering for optimal performance

## 📁 Project Structure

```
fantasy-weekly-dashboard/
├── index.html                    # Main dashboard
├── pages/
│   ├── dfs-players.html         # DFS player analysis
│   ├── game-details.html        # Game breakdowns
│   └── weather.html             # Weather impact view
├── assets/
│   └── js/
│       ├── data-loader.js       # Data management class
│       ├── dashboard.js         # Main dashboard logic
│       ├── dfs-players.js       # DFS players page logic
│       └── game-details.js      # Game details logic
├── data/
│   └── week10-data.json         # NFL game data
├── sneat-bootstrap-template/    # Sneat template files
├── Dockerfile                    # Docker configuration
├── railway.json                  # Railway deployment config
└── README.md                     # This file
```

## 🛠️ Local Development

### Prerequisites

- Node.js (LTS version recommended)
- npm or yarn
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd fantasy-weekly-dashboard
   ```

2. **Install dependencies** (for Sneat template build tools)
   ```bash
   cd sneat-bootstrap-template
   npm install --legacy-peer-deps
   ```

3. **Start development server**
   ```bash
   npm run serve
   ```

4. **Open in browser**
   ```
   http://localhost:3000
   ```

### Development Workflow

The project uses Gulp for build automation:

- `npm run serve` - Start dev server with live reload
- `npm run build` - Build for production
- `npm run watch` - Watch files for changes

## 🚂 Railway Deployment

### Method 1: Deploy from GitHub (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Fantasy Weekly Dashboard"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to [Railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the Dockerfile and deploy

3. **Configure Domain** (Optional)
   - In Railway dashboard, go to Settings
   - Generate a domain or add custom domain

### Method 2: Deploy with Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize and Deploy**
   ```bash
   railway init
   railway up
   ```

4. **Open deployed site**
   ```bash
   railway open
   ```

## 📊 Data Management

### Updating Game Data

To update the dashboard with new data:

1. **Edit the JSON file**
   ```bash
   # Edit data/week10-data.json with new game data
   ```

2. **Commit and push**
   ```bash
   git add data/week10-data.json
   git commit -m "Update Week 10 data"
   git push
   ```

3. **Railway auto-deploys** - Changes will be live in ~2 minutes

### JSON Data Structure

The `week10-data.json` file contains:
- `games[]` - Array of game objects with vegas lines, weather, injuries
- `dfs_player_pool` - Player recommendations by position
- `weather_watch[]` - Games with weather alerts
- `outlier_summary` - Betting trends and insights

## 🎨 Customization

### Branding

Update branding in:
- `index.html` - Change "Fantasy Weekly" text
- `sneat-bootstrap-template/assets/img/favicon/` - Replace favicon

### Styling

Custom styles can be added to:
- `assets/css/custom.css` (create this file)
- Link in HTML: `<link rel="stylesheet" href="assets/css/custom.css">`

### Adding New Pages

1. Create HTML file in `pages/` directory
2. Create corresponding JS file in `assets/js/`
3. Add menu item in navigation sidebar
4. Use data-loader.js to access NFL data

## 🔧 Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **Template**: Sneat Admin Template (Free)
- **Charts**: ApexCharts
- **Icons**: Boxicons
- **Deployment**: Docker + Nginx on Railway
- **Build Tools**: Gulp, Webpack

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🐛 Troubleshooting

### Data Not Loading

**Issue**: Games or players not displaying

**Solution**:
1. Check browser console for errors (F12)
2. Verify `data/week10-data.json` is valid JSON
3. Check file paths are correct (relative paths)
4. Clear browser cache and reload

### Railway Deployment Fails

**Issue**: Build fails on Railway

**Solution**:
1. Check Dockerfile syntax
2. Verify all files are committed to Git
3. Check Railway build logs for specific errors
4. Ensure `railway.json` is in root directory

### Styling Issues

**Issue**: CSS not loading correctly

**Solution**:
1. Verify all CSS files are in correct locations
2. Check file paths in HTML (relative to page location)
3. Clear browser cache
4. Check for CSS conflicts in browser dev tools

## 📄 License

This project uses the Sneat Bootstrap Template which is licensed under MIT.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review Railway documentation for deployment issues

## 🎯 Roadmap

- [ ] Add game details page with charts
- [ ] Implement weather visualization page
- [ ] Add player comparison tool
- [ ] Export DFS lineups to CSV
- [ ] Add historical data tracking
- [ ] Implement dark mode toggle
- [ ] Add mobile app (PWA)

## 📚 Resources

- [Sneat Documentation](https://demos.themeselection.com/sneat-bootstrap-html-admin-template/documentation/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Railway Docs](https://docs.railway.app/)
- [ApexCharts Docs](https://apexcharts.com/docs/)

---

**Built with ❤️ for Fantasy Football enthusiasts**

Last Updated: November 2025