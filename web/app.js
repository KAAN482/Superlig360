// Real Süper Lig data from Google (17. Hafta - 2025-26 Sezonu)
const REAL_STANDINGS = [
    { rank: 1, team_name: "Galatasaray", played: 17, wins: 13, draws: 3, losses: 1, goals_for: 39, goals_against: 12, goal_diff: 42, points: 42, form: ["G", "B", "G", "G", "G"] },
    { rank: 2, team_name: "Fenerbahçe", played: 17, wins: 11, draws: 6, losses: 0, goals_for: 39, goals_against: 14, goal_diff: 39, points: 39, form: ["G", "B", "B", "G", "G"] },
    { rank: 3, team_name: "Trabzonspor", played: 17, wins: 10, draws: 5, losses: 2, goals_for: 33, goals_against: 20, goal_diff: 35, points: 35, form: ["G", "G", "G", "B", "M"] },
    { rank: 4, team_name: "Göztepe", played: 17, wins: 9, draws: 5, losses: 3, goals_for: 21, goals_against: 9, goal_diff: 32, points: 32, form: ["B", "G", "M", "G", "G"] },
    { rank: 5, team_name: "Beşiktaş", played: 17, wins: 8, draws: 5, losses: 4, goals_for: 30, goals_against: 22, goal_diff: 29, points: 29, form: ["B", "G", "B", "B", "G"] },
    { rank: 6, team_name: "Samsunspor", played: 17, wins: 6, draws: 7, losses: 4, goals_for: 22, goals_against: 20, goal_diff: 25, points: 25, form: ["B", "B", "M", "M", "M"] },
    { rank: 7, team_name: "Başakşehir", played: 17, wins: 6, draws: 5, losses: 6, goals_for: 27, goals_against: 18, goal_diff: 23, points: 23, form: ["M", "G", "B", "G", "G"] },
    { rank: 8, team_name: "Kocaelispor", played: 17, wins: 6, draws: 5, losses: 6, goals_for: 15, goals_against: 17, goal_diff: -2, points: 23, form: ["B", "G", "B", "B", "G"] },
    { rank: 9, team_name: "Gaziantep FK", played: 17, wins: 6, draws: 5, losses: 6, goals_for: 24, goals_against: 30, goal_diff: -6, points: 23, form: ["G", "M", "B", "M", "M"] },
    { rank: 10, team_name: "Alanyaspor", played: 17, wins: 4, draws: 9, losses: 4, goals_for: 16, goals_against: 15, goal_diff: 21, points: 21, form: ["M", "B", "B", "B", "G"] },
    { rank: 11, team_name: "Gençlerbirliği", played: 17, wins: 5, draws: 3, losses: 9, goals_for: 21, goals_against: 24, goal_diff: -3, points: 18, form: ["M", "M", "G", "B", "G"] },
    { rank: 12, team_name: "Rizespor", played: 17, wins: 4, draws: 6, losses: 7, goals_for: 20, goals_against: 24, goal_diff: -4, points: 18, form: ["M", "M", "B", "G", "M"] },
    { rank: 13, team_name: "Konyaspor", played: 17, wins: 4, draws: 5, losses: 8, goals_for: 21, goals_against: 29, goal_diff: -8, points: 17, form: ["B", "M", "B", "M", "B"] },
    { rank: 14, team_name: "Kasımpaşa", played: 17, wins: 3, draws: 6, losses: 8, goals_for: 14, goals_against: 24, goal_diff: -10, points: 15, form: ["G", "M", "B", "B", "M"] },
    { rank: 15, team_name: "Antalyaspor", played: 17, wins: 4, draws: 3, losses: 10, goals_for: 16, goals_against: 31, goal_diff: -15, points: 15, form: ["B", "M", "B", "M", "M"] },
    { rank: 16, team_name: "Kayserispor", played: 17, wins: 2, draws: 9, losses: 6, goals_for: 16, goals_against: 33, goal_diff: -17, points: 15, form: ["M", "G", "B", "B", "B"] },
    { rank: 17, team_name: "Eyüpspor", played: 17, wins: 3, draws: 4, losses: 10, goals_for: 10, goals_against: 24, goal_diff: -14, points: 13, form: ["B", "G", "B", "M", "M"] },
    { rank: 18, team_name: "Fatih Karagümrük", played: 17, wins: 2, draws: 3, losses: 12, goals_for: 14, goals_against: 32, goal_diff: -18, points: 9, form: ["B", "M", "M", "B", "M"] },
];

