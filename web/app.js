// Real Süper Lig data from Google (17. Hafta - 2025-26 Sezonu)
const REAL_STANDINGS = [
    { rank: 1, team_name: "Galatasaray", played: 19, wins: 14, draws: 4, losses: 1, goals_for: 43, goals_against: 14, goal_diff: 29, points: 46, form: ["G", "G", "G", "B", "G"] },
    { rank: 2, team_name: "Fenerbahçe", played: 19, wins: 12, draws: 7, losses: 0, goals_for: 43, goals_against: 17, goal_diff: 26, points: 43, form: ["B", "G", "G", "G", "B"] },
    { rank: 3, team_name: "Trabzonspor", played: 19, wins: 12, draws: 5, losses: 2, goals_for: 37, goals_against: 22, goal_diff: 15, points: 41, form: ["G", "B", "M", "G", "G"] },
    { rank: 4, team_name: "Göztepe", played: 19, wins: 10, draws: 6, losses: 3, goals_for: 25, goals_against: 11, goal_diff: 14, points: 36, form: ["M", "G", "G", "G", "B"] },
    { rank: 5, team_name: "Beşiktaş", played: 19, wins: 9, draws: 6, losses: 4, goals_for: 33, goals_against: 24, goal_diff: 9, points: 33, form: ["B", "B", "G", "G", "B"] },
    { rank: 6, team_name: "Başakşehir", played: 19, wins: 8, draws: 5, losses: 6, goals_for: 32, goals_against: 19, goal_diff: 13, points: 29, form: ["B", "G", "G", "G", "G"] },
    { rank: 7, team_name: "Samsunspor", played: 19, wins: 6, draws: 9, losses: 4, goals_for: 23, goals_against: 21, goal_diff: 2, points: 27, form: ["M", "M", "M", "B", "B"] },
    { rank: 8, team_name: "Gaziantep FK", played: 19, wins: 6, draws: 7, losses: 6, goals_for: 26, goals_against: 32, goal_diff: -6, points: 25, form: ["B", "M", "M", "B", "B"] },
    { rank: 9, team_name: "Kocaelispor", played: 19, wins: 6, draws: 6, losses: 7, goals_for: 16, goals_against: 19, goal_diff: -3, points: 24, form: ["B", "B", "G", "M", "B"] },
    { rank: 10, team_name: "Alanyaspor", played: 19, wins: 4, draws: 10, losses: 5, goals_for: 19, goals_against: 19, goal_diff: 0, points: 22, form: ["B", "B", "G", "M", "B"] },
    { rank: 11, team_name: "Gençlerbirliği", played: 19, wins: 5, draws: 4, losses: 10, goals_for: 23, goals_against: 27, goal_diff: -4, points: 19, form: ["G", "B", "G", "B", "M"] },
    { rank: 12, team_name: "Rizespor", played: 19, wins: 4, draws: 7, losses: 8, goals_for: 22, goals_against: 28, goal_diff: -6, points: 19, form: ["B", "G", "M", "M", "B"] },
    { rank: 13, team_name: "Konyaspor", played: 19, wins: 4, draws: 7, losses: 8, goals_for: 23, goals_against: 31, goal_diff: -8, points: 19, form: ["B", "M", "B", "B", "B"] },
    { rank: 14, team_name: "Antalyaspor", played: 19, wins: 5, draws: 4, losses: 10, goals_for: 18, goals_against: 32, goal_diff: -14, points: 19, form: ["B", "M", "M", "B", "G"] },
    { rank: 15, team_name: "Kasımpaşa", played: 19, wins: 3, draws: 7, losses: 9, goals_for: 15, goals_against: 26, goal_diff: -11, points: 16, form: ["B", "B", "M", "B", "M"] },
    { rank: 16, team_name: "Eyüpspor", played: 19, wins: 3, draws: 6, losses: 10, goals_for: 13, goals_against: 27, goal_diff: -14, points: 15, form: ["B", "M", "M", "B", "B"] },
    { rank: 17, team_name: "Kayserispor", played: 19, wins: 2, draws: 9, losses: 8, goals_for: 16, goals_against: 37, goal_diff: -21, points: 15, form: ["B", "B", "B", "M", "M"] },
    { rank: 18, team_name: "Fatih Karagümrük", played: 19, wins: 2, draws: 3, losses: 14, goals_for: 16, goals_against: 37, goal_diff: -21, points: 9, form: ["M", "B", "M", "M", "M"] },
];

