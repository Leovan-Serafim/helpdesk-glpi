PRAGMA foreign_keys = ON;

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    contrato_tipo TEXT,
    ativo BOOLEAN DEFAULT 1
);

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    setor TEXT,
    email TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE equipamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    hostname TEXT NOT NULL,
    tipo TEXT,
    sistema_operacional TEXT,
    status TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE chamados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    equipamento_id INTEGER,
    usuario_id INTEGER,
    categoria TEXT,
    problema TEXT NOT NULL,
    status TEXT,
    data_abertura DATE NOT NULL,
    data_fechamento DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE solucoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chamado_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    sucesso BOOLEAN,
    data_aplicacao DATE NOT NULL,
    FOREIGN KEY (chamado_id) REFERENCES chamados(id)
);
