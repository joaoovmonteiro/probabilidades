#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA COMPLETO UNIFICADO - Campeonato Brasileiro 2025
Combina toda a lógica dos scripts em um arquivo único

Este script executa:
1. Busca de jogos da Série A e B
2. Busca de jogos faltantes
3. Busca de próximos jogos
4. Simulação estatística
5. Processamento para web

Autor: Sistema de Análise Brasileirão
Data: 2025
"""

import requests
import json
import time
import random
import numpy as np
import os
import statistics
from itertools import permutations
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timedelta

# =============================================================================
# CONFIGURAÇÕES GERAIS
# =============================================================================

API_KEY = "123"
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

# Times da Série A 2025
SERIE_A_TEAMS = {
    "Atlético Mineiro": {"idTeam": "134299", "strTeam": "Atlético Mineiro"},
    "Bahia": {"idTeam": "134293", "strTeam": "Bahia"},
    "Botafogo": {"idTeam": "134285", "strTeam": "Botafogo"},
    "Bragantino": {"idTeam": "134736", "strTeam": "Bragantino"},
    "Ceará": {"idTeam": "134744", "strTeam": "Ceará"},
    "Corinthians": {"idTeam": "134284", "strTeam": "Corinthians"},
    "Cruzeiro": {"idTeam": "134294", "strTeam": "Cruzeiro"},
    "Flamengo": {"idTeam": "134287", "strTeam": "Flamengo"},
    "Fluminense": {"idTeam": "134296", "strTeam": "Fluminense"},
    "Fortaleza": {"idTeam": "136186", "strTeam": "Fortaleza"},
    "Grêmio": {"idTeam": "134288", "strTeam": "Grêmio"},
    "Internacional": {"idTeam": "134281", "strTeam": "Internacional"},
    "Juventude": {"idTeam": "135887", "strTeam": "Juventude"},
    "Mirassol": {"idTeam": "141181", "strTeam": "Mirassol"},
    "Palmeiras": {"idTeam": "134465", "strTeam": "Palmeiras"},
    "Santos": {"idTeam": "134286", "strTeam": "Santos"},
    "São Paulo": {"idTeam": "134291", "strTeam": "São Paulo"},
    "Sport Club do Recife": {"idTeam": "136250", "strTeam": "Sport Club do Recife"},
    "Vasco da Gama": {"idTeam": "134282", "strTeam": "Vasco da Gama"},
    "Vitória": {"idTeam": "134280", "strTeam": "Vitória"},
}

# Times da Série B 2025
SERIE_B_TEAMS = {
    "Amazonas": {"idTeam": "145394", "strTeam": "Amazonas"},
    "América Mineiro": {"idTeam": "134742", "strTeam": "América Mineiro"},
    "Athletic Club-MG": {"idTeam": "147142", "strTeam": "Athletic Club-MG"},
    "Atlético Goianiense": {"idTeam": "134737", "strTeam": "Atlético Goianiense"},
    "Athletico Paranaense": {"idTeam": "134297", "strTeam": "Athletico Paranaense"},
    "Avaí": {"idTeam": "134738", "strTeam": "Avaí"},
    "Botafogo-SP": {"idTeam": "136830", "strTeam": "Botafogo-SP"},
    "Chapecoense": {"idTeam": "134464", "strTeam": "Chapecoense"},
    "CRB": {"idTeam": "135680", "strTeam": "CRB"},
    "Criciúma": {"idTeam": "134292", "strTeam": "Criciúma"},
    "Coritiba": {"idTeam": "134298", "strTeam": "Coritiba"},
    "Cuiabá": {"idTeam": "136831", "strTeam": "Cuiabá"},
    "Ferroviária": {"idTeam": "142270", "strTeam": "Ferroviária"},
    "Goiás": {"idTeam": "134295", "strTeam": "Goiás"},
    "Novorizontino": {"idTeam": "141182", "strTeam": "Novorizontino"},
    "Operário Ferroviário": {"idTeam": "136829", "strTeam": "Operário Ferroviário"},
    "Paysandu": {"idTeam": "135671", "strTeam": "Paysandu"},
    "Remo": {"idTeam": "137818", "strTeam": "Remo"},
    "Vila Nova": {"idTeam": "134734", "strTeam": "Vila Nova"},
    "Volta Redonda": {"idTeam": "138060", "strTeam": "Volta Redonda"},
}

# =============================================================================
# FUNÇÕES UTILITÁRIAS
# =============================================================================

def log_message(message, color=""):
    """Registra mensagem no console"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def carregar_cache(serie):
    """Carrega cache de jogos"""
    cache_file = Path(f"data/cache_jogos_{serie}.json")
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_cache(cache_data, serie):
    """Salva cache de jogos"""
    cache_file = Path(f"data/cache_jogos_{serie}.json")
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

