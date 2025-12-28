from database.connection import get_connection
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT NOT NULL,
        cnpj TEXT,
        contato TEXT
                   
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        tipo TEXT,
        marca TEXT,
        modelo TEXT,
        serial TEXT,
        localizacao TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                
        )
        """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    cliente_id INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                      
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chamados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        equipamento_id INTEGER,
        usuario_id INTEGER,
        problema TEXT,
        categoria TEXT,
        status TEXT,
        data_abertura TEXT,
        data_fechamento TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS solucoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT,
        descricao_problema TEXT,
        procedimento TEXT,
        observacoes TEXT
    )
    """)

    conn.commit()
    conn.close()