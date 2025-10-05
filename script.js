// Funções utilitárias globais
class DataLoader {
    static async loadJSON(url) {
        try {
            // Adicionar timestamp para evitar cache
            const urlWithTimestamp = `${url}?t=${Date.now()}`;
            const response = await fetch(urlWithTimestamp);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            return null;
        }
    }

    static formatPercentage(value) {
        if (value === null || value === undefined || isNaN(value)) {
            return '0.0%';
        }
        // Os dados já estão em percentual (0.1 = 0.1%, 46.6 = 46.6%)
        // Não multiplicar por 100, apenas formatar
        return `${value.toFixed(1)}%`;
    }

    static formatNumber(value) {
        if (value === null || value === undefined || isNaN(value)) {
            return '0';
        }
        return value.toLocaleString('pt-BR');
    }

    static getProgressBarClass(percentage) {
        if (percentage === null || percentage === undefined || isNaN(percentage)) {
            return 'low';
        }
        if (percentage >= 70) return 'high';
        if (percentage >= 30) return 'medium';
        return 'low';
    }

    static createProgressBar(percentage, showText = true) {
        if (percentage === null || percentage === undefined || isNaN(percentage)) {
            percentage = 0;
        }
        
        const progressClass = this.getProgressBarClass(percentage);
        const text = showText ? `${this.formatPercentage(percentage)}` : '';
        
        return `
            <div class="progress-bar">
                <div class="progress-fill ${progressClass}" style="width: ${percentage}%">
                    ${text}
                </div>
            </div>
        `;
    }

    static formatDate(dateString) {
        if (!dateString) return 'N/A';
        try {
            // Parse da data no formato YYYY-MM-DD sem conversão de timezone
            const parts = dateString.split('-');
            if (parts.length === 3) {
                const year = parseInt(parts[0]);
                const month = parseInt(parts[1]) - 1; // Mês é 0-indexado
                const day = parseInt(parts[2]);
                const date = new Date(year, month, day);
                return date.toLocaleDateString('pt-BR');
            } else {
                // Fallback para formato ISO
                const date = new Date(dateString + 'T00:00:00');
                return date.toLocaleDateString('pt-BR');
            }
        } catch (error) {
            return 'N/A';
        }
    }
}

// Funções para criar gráficos
class ChartManager {
    static charts = {}; // Armazenar referências dos gráficos
    
    static createBarChart(canvasId, data, title, colors = ['#3498db']) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        // Destruir gráfico existente se houver
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }

        // Criar novo gráfico
        this.charts[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: title,
                    data: data.values,
                    backgroundColor: colors,
                    borderColor: colors.map(color => color.replace('0.8', '1')),
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: title,
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 0
                        }
                    }
                }
            }
        });
    }

    static createDoughnutChart(canvasId, data, title, colors = ['#e74c3c', '#f39c12', '#27ae60', '#3498db']) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        // Destruir gráfico existente se houver
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }

        // Criar novo gráfico
        this.charts[canvasId] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: title,
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    }
    
    static destroyChart(canvasId) {
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }
    }
    
    static destroyAllCharts() {
        Object.keys(this.charts).forEach(canvasId => {
            this.destroyChart(canvasId);
        });
    }
}

// Funções para tabelas
class TableManager {
    static populateTable(tableBodyId, data, columns, formatters = {}) {
        const tbody = document.getElementById(tableBodyId);
        if (!tbody) return;

        tbody.innerHTML = '';

        data.forEach((item, index) => {
            const row = document.createElement('tr');
            
            columns.forEach(column => {
                const cell = document.createElement('td');
                let value = item[column.key];
                
                // Aplicar formatador se existir
                if (formatters[column.key]) {
                    value = formatters[column.key](value, item, index);
                }
                
                cell.innerHTML = value;
                row.appendChild(cell);
            });
            
            tbody.appendChild(row);
        });
    }

    static createTitleTable(data, tableBodyId) {
        const columns = [
            { key: 'position', label: 'Pos' },
            { key: 'team', label: 'Time' },
            { key: 'probability', label: 'Probabilidade' }
        ];

        const formatters = {
            position: (value, item, index) => index + 1,
            team: (value) => value,
            probability: (value) => DataLoader.formatPercentage(value)
        };

        this.populateTable(tableBodyId, data, columns, formatters);
    }