# =============================================================================
# BUSCA DE JOGOS
# =============================================================================

def buscar_jogo_api(home, away, teams_info, serie):
    """Busca jogo específico na API"""
    home_name = teams_info[home]["strTeam"]
    away_name = teams_info[away]["strTeam"]
    key = f"{home_name}_vs_{away_name}"
    
    league = "Brazilian Serie A" if serie == "serie_a" else "Brazilian Serie B"
    league_filter = "Brazilian%20Serie%20A" if serie == "serie_a" else "Brazilian%20Serie%20B"
    
    # Primeira tentativa: busca por nome
    url = f"{BASE_URL}/searchevents.php?e={home_name}_vs_{away_name}&s=2025&f={league_filter}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            eventos = data.get("event", [])
            if eventos:
                eventos_filtrados = [jogo for jogo in eventos if jogo.get("strLeague") == league]
                if eventos_filtrados:
                    return eventos_filtrados
    except:
        pass
    
    # Segunda tentativa: busca por ID do time
    home_id = teams_info[home]["idTeam"]
    away_id = teams_info[away]["idTeam"]
    
    for team_id, team_name in [(home_id, home_name), (away_id, away_name)]:
        try:
            url_last = f"{BASE_URL}/eventslast.php?id={team_id}"
            response = requests.get(url_last)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                for jogo in results:
                    if (jogo.get("strHomeTeam") == home_name and 
                        jogo.get("strAwayTeam") == away_name and 
                        jogo.get("strLeague") == league):
                        return [jogo]
        except:
            continue
    
    return None

def buscar_jogos_serie(serie):
    """Busca todos os jogos de uma série"""
    log_message(f"Buscando jogos da {serie.upper()}...")
    
    teams_info = SERIE_A_TEAMS if serie == "serie_a" else SERIE_B_TEAMS
    team_names = list(teams_info.keys())
    
    cache = carregar_cache(serie)
    tabela = defaultdict(lambda: {
        "pontos": 0, "jogos": 0, "vitorias": 0,
        "empates": 0, "derrotas": 0, "gp": 0, "gc": 0
    })
    
    contador_jogos = defaultdict(int)
    total_combinations = len(list(permutations(team_names, 2)))
    
    for i, (home, away) in enumerate(permutations(team_names, 2)):
        log_message(f"Processando {i+1}/{total_combinations}: {home} vs {away}")
        
        jogos = buscar_jogo_api(home, away, teams_info, serie)
        if not jogos:
            continue
        
        for jogo in jogos:
            try:
                league = "Brazilian Serie A" if serie == "serie_a" else "Brazilian Serie B"
                if jogo.get("strLeague") != league:
                    continue
                
                g_casa = jogo.get("intHomeScore")
                g_fora = jogo.get("intAwayScore")
                casa = jogo.get("strHomeTeam")
                fora = jogo.get("strAwayTeam")
                
                if g_casa is None or g_fora is None:
                    continue
                
                g_casa, g_fora = int(g_casa), int(g_fora)
                
                # Atualizar contadores
                contador_jogos[casa] += 1
                contador_jogos[fora] += 1
                
                tabela[casa]["jogos"] += 1
                tabela[fora]["jogos"] += 1
                tabela[casa]["gp"] += g_casa
                tabela[casa]["gc"] += g_fora
                tabela[fora]["gp"] += g_fora
                tabela[fora]["gc"] += g_casa
                
                # Resultados
                if g_casa > g_fora:
                    tabela[casa]["pontos"] += 3
                    tabela[casa]["vitorias"] += 1
                    tabela[fora]["derrotas"] += 1
                elif g_fora > g_casa:
                    tabela[fora]["pontos"] += 3
                    tabela[fora]["vitorias"] += 1
                    tabela[casa]["derrotas"] += 1
                else:
                    tabela[casa]["pontos"] += 1
                    tabela[fora]["pontos"] += 1
                    tabela[casa]["empates"] += 1
                    tabela[fora]["empates"] += 1
                
                # Salvar no cache
                key = f"{casa}_vs_{fora}"
                if key not in cache:
                    cache[key] = []
                cache[key].append(jogo)
                
            except Exception as e:
                continue
        
        time.sleep(0.5)  # Rate limiting
    
    # Salvar cache
    salvar_cache(cache, serie)
    
    log_message(f"Busca da {serie.upper()} concluída!")
    return cache

