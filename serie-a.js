// Gerenciador de dados da Série A
class SerieAManager {
    static async loadData() {
        try {
            console.log('=== INICIANDO CARREGAMENTO SÉRIE A ===');
            console.log('DataLoader disponível:', typeof DataLoader);
            console.log('DataLoader.loadData disponível:', typeof DataLoader.loadData);
            
            // Carregar dados processados para o site
            console.log('Tentando carregar dados da série-a...');
            const resultsData = await DataLoader.loadData('serie-a');
            
            console.log('Resultado do carregamento:', resultsData);
            
            if (!resultsData) {
                throw new Error('Erro ao carregar dados processados');
            }

            console.log('Dados carregados com sucesso:', resultsData);
            
            // Carregar dados de próximos jogos
            const proximosJogosData = await DataLoader.loadJSON('data/proximos_jogos_serie_a.json');
            
            // Processar e exibir os dados
            this.displayProbabilities(resultsData);
            this.displayClassification(resultsData);
            this.displayStatistics(resultsData);
            
            if (proximosJogosData) {
                this.displayUpcomingGames(proximosJogosData);
            }
            
            console.log('Série A carregada com sucesso!');
            
        } catch (error) {
            console.error('Erro ao carregar dados da Série A:', error);
            this.showError('Erro ao carregar dados da Série A. Tente recarregar a página.');
        }
    }

    static displayProbabilities(data) {
        console.log('=== EXIBINDO PROBABILIDADES SÉRIE A ===');
        console.log('Dados recebidos:', data);
        
        // Exibir probabilidades de título
        if (data.titulo) {
            console.log('Exibindo probabilidades de título:', data.titulo);
            this.populateTable('titleTableBody', data.titulo, 'titulo');
        }
        
        // Exibir probabilidades de Libertadores
        if (data.libertadores) {
            console.log('Exibindo probabilidades de Libertadores:', data.libertadores);
            this.populateTable('libertadoresTableBody', data.libertadores, 'libertadores');
        }
        
        // Exibir probabilidades de rebaixamento
        if (data.rebaixamento) {
            console.log('Exibindo probabilidades de rebaixamento:', data.rebaixamento);
            this.populateTable('rebaixamentoTableBody', data.rebaixamento, 'rebaixamento');
        }
    }

    static displayClassification(data) {
        if (data.classificacao) {
            this.populateClassificationTable('classificationTableBody', data.classificacao);
        }
    }

    static displayStatistics(data) {
        console.log('=== EXIBINDO ESTATÍSTICAS SÉRIE A ===');
        console.log('Dados recebidos:', data);
        
        if (data.estatisticas) {
            console.log('Exibindo estatísticas:', data.estatisticas);
            this.populateStatistics('home-away-table-container', data.estatisticas);
        }
    }

    static displayUpcomingGames(data) {
        console.log('=== EXIBINDO PRÓXIMOS JOGOS SÉRIE A ===');
        console.log('Dados recebidos:', data);
        
        if (data.proximos_jogos) {
            console.log('Exibindo próximos jogos:', data.proximos_jogos);
            this.populateUpcomingGames('nextGames', data.proximos_jogos);
        }
    }

