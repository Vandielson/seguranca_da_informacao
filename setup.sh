#!/bin/bash
echo "Iniciando setup do ambiente da PoC..."

# 1. Criar arquivo .env se não existir
if [ ! -f .env ]; then
  echo "Arquivo .env não encontrado. Criando a partir de .env.example..."
  echo "Por favor, edite o arquivo .env e adicione sua GOOGLE_API_KEY."
  cp .env.example .env
  # Pausa para o usuário editar o .env
  read -p "Pressione [Enter] após editar o .env com sua API Key..."
fi

# 2. Criar diretórios de dados se não existirem
mkdir -p ./data/corpus
mkdir -p ./data/db # Para persistência do ChromaDB

echo "Construindo a imagem Docker..."
docker-compose build

echo "Subindo o container (em modo detached)..."
docker-compose up -d

echo "Setup concluído! O pipeline está disponível em http://localhost:8000"
echo "Para ver os logs, rode: docker-compose logs -f"
echo "Para derrubar o ambiente, rode: docker-compose down"