def buscar_jogos_faltantes(serie):
    """Busca jogos faltantes por data"""
    log_message(f"Buscando jogos faltantes da {serie.upper()}...")
    
    cache = carregar_cache(serie)
    league = "Brazilian%20Serie%20A" if serie == "serie_a" else "Brazilian%20Serie%20B"
    
    # Buscar jogos dos últimos 30 dias
    data_inicio = datetime.now() - timedelta(days=30)
    data_fim = datetime.now() + timedelta(days=30)
    
    jogos_adicionados = 0
    
    data_atual = data_inicio
    while data_atual <= data_fim:
        data_str = data_atual.strftime("%Y-%m-%d")
        
        try:
            url = f"{BASE_URL}/eventsday.php?d={data_str}&l={league}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                
                for evento in events:
                    if evento.get('strHomeTeam') and evento.get('strAwayTeam'):
                        chave = f"{evento['strHomeTeam']}_vs_{evento['strAwayTeam']}"
                        
                        if chave not in cache:
                            cache[chave] = [evento]
                            jogos_adicionados += 1
                            log_message(f"  [+] Novo jogo: {evento['strHomeTeam']} vs {evento['strAwayTeam']}")
        
        except:
            pass
        
        time.sleep(1)
        data_atual += timedelta(days=1)
    
    if jogos_adicionados > 0:
        salvar_cache(cache, serie)
        log_message(f"Adicionados {jogos_adicionados} jogos faltantes da {serie.upper()}")
    
    return cache

def buscar_proximos_jogos(serie):
    """Busca próximos jogos de uma série"""
    log_message(f"Buscando próximos jogos da {serie.upper()}...")
    
    teams_info = SERIE_A_TEAMS if serie == "serie_a" else SERIE_B_TEAMS
    league = "Brazilian Serie A" if serie == "serie_a" else "Brazilian Serie B"
    
    proximos_jogos = {}
    
    for time_nome, info in teams_info.items():
        team_id = info["idTeam"]
        
        try:
            url = f"{BASE_URL}/eventsnext.php?id={team_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get("events", [])
                
                jogos_serie = []
                for evento in events:
                    if evento.get("strLeague") == league:
                        jogos_serie.append(evento)
                
                proximos_jogos[time_nome] = jogos_serie
                log_message(f"  {time_nome}: {len(jogos_serie)} jogos encontrados")
        
        except Exception as e:
            proximos_jogos[time_nome] = []
        
        time.sleep(0.5)
    
    # Salvar próximos jogos
    with open(f'data/proximos_jogos_{serie}.json', 'w', encoding='utf-8') as f:
        json.dump(proximos_jogos, f, ensure_ascii=False, indent=2)
    
    total_jogos = sum(len(jogos) for jogos in proximos_jogos.values())
    log_message(f"Total de próximos jogos da {serie.upper()}: {total_jogos}")
    
    return proximos_jogos