    static createProbabilityTable(data, tableBodyId, probabilityKey) {
        const columns = [
            { key: 'team', label: 'Time' },
            { key: probabilityKey, label: 'Probabilidade' }
        ];

        const formatters = {
            team: (value) => value,
            [probabilityKey]: (value) => DataLoader.formatPercentage(value)
        };

        this.populateTable(tableBodyId, data, columns, formatters);
    }

    static createClassificationTable(data, tableBodyId) {
        const columns = [
            { key: 'position', label: 'Pos' },
            { key: 'time', label: 'Time' },
            { key: 'pontos', label: 'Pts' },
            { key: 'jogos', label: 'J' },
            { key: 'vitorias', label: 'V' },
            { key: 'empates', label: 'E' },
            { key: 'derrotas', label: 'D' },
            { key: 'gols_pro', label: 'GP' },
            { key: 'gols_contra', label: 'GC' },
            { key: 'saldo_gols', label: 'SG' }
        ];

        const formatters = {
            position: (value, item, index) => index + 1,
            time: (value) => value,
            pontos: (value) => value || 0,
            jogos: (value) => value || 0,
            vitorias: (value) => value || 0,
            empates: (value) => value || 0,
            derrotas: (value) => value || 0,
            gols_pro: (value) => value || 0,
            gols_contra: (value) => value || 0,
            saldo_gols: (value) => value || 0
        };

        this.populateTable(tableBodyId, data, columns, formatters);
    }
}

// Funções para próximos jogos
class NextGamesManager {
    static async loadNextGames(series, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        try {
            const data = await DataLoader.loadJSON(`data/proximos_jogos_${series}.json`);
            if (!data) {
                container.innerHTML = '<p class="error">Erro ao carregar próximos jogos</p>';
                return;
            }

            this.displayNextGames(data, container);
        } catch (error) {
            console.error('Erro ao carregar próximos jogos:', error);
            container.innerHTML = '<p class="error">Erro ao carregar próximos jogos</p>';
        }
    }

    static displayNextGamesWithProbabilities(data, container, proximaRodada = null) {
        container.innerHTML = '';
        
        // Adicionar cabeçalho com número da rodada
        if (proximaRodada) {
            const headerElement = document.createElement('div');
            headerElement.className = 'next-games-header';
            headerElement.innerHTML = `<h3>Rodada ${proximaRodada}</h3>`;
            container.appendChild(headerElement);
        }
        
        // Converter para array e remover duplicatas
        const allGames = [];
        const gameIds = new Set(); // Para evitar duplicatas
        
        Object.entries(data).forEach(([team, games]) => {
            if (games && games.length > 0) {
                games.forEach(game => {
                    // Criar ID único para o jogo
                    const gameId = `${game.dateEvent}_${game.strHomeTeam}_${game.strAwayTeam}`;
                    
                    if (!gameIds.has(gameId)) {
                        gameIds.add(gameId);
                        allGames.push({
                            ...game,
                            team: team,
                            gameId: gameId
                        });
                    }
                });
            }
        });
        
        // Ordenar por data
        allGames.sort((a, b) => new Date(a.dateEvent) - new Date(b.dateEvent));
        
        if (allGames.length === 0) {
            const noGamesElement = document.createElement('div');
            noGamesElement.className = 'no-games';
            noGamesElement.innerHTML = '<p>Nenhum jogo encontrado para esta rodada.</p>';
            container.appendChild(noGamesElement);
            return;
        }
        
        allGames.forEach(game => {
            const gameElement = document.createElement('div');
            gameElement.className = 'next-game-row';
            
            // Usar probabilidades calculadas pelo backend ou estimar se não disponível
            const probabilities = game.probabilidades || this.estimateGameProbabilities(game.strHomeTeam, game.strAwayTeam);
            
            gameElement.innerHTML = `
                <div class="game-info">
                    <div class="game-date">${DataLoader.formatDate(game.dateEvent)}</div>
                    <div class="game-time">${game.strTime || 'TBD'}</div>
                </div>
                <div class="game-teams">
                    <span class="home-team">${game.strHomeTeam}</span>
                    <span class="vs">vs</span>
                    <span class="away-team">${game.strAwayTeam}</span>
                </div>
                <div class="game-probabilities">
                    <span class="prob-home">${DataLoader.formatPercentage(probabilities.home)}</span>
                    <span class="prob-draw">${DataLoader.formatPercentage(probabilities.draw)}</span>
                    <span class="prob-away">${DataLoader.formatPercentage(probabilities.away)}</span>
                </div>
            `;
            
            container.appendChild(gameElement);
        });
    }
    
