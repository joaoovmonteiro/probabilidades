#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN.PY - Sistema Completo de Analise e Simulacao
Campeonato Brasileiro - Series A e B 2025

Este script executa todo o pipeline de analise:
1. Mantém dados existentes (nunca limpa automaticamente)
2. Executa sistema completo unificado (todos os processos em um arquivo)
3. Modo agendador automático (execução diária às 6h, sem parar)
4. Inicia servidor web (opcional)

O sistema unificado inclui:
- Busca de jogos da Serie A e B
- Busca de jogos faltantes
- Busca de próximos jogos
- Simulação estatística (300.000 simulações)
- Processamento para web

Uso:
    python main.py              # Modo agendador automático (executa 1x/dia, sem parar)
    python main.py --clean      # Executa limpando dados antigos
    python main.py -c           # Mesmo que --clean
    python main.py --server     # Executa e inicia servidor web
    python main.py -s           # Mesmo que --server
    python main.py --agendador  # Modo agendador (executa automaticamente 1x/dia)
    python main.py -a           # Mesmo que --agendador
    python main.py --status     # Mostra status do agendador
    python main.py --clean --server  # Limpa dados + executa + servidor

Autor: Sistema de Analise Brasileirao
Data: 2025
"""

import os
import sys
import time
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta

# Configurações
DATA_DIR = Path("data")
LOG_FILE = "execucao_log.txt"
AGENDADOR_FILE = "agendador_status.json"
HORA_EXECUCAO = 6  # 6:00 da manhã

# Cores para output (Windows)
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log_message(message, color=Colors.BLUE):
    """Registra mensagem no log e no console"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    
    # Remover cores no Windows para evitar problemas de encoding
    if os.name == 'nt':
        print(log_msg)
    else:
        print(f"{color}{log_msg}{Colors.END}")
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

def limpar_dados_antigos():
    """Remove todos os arquivos JSON de dados"""
    log_message("[LIMPEZA] Limpando dados antigos...", Colors.YELLOW)
    
    arquivos_para_remover = [
        "cache_jogos_serie_a.json",
        "cache_jogos_serie_b.json", 
        "proximos_jogos_serie_a.json",
        "proximos_jogos_serie_b.json",
        "resultados_simulacao_serie_a.json",
        "resultados_simulacao_serie_b.json"
    ]
    
    removidos = 0
    for arquivo in arquivos_para_remover:
        arquivo_path = DATA_DIR / arquivo
        if arquivo_path.exists():
            arquivo_path.unlink()
            log_message(f"  [OK] Removido: {arquivo}", Colors.GREEN)
            removidos += 1
        else:
            log_message(f"  [INFO] Nao encontrado: {arquivo}")
    
    log_message(f"[RESUMO] Total de arquivos removidos: {removidos}", Colors.GREEN)

def executar_script(nome_script, descricao):
    """Executa um script Python e captura o output"""
    log_message(f"[EXECUTANDO] {descricao}", Colors.BLUE)
    
    script_path = SCRIPTS_DIR / nome_script
    
    if not script_path.exists():
        log_message(f"[ERRO] Script nao encontrado: {script_path}", Colors.RED)
        return False
    
    try:
        # Executar script
        inicio = time.time()
        # Configurar encoding para Windows
        encoding = 'utf-8' if os.name != 'nt' else 'cp1252'
        
        resultado = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=".",  # Executar da raiz do projeto
            capture_output=True,
            text=True,
            encoding=encoding,
            errors='ignore'
        )
        fim = time.time()
        duracao = fim - inicio
        
        if resultado.returncode == 0:
            log_message(f"[OK] Concluido: {descricao} ({duracao:.1f}s)", Colors.GREEN)
            
            # Salvar output do script no log
            if resultado.stdout:
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(f"\n--- OUTPUT {descricao} ---\n")
                    f.write(resultado.stdout)
                    f.write("\n--- FIM OUTPUT ---\n\n")
            
            return True
        else:
            log_message(f"[ERRO] Falha em {descricao}: {resultado.stderr}", Colors.RED)
            return False
            
    except Exception as e:
        log_message(f"[EXCECAO] Erro em {descricao}: {str(e)}", Colors.RED)
        return False

