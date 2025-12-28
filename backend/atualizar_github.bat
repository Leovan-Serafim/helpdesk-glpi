@echo off

# 1. Entre na pasta do projeto (se ainda não estiver)
cd D:\[PROJETOS]\Inovit\helpdesk-glpi\helpdesk-glpi

# 2. Verifique o status (opcional, mas recomendado)
git status

# 3. Adicione TODAS as alterações de uma vez
git add .

# 4. Faça o commit com uma mensagem clara
git commit -m "Atualização completa: correções finais, frontend funcional, integração Ollama/Mistral e página de chamados"

# 5. Envie tudo para o GitHub
git push origin main