    static estimateGameProbabilities(homeTeam, awayTeam) {
        // Probabilidades baseadas em fatores gerais
        // Em um sistema real, isso seria baseado em dados históricos e classificação
        
        // Fator casa: time da casa tem vantagem
        const homeAdvantage = 0.05;
        
        // Probabilidades base mais realistas
        let homeProb = 0.40;
        let awayProb = 0.30;
        let drawProb = 0.30;
        
        // Ajustar baseado em "força" dos times (simplificado)
        const teamStrength = this.getTeamStrength(homeTeam, awayTeam);
        
        if (teamStrength.home > teamStrength.away) {
            homeProb += 0.10;
            awayProb -= 0.05;
            drawProb -= 0.05;
        } else if (teamStrength.away > teamStrength.home) {
            awayProb += 0.10;
            homeProb -= 0.05;
            drawProb -= 0.05;
        }
        
        // Aplicar vantagem de casa
        homeProb += homeAdvantage;
        awayProb -= homeAdvantage * 0.3;
        drawProb -= homeAdvantage * 0.7;
        
        // Garantir que as probabilidades sejam razoáveis
        homeProb = Math.max(0.25, Math.min(0.65, homeProb));
        awayProb = Math.max(0.20, Math.min(0.50, awayProb));
        drawProb = Math.max(0.15, Math.min(0.40, drawProb));
        
        // Normalizar para somar 100%
        const total = homeProb + awayProb + drawProb;
        
        return {
            home: homeProb / total,
            draw: drawProb / total,
            away: awayProb / total
        };
    }
    
    static getTeamStrength(team1, team2) {
        // Força simplificada baseada em nomes conhecidos
        // Em um sistema real, isso viria de dados históricos
        const strongTeams = ['Flamengo', 'Palmeiras', 'Cruzeiro', 'São Paulo', 'Corinthians', 'Atlético Mineiro', 'Grêmio', 'Internacional'];
        const mediumTeams = ['Botafogo', 'Fluminense', 'Santos', 'Bragantino', 'Vasco da Gama', 'Bahia', 'Fortaleza', 'Ceará'];
        
        return {
            home: this.getTeamStrengthValue(team1, strongTeams, mediumTeams),
            away: this.getTeamStrengthValue(team2, strongTeams, mediumTeams)
        };
    }
    
    static getTeamStrengthValue(team, strongTeams, mediumTeams) {
        if (strongTeams.includes(team)) return 0.8;
        if (mediumTeams.includes(team)) return 0.6;
        return 0.4; // Times menores
    }
}

// Funções para estatísticas gerais
class StatsManager {
    static async loadAndDisplayStats(series, containerId) {
        try {
            const cacheData = await DataLoader.loadJSON(`data/cache_jogos_${series}.json`);
            const resultsData = await DataLoader.loadJSON(`data/resultados_simulacao_${series}.json`);
            
            if (!cacheData || !resultsData) {
                console.error('Erro ao carregar dados de estatísticas');
                return;
            }

            this.displayStats(cacheData, resultsData, containerId);
        } catch (error) {
            console.error('Erro ao carregar estatísticas:', error);
        }
    }

    static displayStats(cacheData, resultsData, containerId) {
        // Calcular total de jogos
        let totalGames = 0;
        Object.values(cacheData).forEach(games => {
            if (Array.isArray(games)) {
                totalGames += games.length;
            }
        });

        // Calcular média de gols
        let totalGoals = 0;
        let gamesWithGoals = 0;
        
        Object.values(cacheData).forEach(games => {
            if (Array.isArray(games)) {
                games.forEach(game => {
                    if (game.intHomeScore !== null && game.intAwayScore !== null) {
                        const homeScore = parseInt(game.intHomeScore) || 0;
                        const awayScore = parseInt(game.intAwayScore) || 0;
                        totalGoals += homeScore + awayScore;
                        gamesWithGoals++;
                    }
                });
            }
        });

        const avgGoals = gamesWithGoals > 0 ? Number(totalGoals / gamesWithGoals).toFixed(2) : '0.00';

        // Atualizar elementos
        const totalGamesEl = document.getElementById('totalGames');
        const avgGoalsEl = document.getElementById('avgGoals');
        const lastUpdateEl = document.getElementById('lastUpdate');

        if (totalGamesEl) totalGamesEl.textContent = DataLoader.formatNumber(totalGames);
        if (avgGoalsEl) avgGoalsEl.textContent = avgGoals;
        if (lastUpdateEl) lastUpdateEl.textContent = DataLoader.formatDate(new Date().toISOString());
    }
}

