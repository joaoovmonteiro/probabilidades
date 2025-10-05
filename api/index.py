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
                with open('data/web_serie_a.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.wfile.write(json.dumps(data).encode())
            except FileNotFoundError:
                self.wfile.write(json.dumps({'error': 'Dados da Série A não encontrados'}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        # Rota para dados da Série B
        elif self.path == '/api/serie-b':
            try:
                with open('data/web_serie_b.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.wfile.write(json.dumps(data).encode())
            except FileNotFoundError:
                self.wfile.write(json.dumps({'error': 'Dados da Série B não encontrados'}).encode())
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
                    '/api/status'
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