// Gol Krallığı (FotMob 2025/2026)
const TOP_SCORERS = [
    { name: "Eldor Shomurodov", team: "Başakşehir", count: 12 },
    { name: "Paul Onuachu", team: "Trabzonspor", count: 11 },
    { name: "Mauro Icardi", team: "Galatasaray", count: 9 },
    { name: "Anderson Talisca", team: "Fenerbahçe", count: 9 },
    { name: "Felipe Augusto", team: "Trabzonspor", count: 8 }
];

// Asist Krallığı (FotMob 2025/2026)
const TOP_ASSISTS = [
    { name: "Barış Alper Yılmaz", team: "Galatasaray", count: 7 },
    { name: "Yunus Akgün", team: "Galatasaray", count: 6 },
    { name: "Alexandru Maxim", team: "Gaziantep FK", count: 6 },
    { name: "Václav Cerny", team: "Samsunspor", count: 6 },
    { name: "Göktan Gürpüz", team: "Trabzonspor", count: 5 }
];

// En İyi FotMob Rating (2025/2026)
const TOP_RATING = [
    { name: "Marco Asensio", team: "Fenerbahçe", count: 7.91 },
    { name: "Leroy Sané", team: "Galatasaray", count: 7.70 },
    { name: "Mateusz Lis", team: "Göztepe", count: 7.66 },
    { name: "Christ Inao Oulai", team: "Trabzonspor", count: 7.59 },
    { name: "Barış Alper Yılmaz", team: "Galatasaray", count: 7.57 }
];

// Kaçırılan Büyük Fırsatlar (FotMob 2025/2026)
const MISSED_CHANCES = [
    { name: "Paul Onuachu", team: "Trabzonspor", count: 10 },
    { name: "Tammy Abraham", team: "Beşiktaş", count: 10 },
    { name: "Victor Osimhen", team: "Galatasaray", count: 9 },
    { name: "Ali Sowe", team: "Göztepe", count: 9 },
    { name: "Janderson", team: "Gaziantep FK", count: 9 }
];

// Kalesini Gole Kapatanlar (FotMob 2025/2026)
const CLEAN_SHEETS = [
    { name: "Mateusz Lis", team: "Göztepe", count: 11 },
    { name: "Ertuğrul Taşkıran", team: "Alanyaspor", count: 7 },
    { name: "Uğurcan Çakır", team: "Trabzonspor", count: 6 },
    { name: "Aleksandar Jovanovic", team: "Kocaelispor", count: 6 },
    { name: "Ederson", team: "Fenerbahçe", count: 5 }
];

// Sarı Kartlar (FotMob 2025/2026)
const YELLOW_CARDS = [
    { name: "Emirhan Topçu", team: "Beşiktaş", count: 7 },
    { name: "Kevin Rodrigues", team: "Kasımpaşa", count: 6 },
    { name: "Arda Kızıldağ", team: "Gaziantep FK", count: 6 },
    { name: "Samet Akaydın", team: "Fenerbahçe", count: 6 },
    { name: "Show", team: "Çaykur Rizespor", count: 6 }
];

// Kırmızı Kartlar (FotMob 2025/2026)
const RED_CARDS = [
    { name: "Orkun Kökcü", team: "Galatasaray", count: 2 },
    { name: "Thalisson", team: "Antalyaspor", count: 2 },
    { name: "Kevin Rodrigues", team: "Kasımpaşa", count: 1 },
    { name: "Davinson Sanchez", team: "Galatasaray", count: 1 },
    { name: "Jayden Oosterwolde", team: "Fenerbahçe", count: 1 }
];

