Federal Register Chat Agent (RAG System)

This project builds a local Retrieval-Augmented Generation (RAG) chat system that lets users ask questions about U.S. Federal Register documents using:

--> MySQL database (daily updated)

--> Local LLM (qwen:0.5b via Ollama)

--> Custom tool-call logic

--> FastAPI backend

--> Streamlit chat interface

      (  ----------------PROJECT FILES----------------    )


| File / Folder             | Description                                  |
| ------------------------- | -------------------------------------------- |
| `test_ollama.py`          | Tests that the local LLM (Ollama) is working |
| `source.py`               | Main agent logic (LLM + MySQL query)         |
| `fast_api.py`             | FastAPI backend exposing `/chat` endpoint    |
| `chat_ui.py`              | Streamlit web interface                      |
| `insert_data_to_mysql.py` | Loads processed CSV data into MySQL          |
| `processed_data/`         | Folder containing cleaned CSV files          |

      ( --------------Setup Instructions---------------------  )

1. Install Requirements  
         pip install openai==0.28.1 streamlit fastapi uvicorn mysql-connector-python requests
2. Pull & Run the Model
         ollama pull qwen:0.5b
         ollama run qwen:0.5b
3. Prepare MySQL Database
         Create a database: federal_data
         Create a table federal_register with columns:
                  title (TEXT)
                  publication_date (DATE)
                  agency (VARCHAR)
         Then load your data:
                  python insert_data_to_mysql.py

   ( --------------------- Run the System ---------------- )

   
   Step 1: Test Ollama LLM
         python test_ollama.py
   
   Step 2: Test Query + LLM Agent Logic
          python source.py
   
   Step 3: Start FastAPI Backend
           uvicorn fast_api:app --reload
   
    Step 4: Launch Streamlit Web UI
           streamlit run chat_ui.py

 