# =============================================================================
# SIMULAÇÃO ESTATÍSTICA
# =============================================================================

def calcular_estatisticas_retrospectivas(cache_jogos, serie):
    """Calcula estatísticas retrospectivas de cada time"""
    log_message(f"Calculando estatísticas da {serie.upper()}...")
    
    league = "Brazilian Serie A" if serie == "serie_a" else "Brazilian Serie B"
    stats_por_time = defaultdict(lambda: {
        'jogos': 0, 'gols_marcados': 0, 'gols_sofridos': 0, 'vitorias': 0, 
        'empates': 0, 'derrotas': 0, 'gols_por_jogo_marcados': [], 
        'gols_por_jogo_sofridos': [], 'pontos': 0
    })
    
    for chave_jogo, lista_jogos in cache_jogos.items():
        for jogo in lista_jogos:
            if (jogo.get('strLeague') == league and 
                jogo.get('intHomeScore') is not None and 
                jogo.get('intAwayScore') is not None):
                
                mandante = jogo.get('strHomeTeam')
                visitante = jogo.get('strAwayTeam')
                gols_mandante = int(jogo.get('intHomeScore'))
                gols_visitante = int(jogo.get('intAwayScore'))
                
                # Estatísticas do mandante
                stats_por_time[mandante]['jogos'] += 1
                stats_por_time[mandante]['gols_marcados'] += gols_mandante
                stats_por_time[mandante]['gols_sofridos'] += gols_visitante
                stats_por_time[mandante]['gols_por_jogo_marcados'].append(gols_mandante)
                stats_por_time[mandante]['gols_por_jogo_sofridos'].append(gols_visitante)
                
                # Estatísticas do visitante
                stats_por_time[visitante]['jogos'] += 1
                stats_por_time[visitante]['gols_marcados'] += gols_visitante
                stats_por_time[visitante]['gols_sofridos'] += gols_mandante
                stats_por_time[visitante]['gols_por_jogo_marcados'].append(gols_visitante)
                stats_por_time[visitante]['gols_por_jogo_sofridos'].append(gols_mandante)
                
                # Resultados
                if gols_mandante > gols_visitante:
                    stats_por_time[mandante]['vitorias'] += 1
                    stats_por_time[mandante]['pontos'] += 3
                    stats_por_time[visitante]['derrotas'] += 1
                elif gols_visitante > gols_mandante:
                    stats_por_time[visitante]['vitorias'] += 1
                    stats_por_time[visitante]['pontos'] += 3
                    stats_por_time[mandante]['derrotas'] += 1
                else:
                    stats_por_time[mandante]['empates'] += 1
                    stats_por_time[mandante]['pontos'] += 1
                    stats_por_time[visitante]['empates'] += 1
                    stats_por_time[visitante]['pontos'] += 1
    
    # Calcular médias e desvios
    for time, stats in stats_por_time.items():
        if stats['jogos'] > 0:
            stats['media_gols_marcados'] = statistics.mean(stats['gols_por_jogo_marcados'])
            stats['media_gols_sofridos'] = statistics.mean(stats['gols_por_jogo_sofridos'])
            stats['desvio_gols_marcados'] = statistics.stdev(stats['gols_por_jogo_marcados']) if len(stats['gols_por_jogo_marcados']) > 1 else 0
            stats['desvio_gols_sofridos'] = statistics.stdev(stats['gols_por_jogo_sofridos']) if len(stats['gols_por_jogo_sofridos']) > 1 else 0
    
    return stats_por_time