// Week 18 Fixtures from Google
const FIXTURES = [
    { home: "Başakşehir", away: "Fatih Karagümrük", date: "Yakında", time: "17:00" },
    { home: "Galatasaray", away: "Gaziantep FK", date: "Yakında", time: "20:00" },
    { home: "Kasımpaşa", away: "Antalyaspor", date: "Yakında", time: "14:30" },
    { home: "Gençlerbirliği", away: "Samsunspor", date: "Yakında", time: "17:00" },
    { home: "Kocaelispor", away: "Trabzonspor", date: "Yakında", time: "17:00" },
    { home: "Alanyaspor", away: "Fenerbahçe", date: "Yakında", time: "20:00" },
    { home: "Konyaspor", away: "Eyüpspor", date: "Yakında", time: "17:00" },
    { home: "Beşiktaş", away: "Kayserispor", date: "Yakında", time: "20:00" },
    { home: "Göztepe", away: "Rizespor", date: "Yakında", time: "20:00" },
];

// Get team data by name
function getTeamData(teamName) {
    return REAL_STANDINGS.find(t => t.team_name === teamName);
}

// Calculate form score (recent form weight)
function calculateFormScore(form) {
    let score = 0;
    const weights = [1, 1.2, 1.4, 1.6, 2]; // More recent = more weight
    form.forEach((result, i) => {
        if (result === 'G') score += 3 * weights[i];
        else if (result === 'B') score += 1 * weights[i];
    });
    return score;
}

// AI Prediction based on standings position and form
function predictMatch(homeTeam, awayTeam) {
    const home = getTeamData(homeTeam);
    const away = getTeamData(awayTeam);

    if (!home || !away) return { prediction: "?", confidence: 0 };

    // Calculate strength scores
    const homeAdvantage = 1.15; // 15% home advantage
    const homeFormScore = calculateFormScore(home.form);
    const awayFormScore = calculateFormScore(away.form);

    // Points per game
    const homePPG = home.points / home.played;
    const awayPPG = away.points / away.played;

    // Goal difference factor
    const homeGD = home.goal_diff / home.played;
    const awayGD = away.goal_diff / away.played;

    // Combined strength
    const homeStrength = (homePPG * 10 + homeFormScore + homeGD) * homeAdvantage;
    const awayStrength = awayPPG * 10 + awayFormScore + awayGD;

    const diff = homeStrength - awayStrength;
    const total = homeStrength + awayStrength;

    let prediction, confidence;

    if (diff > 4) {
        prediction = home.team_name;
        confidence = Math.min(85, 60 + Math.abs(diff) * 3);
    } else if (diff < -4) {
        prediction = away.team_name;
        confidence = Math.min(85, 60 + Math.abs(diff) * 3);
    } else if (diff > 1.5) {
        prediction = home.team_name;
        confidence = Math.min(65, 50 + Math.abs(diff) * 3);
    } else if (diff < -1.5) {
        prediction = away.team_name;
        confidence = Math.min(65, 50 + Math.abs(diff) * 3);
    } else {
        prediction = "Beraberlik";
        confidence = 45;
    }

    return { prediction, confidence: Math.round(confidence) };
}

// Render form badges
function renderFormBadges(form) {
    return form.map(result => {
        const classes = {
            'G': 'form-win',
            'B': 'form-draw',
            'M': 'form-loss'
        };
        return `<span class="form-badge ${classes[result]}">${result}</span>`;
    }).join('');
}

// Get zone class for team position
function getZoneClass(rank) {
    if (rank === 1) return 'zone-ucl';           // Şampiyonlar Ligi
    if (rank >= 2 && rank <= 3) return 'zone-uel'; // Avrupa Ligi
    if (rank >= 4 && rank <= 5) return 'zone-uecl'; // Konferans Ligi
    if (rank >= 16) return 'zone-relegation';     // Küme düşme
    return '';
}

// Load standings table
function loadStandings() {
    const tbody = document.getElementById('standings-body');
    tbody.innerHTML = REAL_STANDINGS.map((team) => `
        <tr class="${getZoneClass(team.rank)}">
            <td class="rank">${team.rank}</td>
            <td class="team-name">${team.team_name}</td>
            <td>${team.played}</td>
            <td class="wins">${team.wins}</td>
            <td>${team.draws}</td>
            <td class="losses">${team.losses}</td>
            <td>${team.goals_for}</td>
            <td>${team.goals_against}</td>
            <td class="${team.goal_diff >= 0 ? 'positive' : 'negative'}">${team.goal_diff > 0 ? '+' : ''}${team.goal_diff}</td>
            <td class="points">${team.points}</td>
            <td class="form-cell">${renderFormBadges(team.form)}</td>
        </tr>
    `).join('');
}

