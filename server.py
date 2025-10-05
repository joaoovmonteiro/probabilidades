#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor HTTP simples para servir o site localmente
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Adicionar headers CORS para permitir carregar arquivos JSON
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Adicionar headers para evitar cache
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start_server():
    """Inicia o servidor HTTP local"""
    # Verificar se estamos no diretório correto
    if not Path('index.html').exists():
        print("Erro: Execute este script na raiz do projeto (onde esta o index.html)")
        return
    
    # Verificar se a pasta data existe
    if not Path('data').exists():
        print("Erro: Pasta 'data' nao encontrada. Execute o main.py primeiro para gerar os dados.")
        return
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("SERVIDOR WEB INICIADO")
            print("=" * 60)
            print(f"URL: http://localhost:{PORT}")
            print(f"Diretorio: {os.getcwd()}")
            print("=" * 60)
            print("Abrindo navegador...")
            print("=" * 60)
            print("Para parar o servidor: Ctrl+C")
            print("=" * 60)
            
            # Abrir navegador automaticamente
            webbrowser.open(f'http://localhost:{PORT}')
            
            # Iniciar servidor
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\nServidor parado pelo usuario")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"Erro: Porta {PORT} ja esta em uso")
            print("Tente fechar outros servidores ou use uma porta diferente")
        else:
            print(f"Erro ao iniciar servidor: {e}")

if __name__ == "__main__":
    start_server()
