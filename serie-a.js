// Script específico para a página da Série A
class SerieAManager {
    static async loadData() {
        try {
            console.log('Carregando dados da Série A...');
            
            // Carregar dados processados para o site
            const resultsData = await DataLoader.loadJSON('data/web_serie_a.json');
            
            if (!resultsData) {
                throw new Error('Erro ao carregar dados processados');
            }

            // Processar e exibir dados
            this.processAndDisplayData(resultsData);

        } catch (error) {
            console.error('Erro ao carregar dados da Série A:', error);
            this.showError('Erro ao carregar dados da Série A: ' + error.message);
        }
    }

    static processAndDisplayData(data) {
        // Destruir gráficos existentes antes de criar novos
        ChartManager.destroyAllCharts();
        
        // Verificar qual página estamos e exibir apenas o conteúdo relevante
        const currentPage = window.location.pathname;
        
        if (currentPage.includes('probabilidades')) {
            this.displayTitleProbabilities(data);
            this.displayLibertadoresProbabilities(data);
            this.displayRelegationProbabilities(data);
        } else if (currentPage.includes('classificacao')) {
            this.displayCurrentClassification(data);
        } else if (currentPage.includes('proximos-jogos')) {
            this.displayNextGames(data);
        } else if (currentPage.includes('estatisticas')) {
            this.displayAdvancedStats(data);
        } else {
            // Página antiga com abas - exibir tudo
            this.displayTitleProbabilities(data);
            this.displayLibertadoresProbabilities(data);
            this.displayRelegationProbabilities(data);
            this.displayCurrentClassification(data);
            this.displayStatistics(data);
            this.displayNextGames(data);
            this.displayAdvancedStats(data);
        }
    }

    static displayTitleProbabilities(data) {
        // Usar dados de título já calculados
        if (data.titulo) {
            const titleData = Object.entries(data.titulo)
                .map(([team, probability]) => ({ team, probability }))
                .sort((a, b) => b.probability - a.probability)
                .slice(0, 10); // Top 10
            
            TableManager.createTitleTable(titleData, 'titleTableBody');
        }
    }

    static displayLibertadoresProbabilities(data) {
        if (data.libertadores) {
            // Converter dados para array ordenado
            const libertadoresData = Object.entries(data.libertadores)
                .map(([team, probability]) => ({ team, probability }))
                .sort((a, b) => b.probability - a.probability)
                .slice(0, 10); // Top 10

            // Criar tabela
            TableManager.createProbabilityTable(libertadoresData, 'libertadoresTableBody', 'probability');

            // Gráfico removido conforme solicitado
        }
    }

    static displayRelegationProbabilities(data) {
        if (data.rebaixamento) {
            // Converter dados para array ordenado
            const relegationData = Object.entries(data.rebaixamento)
                .map(([team, probability]) => ({ team, probability }))
                .sort((a, b) => b.probability - a.probability)
                .slice(0, 8); // Top 8 com maior risco

            // Criar tabela
            TableManager.createProbabilityTable(relegationData, 'rebaixamentoTableBody', 'probability');

            // Gráfico removido conforme solicitado
        }
    }

    static displayCurrentClassification(data) {
        // Usar dados de classificação já processados
        if (data.classificacao) {
            TableManager.createClassificationTable(data.classificacao, 'classificationTableBody');
        }
    }
    
    static displayStatistics(data) {
        // Removido - estatísticas detalhadas não são mais exibidas
    }
    
    static displayNextGames(data) {
        // Reformular próximos jogos com probabilidades estimadas
        const container = document.getElementById('nextGames');
        if (!container) return;

        if (data.proximos_jogos && Object.keys(data.proximos_jogos).length > 0) {
            NextGamesManager.displayNextGamesWithProbabilities(data.proximos_jogos, container, data.proxima_rodada);
        } else {
            container.innerHTML = '<p class="error">Nenhum próximo jogo encontrado</p>';
        }
    }


    static showError(message) {
        // Mostrar mensagem de erro em todas as seções
        const sections = ['titleTableBody', 'libertadoresTableBody', 'rebaixamentoTableBody', 'classificationTableBody'];
        
        sections.forEach(sectionId => {
            const element = document.getElementById(sectionId);
            if (element) {
                element.innerHTML = `<tr><td colspan="4" class="error">${message}</td></tr>`;
            }
        });

        // Mostrar erro nos próximos jogos
        const nextGamesElement = document.getElementById('nextGames');
        if (nextGamesElement) {
            nextGamesElement.innerHTML = `<p class="error">${message}</p>`;
        }
    }
    
    static displayAdvancedStats(data) {
        // Exibir tabela casa/fora
        AdvancedStatsManager.displayHomeAwayTable(data, 'home-away-table-container');
        
        // Exibir forma dos times
        AdvancedStatsManager.displayTeamForm(data, 'team-form-container');
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    SerieAManager.loadData();
});

// Exportar para uso global
window.SerieAManager = SerieAManager;