def verificar_arquivos_gerados():
    """Verifica se os arquivos principais foram gerados"""
    log_message("[VERIFICACAO] Verificando arquivos gerados...", Colors.BLUE)
    
    arquivos_esperados = [
        "cache_jogos_serie_a.json",
        "cache_jogos_serie_b.json",
        "proximos_jogos_serie_a.json", 
        "proximos_jogos_serie_b.json",
        "resultados_simulacao_serie_a.json",
        "resultados_simulacao_serie_b.json"
    ]
    
    gerados = 0
    for arquivo in arquivos_esperados:
        arquivo_path = DATA_DIR / arquivo
        if arquivo_path.exists():
            tamanho = arquivo_path.stat().st_size
            log_message(f"  [OK] {arquivo} ({tamanho:,} bytes)", Colors.GREEN)
            gerados += 1
        else:
            log_message(f"  [FALTA] {arquivo} - NAO GERADO", Colors.RED)
    
    log_message(f"[RESUMO] Arquivos gerados: {gerados}/{len(arquivos_esperados)}", 
                Colors.GREEN if gerados == len(arquivos_esperados) else Colors.YELLOW)
    
    return gerados == len(arquivos_esperados)

def gerar_relatorio_final():
    """Gera um relatório final com estatísticas"""
    log_message("[RELATORIO] Gerando relatorio final...", Colors.BLUE)
    
    relatorio = {
        "data_execucao": datetime.now().isoformat(),
        "arquivos_gerados": [],
        "tamanhos": {},
        "status": "SUCESSO"
    }
    
    # Verificar arquivos gerados
    for arquivo in DATA_DIR.glob("*.json"):
        tamanho = arquivo.stat().st_size
        relatorio["arquivos_gerados"].append(arquivo.name)
        relatorio["tamanhos"][arquivo.name] = tamanho
    
    # Salvar relatório
    with open("relatorio_execucao.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    log_message("[OK] Relatorio salvo em: relatorio_execucao.json", Colors.GREEN)
    
    return relatorio

def carregar_status_agendador():
    """Carrega status do agendador"""
    if Path(AGENDADOR_FILE).exists():
        try:
            with open(AGENDADOR_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"ultima_execucao": None, "execucoes": []}
    return {"ultima_execucao": None, "execucoes": []}

def salvar_status_agendador(status):
    """Salva status do agendador"""
    with open(AGENDADOR_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)

def ja_executou_hoje():
    """Verifica se já executou hoje"""
    status = carregar_status_agendador()
    
    if not status.get("ultima_execucao"):
        return False
    
    try:
        ultima_execucao = datetime.fromisoformat(status["ultima_execucao"])
        hoje = datetime.now().date()
        ultima_data = ultima_execucao.date()
        
        return ultima_data == hoje
    except:
        return False

def calcular_proxima_execucao():
    """Calcula quando será a próxima execução"""
    agora = datetime.now()
    
    # Se já passou da hora de hoje, executa amanhã
    if agora.hour >= HORA_EXECUCAO:
        proxima = agora.replace(hour=HORA_EXECUCAO, minute=0, second=0, microsecond=0) + timedelta(days=1)
    else:
        # Executa hoje na hora programada
        proxima = agora.replace(hour=HORA_EXECUCAO, minute=0, second=0, microsecond=0)
    
    return proxima

def aguardar_proxima_execucao():
    """Aguarda até a próxima execução programada"""
    proxima = calcular_proxima_execucao()
    agora = datetime.now()
    
    tempo_espera = (proxima - agora).total_seconds()
    
    log_message(f"[AGENDADOR] Próxima execução: {proxima.strftime('%Y-%m-%d %H:%M:%S')}", Colors.BLUE)
    log_message(f"[AGENDADOR] Aguardando {tempo_espera/3600:.1f} horas...", Colors.BLUE)
    
    # Aguardar em intervalos de 1 hora para verificar se deve parar
    while tempo_espera > 0:
        if tempo_espera > 3600:  # Mais de 1 hora
            time.sleep(3600)  # Aguardar 1 hora
            tempo_espera -= 3600
        else:
            time.sleep(tempo_espera)  # Aguardar o tempo restante
            break

def executar_sistema_completo():
    """Executa o sistema completo usando script unificado"""
    log_message("[SISTEMA] Iniciando execução completa...", Colors.BLUE)
    
    # Executar script unificado
    if executar_script("sistema_completo.py", "Sistema Completo Unificado"):
        log_message("[OK] Sistema unificado executado com sucesso", Colors.GREEN)
        
        # Verificar resultados
        todos_gerados = verificar_arquivos_gerados()
        
        # Atualizar status do agendador
        agora = datetime.now()
        status = carregar_status_agendador()
        status["ultima_execucao"] = agora.isoformat()
        status["execucoes"].append({
            "data": agora.isoformat(),
            "sucesso": todos_gerados,
            "sucessos": 1 if todos_gerados else 0,
            "falhas": 0 if todos_gerados else 1
        })
        
        # Manter apenas últimas 30 execuções
        if len(status["execucoes"]) > 30:
            status["execucoes"] = status["execucoes"][-30:]
        
        salvar_status_agendador(status)
        
        return todos_gerados
    else:
        log_message("[ERRO] Falha na execução do sistema unificado", Colors.RED)
        
        # Atualizar status do agendador com falha
        agora = datetime.now()
        status = carregar_status_agendador()
        status["ultima_execucao"] = agora.isoformat()
        status["execucoes"].append({
            "data": agora.isoformat(),
            "sucesso": False,
            "sucessos": 0,
            "falhas": 1
        })
        
        salvar_status_agendador(status)
        
        return False

def modo_agendador():
    """Modo agendador - executa automaticamente uma vez por dia"""
    log_message("[AGENDADOR] Modo agendador ativado", Colors.BLUE)
    log_message("[AGENDADOR] Pressione Ctrl+C para parar", Colors.YELLOW)
    
    try:
        while True:
            agora = datetime.now()
            
            # Verificar se é hora de executar
            if agora.hour == HORA_EXECUCAO and agora.minute == 0:
                log_message("[AGENDADOR] Hora de execução atingida!", Colors.GREEN)
                
                # Verificar se já executou hoje
                if not ja_executou_hoje():
                    log_message("[AGENDADOR] Executando sistema...", Colors.BLUE)
                    
                    # Executar sistema completo
                    sucesso = executar_sistema_completo()
                    
                    if sucesso:
                        log_message("[AGENDADOR] Execução concluída com sucesso!", Colors.GREEN)
                    else:
                        log_message("[AGENDADOR] Execução falhou!", Colors.RED)
                else:
                    log_message("[AGENDADOR] Sistema já foi executado hoje", Colors.YELLOW)
                
                # Aguardar até amanhã
                aguardar_proxima_execucao()
            else:
                # Aguardar 1 minuto e verificar novamente
                time.sleep(60)
                
    except KeyboardInterrupt:
        log_message("[AGENDADOR] Modo agendador interrompido pelo usuário", Colors.YELLOW)
    except Exception as e:
        log_message(f"[AGENDADOR] Erro no modo agendador: {str(e)}", Colors.RED)

def mostrar_status_agendador():
    """Mostra status do agendador"""
    status = carregar_status_agendador()
    
    print("\n" + "="*60)
    print("STATUS DO AGENDADOR DIARIO")
    print("="*60)
    
    if status.get("ultima_execucao"):
        ultima = datetime.fromisoformat(status["ultima_execucao"])
        print(f"Ultima execucao: {ultima.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if ja_executou_hoje():
            print("Status: [OK] Ja executou hoje")
        else:
            print("Status: [AGUARDANDO] Ainda nao executou hoje")
    else:
        print("Ultima execucao: Nunca")
        print("Status: [AGUARDANDO] Nunca executou")
    
    print(f"Hora de execucao: {HORA_EXECUCAO:02d}:00")
    
    proxima = calcular_proxima_execucao()
    print(f"Proxima execucao: {proxima.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Mostrar últimas execuções
    if status.get("execucoes"):
        print(f"\nUltimas {min(5, len(status['execucoes']))} execucoes:")
        for execucao in status["execucoes"][-5:]:
            data = datetime.fromisoformat(execucao["data"])
            status_icon = "[OK]" if execucao["sucesso"] else "[ERRO]"
            sucessos = execucao.get("sucessos", 0)
            falhas = execucao.get("falhas", 0)
            print(f"  {status_icon} {data.strftime('%Y-%m-%d %H:%M')} ({sucessos} sucessos, {falhas} falhas)")
    
    print("="*60)

def main():
    """Função principal"""
    print("=" * 80)
    print("SISTEMA COMPLETO DE ANALISE E SIMULACAO")
    print("   Campeonato Brasileiro - Series A e B 2025")
    print("=" * 80)
    
    # Limpar log anterior
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    
    log_message("[INICIO] Iniciando execucao completa do sistema", Colors.BOLD)
    
    # Verificar se estamos no diretório correto
    if not DATA_DIR.exists():
        log_message("[ERRO] Execute este script na raiz do projeto (onde esta a pasta 'data')", Colors.RED)
        return False
    
    # Verificar argumentos de linha de comando
    limpar_dados = False
    iniciar_servidor = False
    modo_agendador_ativo = False
    
    # Verificar argumentos
    for arg in sys.argv[1:]:
        if arg in ['--clean', '-c', '--limpar']:
            limpar_dados = True
            log_message("[INFO] Modo limpeza ativado via argumento", Colors.YELLOW)
        elif arg in ['--server', '-s', '--web']:
            iniciar_servidor = True
            log_message("[INFO] Modo servidor web ativado via argumento", Colors.YELLOW)
        elif arg in ['--agendador', '-a', '--daemon']:
            modo_agendador_ativo = True
            log_message("[INFO] Modo agendador ativado via argumento", Colors.YELLOW)
        elif arg in ['--status']:
            mostrar_status_agendador()
            return True
        elif arg in ['--force']:
            # Força execução mesmo se já executou hoje
            log_message("[INFO] Modo forçado ativado", Colors.YELLOW)
    
    # Se modo agendador ativado, executar diretamente
    if modo_agendador_ativo:
        modo_agendador()
        return True
    
    # Se nenhum argumento foi passado, ativar modo agendador automaticamente
    if len(sys.argv) == 1:
        log_message("[INFO] Nenhum argumento detectado - ativando modo agendador automaticamente", Colors.YELLOW)
        modo_agendador()
        return True
    
    # Nunca limpar dados automaticamente - sempre manter dados existentes
    if not limpar_dados:
        log_message("[INFO] Mantendo dados existentes (modo automatico)", Colors.YELLOW)
    
    if limpar_dados:
        limpar_dados_antigos()
    else:
        log_message("[INFO] Mantendo dados existentes", Colors.YELLOW)
    
    # Executar sistema completo
    sucesso = executar_sistema_completo()
    
    # Gerar relatório final
    relatorio = gerar_relatorio_final()
    
    # Resumo final
    print("\n" + "="*80)
    print("RESUMO DA EXECUCAO")
    print("="*80)
    
    if sucesso:
        log_message("[COMPLETO] SISTEMA EXECUTADO COM SUCESSO!", Colors.GREEN + Colors.BOLD)
        log_message("[INFO] Verifique a pasta 'data/' para os resultados", Colors.BLUE)
    else:
        log_message("[AVISO] Sistema executado com falhas. Verifique o log.", Colors.YELLOW)
    
    log_message(f"[LOG] Log completo salvo em: {LOG_FILE}", Colors.BLUE)
    log_message(f"[RELATORIO] Relatorio salvo em: relatorio_execucao.json", Colors.BLUE)
    
    # Iniciar servidor web se solicitado
    if iniciar_servidor and sucesso:
        log_message("[WEB] Iniciando servidor web...", Colors.BLUE)
        try:
            subprocess.Popen([sys.executable, "server.py"], cwd=".")
            log_message("[WEB] Servidor iniciado em http://localhost:8000", Colors.GREEN)
            log_message("[INFO] Pressione Ctrl+C para parar o servidor", Colors.YELLOW)
        except Exception as e:
            log_message(f"[ERRO] Falha ao iniciar servidor: {str(e)}", Colors.RED)
    
    print("\n[FIM] EXECUCAO CONCLUIDA!")
    
    return sucesso

if __name__ == "__main__":
    try:
        sucesso = main()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n[AVISO] Execucao interrompida pelo usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {str(e)}")
        sys.exit(1)
