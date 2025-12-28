@echo off
echo ===============================
echo RESET DO AMBIENTE - MOCK GLPI
echo ===============================

del mock_glpi.db

python -c "from database.models import create_tables; create_tables()"

python -m database.seed

python -m extraction.run_extraction

echo ===============================
echo PROCESSO FINALIZADO
echo ===============================
pause