// Render stats grid
function renderStatsGrid(data, gridId, label) {
    const grid = document.getElementById(gridId);
    grid.innerHTML = data.map((item, index) => `
        <div class="stat-card ${index < 3 ? 'top-3' : ''}">
            <div class="stat-rank">${index + 1}</div>
            <div class="stat-info">
                <div class="stat-name">${item.name}</div>
                <div class="stat-team">${item.team}</div>
            </div>
            <div class="stat-count">${item.count}</div>
        </div>
    `).join('');
}

// Load fixtures with AI predictions
function loadFixtures() {
    const container = document.getElementById('fixtures-grid');
    container.innerHTML = FIXTURES.map(match => {
        const homeData = getTeamData(match.home);
        const awayData = getTeamData(match.away);
        const prediction = predictMatch(match.home, match.away);

        return `
        <div class="fixture-card">
            <div class="fixture-team-row">
                <div class="fixture-team home">
                    <div class="team-form">${homeData ? renderFormBadges(homeData.form) : ''}</div>
                    <span class="team-name">${match.home}</span>
                    <span class="team-rank">${homeData ? homeData.rank + '.' : ''}</span>
                </div>
                <span class="vs">vs</span>
                <div class="fixture-team away">
                    <span class="team-rank">${awayData ? awayData.rank + '.' : ''}</span>
                    <span class="team-name">${match.away}</span>
                    <div class="team-form">${awayData ? renderFormBadges(awayData.form) : ''}</div>
                </div>
            </div>
            <div class="fixture-info">
                <span class="fixture-date">📅 ${match.date}</span>
                <span class="fixture-time">⏰ ${match.time}</span>
            </div>
            <div class="ai-prediction">
                <span class="ai-label">🤖 AI Tahmini:</span>
                <span class="ai-result ${prediction.prediction === 'Beraberlik' ? 'draw' : ''}">${prediction.prediction}</span>
                <span class="ai-confidence">(%${prediction.confidence})</span>
            </div>
        </div>
    `}).join('');
}

// Tüm istatistikleri yükle
function loadStats() {
    renderStatsGrid(TOP_SCORERS, 'goals-grid', 'Gol');
    renderStatsGrid(TOP_ASSISTS, 'assists-grid', 'Asist');
    renderStatsGrid(TOP_RATING, 'rating-grid', 'Rating');
    renderStatsGrid(MISSED_CHANCES, 'missed-grid', 'Kaçırılan');
    renderStatsGrid(CLEAN_SHEETS, 'cleansheet-grid', 'Gol Yemeden');
    renderStatsGrid(YELLOW_CARDS, 'yellow-grid', 'Sarı Kart');
    renderStatsGrid(RED_CARDS, 'red-grid', 'Kırmızı Kart');
}

// Background images for each tab (from Unsplash - free to use)
const TAB_BACKGROUNDS = {
    standings: 'linear-gradient(rgba(15, 23, 42, 0.85), rgba(30, 41, 59, 0.9)), url("https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?w=1920&q=80")',
    stats: 'linear-gradient(rgba(15, 23, 42, 0.85), rgba(6, 78, 59, 0.9)), url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1920&q=80")',
    fixtures: 'linear-gradient(rgba(15, 23, 42, 0.85), rgba(88, 28, 135, 0.9)), url("https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1920&q=80")'
};

// Change background based on tab
function changeBackground(tabName) {
    const bg = TAB_BACKGROUNDS[tabName] || TAB_BACKGROUNDS.standings;
    document.body.style.background = bg;
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundPosition = 'center';
    document.body.style.backgroundAttachment = 'fixed';
}

// Tab switching for main tabs
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');
        changeBackground(btn.dataset.tab);
    });
});

// Tab switching for stats sub-tabs
document.querySelectorAll('.stats-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.stats-tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.stats-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.stat).classList.add('active');
    });
});

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    loadStandings();
    loadStats();
    loadFixtures();
});
