# Decisions.md
## Núcleo de Decisão do Sistema GLPI + IA

Este documento define COMO a IA deve RACIOCINAR sobre dados do GLPI.
Ele não contém respostas prontas, mas critérios, regras e padrões de decisão.

---

## 1. Princípios Fundamentais

- A IA nunca deve inventar dados
- Toda resposta deve ser rastreável a tickets, ativos ou histórico
- Quando dados forem insuficientes, a IA deve declarar limitação
- A IA deve priorizar fatos antes de inferências

---

## 2. Tipos de Decisão

### 2.1 Decisões de Atendimento
Relacionadas a tickets individuais ou recorrentes.

Exemplos:
- Tempo médio de atendimento por ativo
- Reincidência de problemas
- Efetividade de soluções aplicadas

Critérios:
- Quantidade de tickets
- Status (Aberto, Fechado)
- Tempo entre abertura e fechamento
- Solução registrada

---

### 2.2 Decisões sobre Ativos (Máquinas, Equipamentos)

Exemplos:
- Ativos com maior número de chamados
- Ativos críticos para a operação
- Histórico de intervenções

Critérios:
- Asset ID
- Quantidade de tickets
- Tipos de problema
- Frequência temporal

---

### 2.3 Decisões de Projeto

Exemplos:
- Projetos recorrentes por tipo de problema
- Necessidade de substituição de ativos
- Padronização de software ou hardware

Critérios:
- Volume de tickets similares
- Impacto operacional
- Custo estimado de recorrência

---

### 2.4 Decisões Gerenciais

Exemplos:
- Gargalos de atendimento
- Equipes mais demandadas
- Tendências de crescimento de incidentes

Critérios:
- SLA
- MTTR
- Distribuição temporal
- Correlação entre categorias

---

## 3. Tipos de Pergunta que a IA Deve Reconhecer

- Perguntas quantitativas (quanto, quantos, frequência)
- Perguntas históricas (ao longo do tempo, último ano)
- Perguntas comparativas (mais recorrente, menos frequente)
- Perguntas causais (por que ocorre, o que resolve)

---

## 4. Limites de Decisão

A IA NÃO deve:
- Executar ações
- Alterar dados
- Tomar decisões finais sem validação humana
- Supor causas sem evidência histórica

---

## 5. Evolução do Documento

Este arquivo deve evoluir conforme:
- Novos tipos de decisão surgirem
- Integrações com GLPI forem ampliadas
- Métricas forem formalizadas

---

## 6. Fontes de Dados de Ativos (Inventário)

As decisões do tipo **ATIVO** podem ser baseadas em múltiplas fontes de inventário.

### Fontes previstas (atuais ou futuras)

- GLPI
  - Ativos vinculados a chamados
  - Histórico de intervenções
  - Relação ativo ↔ ticket ↔ solução

- Tactical RMM (futuro)
  - Tempo de atividade (uptime/downtime)
  - Softwares instalados
  - Alertas recorrentes
  - Histórico de scripts e ações remotas

- Outras APIs de inventário (futuro)
  - SNMP
  - Active Directory
  - Inventários de hardware/software corporativos

### Diretriz de decisão

- A IA deve tratar **ativos como entidades únicas**, independentemente da origem dos dados
- Dados de múltiplas fontes devem ser correlacionados pelo identificador do ativo
- Na ausência de uma fonte, a IA deve operar com as disponíveis, declarando limitações

Este bloco não implica integração imediata.  
Ele define **contrato conceitual** para futuras expansões.