// Inicialização da página
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar animações
    const cards = document.querySelectorAll('.data-card, .series-card, .method-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });

    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Atualizar classe ativa na navegação
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// Exportar classes para uso global
// Gerenciador para estatísticas avançadas
class AdvancedStatsManager {
    static displayLastRounds(data, containerId) {
        const container = document.getElementById(containerId);
        if (!container || !data.estatisticas_avancadas?.ultimas_rodadas) return;
        
        container.innerHTML = '';
        
        const ultimasRodadas = data.estatisticas_avancadas.ultimas_rodadas;
        
        Object.keys(ultimasRodadas).forEach(rodadaNome => {
            const jogos = ultimasRodadas[rodadaNome];
            
            const rodadaDiv = document.createElement('div');
            rodadaDiv.className = 'last-round-section';
            
            const titulo = document.createElement('h4');
            titulo.textContent = rodadaNome;
            titulo.className = 'round-title';
            
            const jogosList = document.createElement('div');
            jogosList.className = 'games-list';
            
            jogos.forEach(jogo => {
                const jogoDiv = document.createElement('div');
                jogoDiv.className = 'game-result';
                jogoDiv.innerHTML = `
                    <span class="home-team">${jogo.strHomeTeam}</span>
                    <span class="score">${jogo.intHomeScore} x ${jogo.intAwayScore}</span>
                    <span class="away-team">${jogo.strAwayTeam}</span>
                `;
                jogosList.appendChild(jogoDiv);
            });
            
            rodadaDiv.appendChild(titulo);
            rodadaDiv.appendChild(jogosList);
            container.appendChild(rodadaDiv);
        });
    }
    
    static displayHomeAwayTable(data, containerId) {
        const container = document.getElementById(containerId);
        if (!container || !data.estatisticas_avancadas?.mandante_visitante) return;
        
        // Limpar container antes de adicionar nova tabela
        container.innerHTML = '';
        
        const mandanteVisitante = data.estatisticas_avancadas.mandante_visitante;
        
        const table = document.createElement('table');
        table.className = 'home-away-table';
        
        // Cabeçalho
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Time</th>
                <th colspan="6">Em Casa</th>
                <th colspan="6">Fora de Casa</th>
            </tr>
            <tr>
                <th></th>
                <th>J</th>
                <th>V</th>
                <th>E</th>
                <th>D</th>
                <th>Pts</th>
                <th>%</th>
                <th>J</th>
                <th>V</th>
                <th>E</th>
                <th>D</th>
                <th>Pts</th>
                <th>%</th>
            </tr>
        `;
        table.appendChild(thead);
        
        // Corpo
        const tbody = document.createElement('tbody');
        mandanteVisitante.forEach(time => {
            const row = document.createElement('tr');
            
            // Calcular derrotas e empates
            const empates_casa = time.jogos_casa - time.vitorias_casa - time.derrotas_casa;
            const empates_fora = time.jogos_fora - time.vitorias_fora - time.derrotas_fora;
            
            // Determinar classe de cor para aproveitamento
            const aproveitamentoCasaClass = time.aproveitamento_casa < 50 ? 'low' : 'good';
            const aproveitamentoForaClass = time.aproveitamento_fora < 50 ? 'low' : 'good';
            
            row.innerHTML = `
                <td class="team-name">${time.time}</td>
                <td>${time.jogos_casa}</td>
                <td>${time.vitorias_casa}</td>
                <td>${empates_casa}</td>
                <td>${time.derrotas_casa || 0}</td>
                <td>${time.pontos_casa}</td>
                <td class="percentage ${aproveitamentoCasaClass}">${time.aproveitamento_casa}%</td>
                <td>${time.jogos_fora}</td>
                <td>${time.vitorias_fora}</td>
                <td>${empates_fora}</td>
                <td>${time.derrotas_fora || 0}</td>
                <td>${time.pontos_fora}</td>
                <td class="percentage ${aproveitamentoForaClass}">${time.aproveitamento_fora}%</td>
            `;
            tbody.appendChild(row);
        });
        
        table.appendChild(tbody);
        container.appendChild(table);
    }
    
    static displayTeamForm(data, containerId) {
        const container = document.getElementById(containerId);
        if (!container || !data.estatisticas_avancadas?.times_stats) return;
        
        // Limpar container antes de adicionar novo conteúdo
        container.innerHTML = '';
        
        const timesStats = data.estatisticas_avancadas.times_stats;
        
        const formDiv = document.createElement('div');
        formDiv.className = 'team-form-grid';
        
        Object.keys(timesStats).forEach(time => {
            const stats = timesStats[time];
            const ultimos5 = stats.ultimos_5_jogos || [];
            
            const teamDiv = document.createElement('div');
            teamDiv.className = 'team-form-item';
            
            const teamName = document.createElement('h5');
            teamName.textContent = time;
            
            const formIndicators = document.createElement('div');
            formIndicators.className = 'form-indicators';
            
            // Se não há jogos recentes, mostrar indicador de "sem dados"
            if (ultimos5.length === 0) {
                const indicator = document.createElement('span');
                indicator.className = 'form-indicator no-data';
                indicator.textContent = '-';
                formIndicators.appendChild(indicator);
            } else {
                ultimos5.forEach(jogo => {
                    const indicator = document.createElement('span');
                    indicator.className = 'form-indicator';
                    
                    if (jogo.strHomeTeam === time) {
                        // Time jogou em casa
                        const golsPro = parseInt(jogo.intHomeScore);
                        const golsContra = parseInt(jogo.intAwayScore);
                        
                        if (golsPro > golsContra) {
                            indicator.textContent = 'V';
                            indicator.className += ' victory';
                        } else if (golsPro === golsContra) {
                            indicator.textContent = 'E';
                            indicator.className += ' draw';
                        } else {
                            indicator.textContent = 'D';
                            indicator.className += ' defeat';
                        }
                    } else {
                        // Time jogou fora
                        const golsPro = parseInt(jogo.intAwayScore);
                        const golsContra = parseInt(jogo.intHomeScore);
                        
                        if (golsPro > golsContra) {
                            indicator.textContent = 'V';
                            indicator.className += ' victory';
                        } else if (golsPro === golsContra) {
                            indicator.textContent = 'E';
                            indicator.className += ' draw';
                        } else {
                            indicator.textContent = 'D';
                            indicator.className += ' defeat';
                        }
                    }
                    
                    formIndicators.appendChild(indicator);
                });
            }
            
            teamDiv.appendChild(teamName);
            teamDiv.appendChild(formIndicators);
            formDiv.appendChild(teamDiv);
        });
        
        container.appendChild(formDiv);
    }
}

// Gerenciador de abas
class TabManager {
    static initialize() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabPanes = document.querySelectorAll('.tab-pane');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                
                // Remover classe active de todos os botões
                tabButtons.forEach(btn => btn.classList.remove('active'));
                
                // Adicionar classe active ao botão clicado
                button.classList.add('active');
                
                // Esconder todos os painéis
                tabPanes.forEach(pane => pane.classList.remove('active'));
                
                // Mostrar o painel correspondente
                const targetPane = document.getElementById(`${targetTab}-tab`);
                if (targetPane) {
                    targetPane.classList.add('active');
                }
                
                // Scroll suave para o topo das abas
                document.querySelector('.tabs-navigation').scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            });
        });
    }
}

// Função global para inicializar abas
function initializeTabs() {
    TabManager.initialize();
}

window.DataLoader = DataLoader;
window.ChartManager = ChartManager;
window.TableManager = TableManager;
window.NextGamesManager = NextGamesManager;
window.StatsManager = StatsManager;
window.AdvancedStatsManager = AdvancedStatsManager;
window.TabManager = TabManager;
window.initializeTabs = initializeTabs;
