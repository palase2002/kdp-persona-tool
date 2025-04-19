
@echo off
echo ✅ Avvio della web app Buyer Persona Generator...

REM Imposta il percorso temporaneo (modifica se necessario)
SET PATH=%PATH%;%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts

REM Lancia Streamlit
streamlit run app.py

pause