// Gol Krallığı (FotMob 2025/2026)
const TOP_SCORERS = [
    { name: "Eldor Shomurodov", team: "Bilinmiyor", count: 13 },
    { name: "Paul Onuachu", team: "Bilinmiyor", count: 12 },
    { name: "Anderson Talisca", team: "Bilinmiyor", count: 11 },
    { name: "Felipe Augusto", team: "Bilinmiyor", count: 9 },
    { name: "Mauro Icardi", team: "Bilinmiyor", count: 9 },
];

// Asist Krallığı (FotMob 2025/2026)
const TOP_ASSISTS = [
    { name: "Baris Alper Yilmaz", team: "Bilinmiyor", count: 7 },
    { name: "Alexandru Maxim", team: "Bilinmiyor", count: 6 },
    { name: "Yunus Akgün", team: "Bilinmiyor", count: 6 },
    { name: "Václav Cerny", team: "Bilinmiyor", count: 6 },
    { name: "Marco Asensio", team: "Bilinmiyor", count: 6 },
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
    { name: "Paul Onuachu", team: "Bilinmiyor", count: 10 },
    { name: "Tammy Abraham", team: "Bilinmiyor", count: 10 },
    { name: "Janderson", team: "Bilinmiyor", count: 10 },
    { name: "Mohamed Bayo", team: "Bilinmiyor", count: 9 },
    { name: "Eldor Shomurodov", team: "Bilinmiyor", count: 9 },
];

// Kalesini Gole Kapatanlar (FotMob 2025/2026)
const CLEAN_SHEETS = [
    { name: "Mateusz Lis", team: "Bilinmiyor", count: 11 },
    { name: "Ertugrul Taskiran", team: "Bilinmiyor", count: 7 },
    { name: "Ugurcan Cakir", team: "Bilinmiyor", count: 6 },
    { name: "Aleksandar Jovanovic", team: "Bilinmiyor", count: 6 },
    { name: "Muhammed Sengezer", team: "Bilinmiyor", count: 6 },
];

// Sarı Kartlar (FotMob 2025/2026)
const YELLOW_CARDS = [
    { name: "Emirhan Topcu", team: "Bilinmiyor", count: 7 },
    { name: "Show", team: "Bilinmiyor", count: 7 },
    { name: "Kevin Rodrigues", team: "Bilinmiyor", count: 6 },
    { name: "Arda Kizildag", team: "Bilinmiyor", count: 6 },
    { name: "Fidan Aliti", team: "Bilinmiyor", count: 6 },
];

// Kırmızı Kartlar (FotMob 2025/2026)
const RED_CARDS = [
    { name: "Orkun Kökcü", team: "Bilinmiyor", count: 2 },
    { name: "Thalisson", team: "Bilinmiyor", count: 2 },
    { name: "Kevin Rodrigues", team: "Bilinmiyor", count: 1 },
    { name: "Jure Balkovec", team: "Bilinmiyor", count: 1 },
    { name: "Davinson Sánchez", team: "Bilinmiyor", count: 1 },
];

