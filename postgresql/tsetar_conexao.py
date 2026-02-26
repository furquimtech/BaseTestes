# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import psycopg2
from psycopg2 import OperationalError

# =============================================
# Configurações de conexão
# =============================================
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "dev_db",
    "user":     "postgres",
    "password": "f5vcn32k",
    "options":  "-c client_encoding=UTF8"
}

# =============================================
# Teste de conexão
# =============================================
def testar_conexao():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Versão do PostgreSQL
        cursor.execute("SELECT version();")
        versao = cursor.fetchone()
        print(f"✅ Conexão bem-sucedida!")
        print(f"   PostgreSQL: {versao[0]}")

        # Banco atual
        cursor.execute("SELECT current_database();")
        banco = cursor.fetchone()
        print(f"   Banco:      {banco[0]}")

        # Lista schemas disponíveis
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
            ORDER BY schema_name;
        """)
        schemas = cursor.fetchall()
        print(f"   Schemas:    {[s[0] for s in schemas]}")

        cursor.close()
        conn.close()

    except OperationalError as e:
        print(f"❌ Erro ao conectar: {e}")

if __name__ == "__main__":
    testar_conexao()