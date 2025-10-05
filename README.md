# 🏆 Sistema de Análise e Simulação - Campeonato Brasileiro 2025

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/joaoovmonteiro/probabilidades)

Sistema completo de análise estatística avançada e simulação do Campeonato Brasileiro das Séries A e B 2025, utilizando algoritmos de previsão e dados históricos em tempo real.

## 🚀 Funcionalidades

- **📊 Simulação Estatística**: 300.000 simulações por série para máxima precisão
- **🔄 Coleta Automática**: Busca automática de jogos e resultados via API
- **📈 Análise de Probabilidades**: Cálculo preciso de chances de título, rebaixamento e acesso
- **🌐 Interface Web**: Visualização dos resultados em tempo real
- **⏰ Agendamento Inteligente**: Execução automática diária às 06:00
- **💾 Cache Inteligente**: Preservação de dados para otimização
- **📱 Design Responsivo**: Interface adaptável para desktop e mobile

## 🛠️ Tecnologias

- **Python 3.x**: Lógica principal e simulações estatísticas
- **JavaScript ES6+**: Interface web dinâmica e interativa
- **HTML5/CSS3**: Frontend moderno e responsivo
- **JSON**: Armazenamento eficiente de dados
- **APIs REST**: Coleta automática de dados de jogos
- **NumPy**: Cálculos estatísticos avançados

## 📁 Estrutura do Projeto

```
probabilidades/
├── 📄 main.py                    # Script principal e orquestrador
├── 🎯 sistema_completo.py        # Sistema unificado completo
├── 🌐 server.py                  # Servidor web local
├── 📊 data/                      # Dados processados
│   ├── cache_jogos_serie_a.json
│   ├── cache_jogos_serie_b.json
│   ├── resultados_simulacao_*.json
│   └── web_*.json
├── 🎨 *.html                     # Páginas web (Série A e B)
├── ⚡ *.js                       # JavaScript dinâmico
├── 🎨 styles.css                 # Estilos CSS
└── 📖 README.md                  # Documentação
```

## 🚀 Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone https://github.com/joaoovmonteiro/probabilidades.git
cd probabilidades
```

### 2. Instale as Dependências
```bash
pip install requests numpy
```

### 3. Execute o Sistema
```bash
python main.py
```

## 💻 Uso

### 🔄 Execução Automática (Recomendado)
```bash
python main.py
```
- ✅ Executa automaticamente 1x por dia às 06:00
- ✅ Mantém dados existentes
- ✅ Executa continuamente até interromper

### 🧹 Modos de Execução
```bash
python main.py --clean      # Limpa dados antigos
python main.py --server     # Inicia servidor web
python main.py --status     # Mostra status do agendador
```

### 🌐 Servidor Web
```bash
python server.py
```
**Acesse**: http://localhost:8000

## ⚙️ Configuração

### 🔑 API Key
Configure sua API key no arquivo `sistema_completo.py`:
```python
API_KEY = "sua_api_key_aqui"
```

### ⏰ Horário de Execução
O agendador executa automaticamente às **06:00 da manhã** todos os dias.

## 📊 Dados e Simulações

### 📈 Simulações Estatísticas
- **300.000 simulações** por série para máxima precisão
- **Distribuição Poisson** para gols
- **Análise retrospectiva** de performance
- **Cálculo de probabilidades** em tempo real

### 📁 Arquivos Gerados
- `data/cache_jogos_serie_a.json` - Jogos da Série A
- `data/cache_jogos_serie_b.json` - Jogos da Série B
- `data/resultados_simulacao_*.json` - Resultados das simulações
- `data/web_*.json` - Dados otimizados para interface web

### 🎯 Métricas Calculadas
- **Probabilidades de título** para cada time
- **Chances de rebaixamento** (4 últimos)
- **Possibilidades de acesso** à Série A (4 primeiros da Série B)
- **Classificações finais** projetadas
- **Estatísticas detalhadas** de performance

## 🎨 Interface Web

### 📱 Páginas Disponíveis
- **🏠 Página Inicial**: Visão geral do sistema
- **🏆 Série A**: Probabilidades, classificação, próximos jogos
- **🥈 Série B**: Probabilidades, classificação, próximos jogos
- **ℹ️ Sobre**: História e informações do sistema

### 🎯 Funcionalidades da Interface
- **Atualização automática** de dados
- **Visualização responsiva** para mobile
- **Gráficos interativos** de probabilidades
- **Tabelas de classificação** em tempo real

## 🔧 Desenvolvimento

### 🧪 Testes
```bash
python main.py --status     # Verificar status
python sistema_completo.py  # Execução direta
```

### 📝 Logs
- Logs detalhados de execução
- Status do agendador
- Relatórios de simulação

## 🤝 Contribuição

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**João Monteiro** - [@joaoovmonteiro](https://github.com/joaoovmonteiro)

## 🙏 Agradecimentos

- **TheSportsDB API** por fornecer dados de jogos
- **Comunidade Python** pelas bibliotecas utilizadas
- **Futebol Brasileiro** pela inspiração

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões:

1. **Abra uma Issue** no GitHub
2. **Entre em contato** via email
3. **Contribua** com melhorias

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