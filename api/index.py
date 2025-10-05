#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API para o Vercel - Sistema de Análise e Simulação
Campeonato Brasileiro 2025
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from pathlib import Path

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Configurar headers CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Rota para dados da Série A
        if self.path == '/api/serie-a':
            try:
                # Tentar diferentes caminhos para encontrar o arquivo
                possible_paths = [
                    'data/web_serie_a.json',
                    '/var/task/data/web_serie_a.json',
                    '/vercel/path0/data/web_serie_a.json',
                    os.path.join(os.getcwd(), 'data', 'web_serie_a.json')
                ]
                
                data = None
                for path in possible_paths:
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        break
                    except FileNotFoundError:
                        continue
                
                if data:
                    self.wfile.write(json.dumps(data).encode())
                else:
                    self.wfile.write(json.dumps({'error': 'Dados da Série A não encontrados em nenhum caminho'}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        # Rota para dados da Série B
        elif self.path == '/api/serie-b':
            try:
                # Tentar diferentes caminhos para encontrar o arquivo
                possible_paths = [
                    'data/web_serie_b.json',
                    '/var/task/data/web_serie_b.json',
                    '/vercel/path0/data/web_serie_b.json',
                    os.path.join(os.getcwd(), 'data', 'web_serie_b.json')
                ]
                
                data = None
                for path in possible_paths:
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        break
                    except FileNotFoundError:
                        continue
                
                if data:
                    self.wfile.write(json.dumps(data).encode())
                else:
                    self.wfile.write(json.dumps({'error': 'Dados da Série B não encontrados em nenhum caminho'}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        # Rota para debug do sistema de arquivos
        elif self.path == '/api/debug':
            try:
                debug_info = {
                    'current_directory': os.getcwd(),
                    'files_in_root': [],
                    'data_directory_exists': False,
                    'data_files': []
                }
                
                # Listar arquivos no diretório raiz
                try:
                    debug_info['files_in_root'] = os.listdir('.')
                except:
                    pass
                
                # Verificar se pasta data existe
                if os.path.exists('data'):
                    debug_info['data_directory_exists'] = True
                    try:
                        debug_info['data_files'] = os.listdir('data')
                    except:
                        pass
                
                self.wfile.write(json.dumps(debug_info, indent=2).encode())
            except Exception as e:
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        # Rota para status do sistema
        elif self.path == '/api/status':
            status = {
                'status': 'online',
                'message': 'Sistema de Análise e Simulação - Campeonato Brasileiro 2025',
                'version': '1.0.0',
                'endpoints': [
                    '/api/serie-a',
                    '/api/serie-b',
                    '/api/status',
                    '/api/debug'
                ]
            }
            self.wfile.write(json.dumps(status).encode())
        
        # Rota padrão
        else:
            self.wfile.write(json.dumps({
                'message': 'API do Sistema de Análise e Simulação',
                'endpoints': [
                    '/api/serie-a',
                    '/api/serie-b', 
                    '/api/status'
                ]
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