// Week 18 Fixtures from Google
const FIXTURES = [
    { home: "Antalyaspor", away: "Trabzonspor", date: "30 Ocak", time: "20:00", score: null, status: "oynanacak" },
    { home: "Kasımpaşa", away: "Samsunspor", date: "30 Ocak", time: "20:00", score: null, status: "oynanacak" },
    { home: "Alanyaspor", away: "Eyüpspor", date: "31 Ocak", time: "14:30", score: null, status: "oynanacak" },
    { home: "Başakşehir", away: "Rizespor", date: "31 Ocak", time: "17:00", score: null, status: "oynanacak" },
    { home: "Beşiktaş", away: "Konyaspor", date: "31 Ocak", time: "20:00", score: null, status: "oynanacak" },
    { home: "Göztepe", away: "Fatih Karagümrük", date: "31 Ocak", time: "20:00", score: null, status: "oynanacak" },
    { home: "Gençlerbirliği", away: "Gaziantep FK", date: "1 Şubat", time: "17:00", score: null, status: "oynanacak" },
    { home: "Galatasaray", away: "Kayserispor", date: "1 Şubat", time: "20:00", score: null, status: "oynanacak" },
    { home: "Kocaelispor", away: "Fenerbahçe", date: "2 Şubat", time: "20:00", score: null, status: "oynanacak" },
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
                ${item.team !== 'Bilinmiyor' ? `<div class="stat-team">${item.team}</div>` : ''}
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

        // Oynanan maç mı kontrolü
        const isPlayed = match.status === 'oynandi' && match.score;

        return `
        <div class="fixture-card ${isPlayed ? 'played-match' : ''}">
            <div class="fixture-team-row">
                <div class="fixture-team home">
                    <div class="team-form-box">${homeData ? renderFormBadges(homeData.form) : ''}</div>
                    <div class="team-info-row">
                        <div class="team-rank-box">${homeData ? homeData.rank + '.' : ''}</div>
                        <span class="team-name">${match.home}</span>
                    </div>
                </div>
                <span class="vs">vs</span>
                <div class="fixture-team away">
                    <div class="team-form-box">${awayData ? renderFormBadges(awayData.form) : ''}</div>
                    <div class="team-info-row">
                        <div class="team-rank-box">${awayData ? awayData.rank + '.' : ''}</div>
                        <span class="team-name">${match.away}</span>
                    </div>
                </div>
            </div>
            <div class="fixture-info">
                ${isPlayed
                ? `<span class="fixture-score">${match.score}</span>`
                : `<span class="fixture-date">📅 ${match.date}</span>
                   <span class="fixture-time">⏰ ${match.time}</span>`
            }
            </div>
            ${!isPlayed ? `
            <div class="ai-prediction">
                <span class="ai-label">🤖 AI Tahmini:</span>
                <span class="ai-result ${prediction.prediction === 'Beraberlik' ? 'draw' : ''}">${prediction.prediction}</span>
                <span class="ai-confidence">(%${prediction.confidence})</span>
            </div>
            ` : ''}
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
function switchToTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

    const activeBtn = document.querySelector(`.tab-btn[data-tab="${tabName}"]`);
    const activeContent = document.getElementById(tabName);

    if (activeBtn) activeBtn.classList.add('active');
    if (activeContent) activeContent.classList.add('active');

    changeBackground(tabName);
}

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        switchToTab(tabName);
        window.location.hash = tabName;
    });
});

// Tab switching for stats sub-tabs
document.querySelectorAll('.stats-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const statName = btn.dataset.stat;
        document.querySelectorAll('.stats-tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.stats-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(statName).classList.add('active');
        window.location.hash = `stats-${statName}`;
    });
});

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    loadStandings();
    loadStats();
    loadFixtures();

    // URL hash'e göre sekme aç
    const hash = window.location.hash.substring(1);
    if (hash) {
        if (hash.startsWith('stats-')) {
            // İstatistikler alt sekmesi
            switchToTab('stats');
            const statTab = hash.replace('stats-', '');
            setTimeout(() => {
                const statBtn = document.querySelector(`.stats-tab-btn[data-stat="${statTab}"]`);
                if (statBtn) statBtn.click();
            }, 100);
        } else if (['standings', 'stats', 'fixtures'].includes(hash)) {
            switchToTab(hash);
        }
    }
});