    static populateTable(tableBodyId, data, type) {
        console.log(`=== POPULANDO TABELA ${tableBodyId} ===`);
        console.log('Tipo:', type);
        console.log('Dados:', data);
        
        const tableBody = document.getElementById(tableBodyId);
        console.log('Elemento encontrado:', tableBody);
        
        if (!tableBody) {
            console.log(`❌ Elemento ${tableBodyId} não encontrado`);
            return;
        }

        // Para probabilidades, ordenar por probabilidade (maior para menor)
        // Para classificação, manter ordem da classificação oficial
        let sortedData;
        
        if (type === 'titulo' || type === 'libertadores' || type === 'rebaixamento') {
            // Ordenar por probabilidade (maior para menor)
            sortedData = Object.entries(data)
                .map(([time, probabilidade]) => ({ time, probabilidade }))
                .sort((a, b) => b.probabilidade - a.probabilidade);
        } else {
            // Para outros tipos, manter ordem original
            sortedData = Object.entries(data)
                .map(([time, probabilidade]) => ({ time, probabilidade }));
        }

        console.log('Dados ordenados:', sortedData);

        tableBody.innerHTML = '';
        
        sortedData.forEach((item, index) => {
            const row = document.createElement('tr');
            const progressClass = DataLoader.getProgressBarClass(item.probabilidade);
            
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${item.time}</td>
                <td>
                    <div class="progress-container">
                        <div class="progress-bar ${progressClass}" style="width: ${item.probabilidade}%"></div>
                        <span class="progress-text">${DataLoader.formatPercentage(item.probabilidade)}</span>
                    </div>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
        
        console.log(`✅ Tabela ${tableBodyId} populada com ${sortedData.length} itens`);
    }

    static populateClassificationTable(tableBodyId, classificacao) {
        const tableBody = document.getElementById(tableBodyId);
        if (!tableBody) return;

        tableBody.innerHTML = '';
        
        classificacao.forEach((time, index) => {
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${time.time}</td>
                <td>${time.pontos}</td>
                <td>${time.jogos}</td>
                <td>${time.vitorias}</td>
                <td>${time.empates}</td>
                <td>${time.derrotas}</td>
                <td>${time.gols_pro}</td>
                <td>${time.gols_contra}</td>
                <td>${time.saldo_gols > 0 ? '+' : ''}${time.saldo_gols}</td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    static populateStatistics(containerId, estatisticas) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <h3><i class="fas fa-gamepad"></i> Total de Jogos</h3>
                    <p class="stat-value">${DataLoader.formatNumber(estatisticas.total_jogos)}</p>
                </div>
                <div class="stat-card">
                    <h3><i class="fas fa-futbol"></i> Média de Gols</h3>
                    <p class="stat-value">${estatisticas.media_gols}</p>
                </div>
                <div class="stat-card">
                    <h3><i class="fas fa-calculator"></i> Simulações</h3>
                    <p class="stat-value">${DataLoader.formatNumber(estatisticas.simulacoes)}</p>
                </div>
            </div>
        `;
    }

    static populateUpcomingGames(containerId, proximosJogos) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';
        
        Object.entries(proximosJogos).forEach(([time, jogos]) => {
            if (jogos && jogos.length > 0) {
                const timeSection = document.createElement('div');
                timeSection.className = 'team-games';
                
                timeSection.innerHTML = `
                    <h3><i class="fas fa-calendar"></i> ${time}</h3>
                    <div class="games-list">
                        ${jogos.map(jogo => this.createGameCard(jogo)).join('')}
                    </div>
                `;
                
                container.appendChild(timeSection);
            }
        });
    }

    static createGameCard(jogo) {
        const date = new Date(jogo.strTimestamp);
        const formattedDate = date.toLocaleDateString('pt-BR');
        const formattedTime = date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
        
        return `
            <div class="game-card">
                <div class="game-info">
                    <div class="game-teams">
                        <span class="home-team">${jogo.strHomeTeam}</span>
                        <span class="vs">vs</span>
                        <span class="away-team">${jogo.strAwayTeam}</span>
                    </div>
                    <div class="game-details">
                        <span class="game-date">${formattedDate}</span>
                        <span class="game-time">${formattedTime}</span>
                    </div>
                </div>
            </div>
        `;
    }

    static showError(message) {
        // Mostrar erro em todas as tabelas
        const tableBodies = ['titleTableBody', 'libertadoresTableBody', 'relegationTableBody', 'classificationTableBody'];
        
        tableBodies.forEach(id => {
            const tableBody = document.getElementById(id);
            if (tableBody) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="3" class="error-message">
                            <i class="fas fa-exclamation-triangle"></i>
                            ${message}
                        </td>
                    </tr>
                `;
            }
        });

        // Mostrar erro no container de estatísticas
        const statsContainer = document.getElementById('statisticsContainer');
        if (statsContainer) {
            statsContainer.innerHTML = `
                <div class="error-message">
                    <i class="fas fa-exclamation-triangle"></i>
                    ${message}
                </div>
            `;
        }
    }
}
