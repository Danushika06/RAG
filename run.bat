@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating RAG database from document...
python create_database.py

echo.
echo Starting the RAG chatbot web application...
echo Open your browser and go to: http://localhost:5000
echo.
python app.py