def analisar_jogos_futuros(cache_jogos, serie):
    """Analisa jogos futuros do cache"""
    log_message(f"Analisando jogos futuros da {serie.upper()}...")
    
    league = "Brazilian Serie A" if serie == "serie_a" else "Brazilian Serie B"
    jogos_futuros = []
    
    for chave_jogo, lista_jogos in cache_jogos.items():
        for jogo in lista_jogos:
            if (jogo.get('intHomeScore') is None and 
                jogo.get('intAwayScore') is None and 
                jogo.get('strLeague') == league):
                
                jogos_futuros.append({
                    'data': jogo.get('dateEvent'),
                    'mandante': jogo.get('strHomeTeam'),
                    'visitante': jogo.get('strAwayTeam'),
                    'rodada': jogo.get('intRound', '0')
                })
    
    log_message(f"Encontrados {len(jogos_futuros)} jogos futuros")
    return jogos_futuros

def simular_resultado_jogo(time_a, time_b, stats_por_time):
    """Simula o resultado de um jogo entre dois times"""
    stats_a = stats_por_time[time_a]
    stats_b = stats_por_time[time_b]
    
    # Simular gols usando distribuição Poisson
    lambda_a = max(0.1, stats_a['media_gols_marcados'])
    lambda_b = max(0.1, stats_b['media_gols_marcados'])
    
    # Adicionar ruído baseado no desvio padrão
    noise_a = random.gauss(0, stats_a['desvio_gols_marcados'] * 0.5)
    noise_b = random.gauss(0, stats_b['desvio_gols_sofridos'] * 0.5)
    
    gols_a = max(0, int(np.random.poisson(lambda_a) + noise_a))
    gols_b = max(0, int(np.random.poisson(lambda_b) + noise_b))
    
    return gols_a, gols_b

def simular_campeonato(jogos_futuros, stats_por_time, num_simulacoes=300000):
    """Executa simulação do campeonato"""
    log_message(f"Executando {num_simulacoes:,} simulações...")
    
    resultados = {
        'posicoes_finais': defaultdict(list),
        'pontos_finais': defaultdict(list),
        'libertadores': defaultdict(int),
        'rebaixamento': defaultdict(int),
        'acesso_serie_a': defaultdict(int)  # Para Série B
    }
    
    for simulacao in range(num_simulacoes):
        if simulacao % 30000 == 0:
            log_message(f"  Simulação {simulacao:,}/{num_simulacoes:,}")
        
        # Pontuação inicial
        pontos_atuais = {time: stats['pontos'] for time, stats in stats_por_time.items()}
        
        # Simular cada jogo futuro
        for jogo in jogos_futuros:
            gols_mandante, gols_visitante = simular_resultado_jogo(
                jogo['mandante'], jogo['visitante'], stats_por_time
            )
            
            # Atualizar pontuação
            if gols_mandante > gols_visitante:
                pontos_atuais[jogo['mandante']] += 3
            elif gols_visitante > gols_mandante:
                pontos_atuais[jogo['visitante']] += 3
            else:
                pontos_atuais[jogo['mandante']] += 1
                pontos_atuais[jogo['visitante']] += 1
        
        # Ordenar por pontos
        classificacao = sorted(pontos_atuais.items(), key=lambda x: x[1], reverse=True)
        
        # Armazenar resultados
        for pos, (time, pontos) in enumerate(classificacao, 1):
            resultados['posicoes_finais'][time].append(pos)
            resultados['pontos_finais'][time].append(pontos)
            
            # Libertadores (6 primeiros) ou Acesso à Série A (4 primeiros)
            if pos <= 6:
                resultados['libertadores'][time] += 1
            if pos <= 4:
                resultados['acesso_serie_a'][time] += 1
            
            # Rebaixamento (4 últimos)
            if pos >= 17:
                resultados['rebaixamento'][time] += 1
    
    # Converter contadores para probabilidades
    for time in stats_por_time.keys():
        resultados['libertadores'][time] = resultados['libertadores'][time] / num_simulacoes * 100
        resultados['rebaixamento'][time] = resultados['rebaixamento'][time] / num_simulacoes * 100
        resultados['acesso_serie_a'][time] = resultados['acesso_serie_a'][time] / num_simulacoes * 100
    
    return resultados

def executar_simulacao(serie):
    """Executa simulação completa para uma série"""
    log_message(f"Iniciando simulação da {serie.upper()}...")
    
    # Carregar dados
    cache_jogos = carregar_cache(serie)
    
    # Analisar jogos futuros
    jogos_futuros = analisar_jogos_futuros(cache_jogos, serie)
    
    # Calcular estatísticas retrospectivas
    stats_por_time = calcular_estatisticas_retrospectivas(cache_jogos, serie)
    
    # Executar simulação
    resultados = simular_campeonato(jogos_futuros, stats_por_time)
    
    # Salvar resultados
    with open(f'data/resultados_simulacao_{serie}.json', 'w', encoding='utf-8') as f:
        # Converter numpy arrays para listas
        resultados_serializaveis = {}
        for key, value in resultados.items():
            if isinstance(value, dict):
                resultados_serializaveis[key] = {}
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list):
                        resultados_serializaveis[key][subkey] = subvalue
                    else:
                        resultados_serializaveis[key][subkey] = subvalue
            else:
                resultados_serializaveis[key] = value
        
        json.dump(resultados_serializaveis, f, ensure_ascii=False, indent=2)
    
    log_message(f"Simulação da {serie.upper()} concluída!")
    return resultados

# =============================================================================
# PROCESSAMENTO PARA WEB
# =============================================================================

def calcular_classificacao_real(cache_data, serie):
    """Calcula classificação real baseada nos jogos do cache"""
    league = "Brazilian Serie A" if serie == "serie_a" else "Brazilian Serie B"
    times_stats = defaultdict(lambda: {
        'jogos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0,
        'gols_pro': 0, 'gols_contra': 0, 'pontos': 0
    })
    
    # Processar todos os jogos do cache
    for jogos in cache_data.values():
        if isinstance(jogos, list):
            for jogo in jogos:
                if (jogo.get('intHomeScore') is not None and 
                    jogo.get('intAwayScore') is not None and
                    jogo.get('strLeague') == league and
                    jogo.get('strHomeTeam') and 
                    jogo.get('strAwayTeam')):
                    
                    home_team = jogo['strHomeTeam']
                    away_team = jogo['strAwayTeam']
                    home_score = int(jogo['intHomeScore'])
                    away_score = int(jogo['intAwayScore'])
                    
                    # Atualizar estatísticas
                    times_stats[home_team]['jogos'] += 1
                    times_stats[home_team]['gols_pro'] += home_score
                    times_stats[home_team]['gols_contra'] += away_score
                    
                    times_stats[away_team]['jogos'] += 1
                    times_stats[away_team]['gols_pro'] += away_score
                    times_stats[away_team]['gols_contra'] += home_score
                    
                    # Resultados
                    if home_score > away_score:
                        times_stats[home_team]['vitorias'] += 1
                        times_stats[home_team]['pontos'] += 3
                        times_stats[away_team]['derrotas'] += 1
                    elif away_score > home_score:
                        times_stats[away_team]['vitorias'] += 1
                        times_stats[away_team]['pontos'] += 3
                        times_stats[home_team]['derrotas'] += 1
                    else:
                        times_stats[home_team]['empates'] += 1
                        times_stats[home_team]['pontos'] += 1
                        times_stats[away_team]['empates'] += 1
                        times_stats[away_team]['pontos'] += 1
    
    # Converter para lista e ordenar
    classificacao = []
    for time, stats in times_stats.items():
        if stats['jogos'] > 0:
            classificacao.append({
                'time': time,
                'pontos': stats['pontos'],
                'jogos': stats['jogos'],
                'vitorias': stats['vitorias'],
                'empates': stats['empates'],
                'derrotas': stats['derrotas'],
                'gols_pro': stats['gols_pro'],
                'gols_contra': stats['gols_contra'],
                'saldo_gols': stats['gols_pro'] - stats['gols_contra']
            })
    
    # Ordenar por pontos
    classificacao.sort(key=lambda x: (x['pontos'], x['vitorias'], x['saldo_gols']), reverse=True)
    
    return classificacao

def encontrar_proxima_rodada(cache_data, serie):
    """Encontra a próxima rodada"""
    league = "Brazilian Serie A" if serie == "serie_a" else "Brazilian Serie B"
    rodadas_jogadas = set()
    rodadas_pendentes = set()
    
    for jogos in cache_data.values():
        if isinstance(jogos, list):
            for jogo in jogos:
                if jogo.get('intRound') and jogo.get('strLeague') == league:
                    rodada = int(jogo['intRound'])
                    
                    if (jogo.get('intHomeScore') is not None and 
                        jogo.get('intAwayScore') is not None):
                        rodadas_jogadas.add(rodada)
                    else:
                        rodadas_pendentes.add(rodada)
    
    ultima_rodada_jogada = max(rodadas_jogadas) if rodadas_jogadas else 0
    proximas_rodadas = [r for r in rodadas_pendentes if r > ultima_rodada_jogada]
    proxima_rodada = min(proximas_rodadas) if proximas_rodadas else ultima_rodada_jogada + 1
    
    return proxima_rodada

def processar_dados_web(serie):
    """Processa dados para o site web"""
    log_message(f"Processando dados web da {serie.upper()}...")
    
    # Carregar dados de simulação
    with open(f'data/resultados_simulacao_{serie}.json', 'r', encoding='utf-8') as f:
        simulacao_data = json.load(f)
    
    # Carregar dados de cache
    cache_data = carregar_cache(serie)
    
    # Processar dados
    dados_web = {
        'titulo': {},
        'libertadores': {},
        'rebaixamento': {},
        'classificacao': [],
        'estatisticas': {},
        'proximos_jogos': {},
        'ultima_atualizacao': datetime.now().isoformat()
    }
    
    # Calcular probabilidades de título
    if 'posicoes_finais' in simulacao_data:
        for time, posicoes in simulacao_data['posicoes_finais'].items():
            if posicoes:
                primeiro_lugar = sum(1 for pos in posicoes if pos == 1)
                probabilidade = (primeiro_lugar / len(posicoes)) * 100
                dados_web['titulo'][time] = round(probabilidade, 1)
    
    # Dados de Libertadores/Acesso
    if 'libertadores' in simulacao_data:
        dados_web['libertadores'] = simulacao_data['libertadores']
    
    if 'acesso_serie_a' in simulacao_data:
        dados_web['acesso_serie_a'] = simulacao_data['acesso_serie_a']
    
    # Dados de Rebaixamento
    if 'rebaixamento' in simulacao_data:
        dados_web['rebaixamento'] = simulacao_data['rebaixamento']
    
    # Classificação
    dados_web['classificacao'] = calcular_classificacao_real(cache_data, serie)
    
    # Estatísticas
    total_jogos = 0
    total_gols = 0
    
    for jogos in cache_data.values():
        if isinstance(jogos, list):
            for jogo in jogos:
                if jogo.get('intHomeScore') is not None and jogo.get('intAwayScore') is not None:
                    total_jogos += 1
                    gols_casa = int(jogo['intHomeScore'])
                    gols_fora = int(jogo['intAwayScore'])
                    total_gols += gols_casa + gols_fora
    
    dados_web['estatisticas'] = {
        'total_jogos': total_jogos,
        'media_gols': round(total_gols / total_jogos, 2) if total_jogos > 0 else 0,
        'simulacoes': 300000
    }
    
    # Próximos jogos
    try:
        with open(f'data/proximos_jogos_{serie}.json', 'r', encoding='utf-8') as f:
            proximos_data = json.load(f)
        
        proxima_rodada = encontrar_proxima_rodada(cache_data, serie)
        dados_web['proximos_jogos'] = proximos_data
        dados_web['proxima_rodada'] = proxima_rodada
        
    except FileNotFoundError:
        dados_web['proximos_jogos'] = {}
        dados_web['proxima_rodada'] = None
    
    # Salvar dados processados
    with open(f'data/web_{serie}.json', 'w', encoding='utf-8') as f:
        json.dump(dados_web, f, ensure_ascii=False, indent=2)
    
    log_message(f"Dados web da {serie.upper()} processados!")
    return dados_web

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def executar_sistema_completo():
    """Executa todo o sistema unificado"""
    log_message("=" * 80)
    log_message("SISTEMA COMPLETO UNIFICADO - CAMPEONATO BRASILEIRO 2025")
    log_message("=" * 80)
    
    # Verificar se estamos no diretório correto
    if not Path("data").exists():
        log_message("ERRO: Diretório 'data' não encontrado!")
        log_message("Execute este script na raiz do projeto.")
        return False
    
    # Criar diretório data se não existir
    Path("data").mkdir(exist_ok=True)
    
    try:
        # 1. Buscar jogos da Série A
        log_message("\n1. BUSCANDO JOGOS DA SÉRIE A")
        log_message("-" * 40)
        cache_serie_a = buscar_jogos_serie("serie_a")
        
        # 2. Buscar jogos da Série B
        log_message("\n2. BUSCANDO JOGOS DA SÉRIE B")
        log_message("-" * 40)
        cache_serie_b = buscar_jogos_serie("serie_b")
        
        # 3. Buscar jogos faltantes
        log_message("\n3. BUSCANDO JOGOS FALTANTES")
        log_message("-" * 40)
        buscar_jogos_faltantes("serie_a")
        buscar_jogos_faltantes("serie_b")
        
        # 4. Buscar próximos jogos
        log_message("\n4. BUSCANDO PRÓXIMOS JOGOS")
        log_message("-" * 40)
        buscar_proximos_jogos("serie_a")
        buscar_proximos_jogos("serie_b")
        
        # 5. Executar simulações
        log_message("\n5. EXECUTANDO SIMULAÇÕES")
        log_message("-" * 40)
        executar_simulacao("serie_a")
        executar_simulacao("serie_b")
        
        # 6. Processar dados para web
        log_message("\n6. PROCESSANDO DADOS PARA WEB")
        log_message("-" * 40)
        processar_dados_web("serie_a")
        processar_dados_web("serie_b")
        
        log_message("\n" + "=" * 80)
        log_message("SISTEMA COMPLETO EXECUTADO COM SUCESSO!")
        log_message("=" * 80)
        log_message("Arquivos gerados:")
        log_message("- data/cache_jogos_serie_a.json")
        log_message("- data/cache_jogos_serie_b.json")
        log_message("- data/proximos_jogos_serie_a.json")
        log_message("- data/proximos_jogos_serie_b.json")
        log_message("- data/resultados_simulacao_serie_a.json")
        log_message("- data/resultados_simulacao_serie_b.json")
        log_message("- data/web_serie_a.json")
        log_message("- data/web_serie_b.json")
        log_message("=" * 80)
        
        return True
        
    except Exception as e:
        log_message(f"ERRO durante execução: {e}")
        return False

def main():
    """Função principal"""
    print("Sistema Completo Unificado - Campeonato Brasileiro 2025")
    print("Este script executa toda a análise em um arquivo único")
    print()
    
    try:
        sucesso = executar_sistema_completo()
        if sucesso:
            print("\n✅ Execução concluída com sucesso!")
            print("📊 Dados processados e salvos na pasta 'data/'")
            print("🌐 Execute 'python server.py' para visualizar no navegador")
        else:
            print("\n❌ Execução falhou!")
            
    except KeyboardInterrupt:
        print("\n⚠️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
