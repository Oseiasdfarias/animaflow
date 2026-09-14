# Declarando Nós e Conexões

Este guia detalha como modelar entidades, conexões e legendas no **animaflow**.

---

## 🏗️ Adicionando Nós (`add_node`)

O método `flow.add_node()` registra uma nova entidade no diagrama:

```python
# Adicionando nós com título e subtítulo técnico
client = flow.add_node("Mobile App", subtitle="React Native")
gateway = flow.add_node("API Gateway", subtitle="Traefik / Envoy")
auth = flow.add_node("Auth Service", subtitle="OAuth2 / JWT")
db = flow.add_node("Users DB", subtitle="PostgreSQL")
```

### Propriedades Disponíveis:
| Parâmetro | Tipo | Padrão | Descrição |
| --- | --- | --- | --- |
| `name` | `str` | *obrigatório* | Nome principal exibido no nó |
| `id` | `str` | `None` | Identificador único. Se omitido, é gerado automaticamente |
| `subtitle` | `str` | `None` | Descrição técnica exibida abaixo do nome em tipografia menor |
| `icon` | `str` | `None` | Identificador de ícone ou categoria |

---

## 🔗 Conectando Nós (`connect`)

Conecte dois nós passando os objetos retornados por `add_node` ou seus respectivos `id`s:

```python
# Conexão direta com rótulo descritivo
flow.connect(client, gateway, label="HTTPS POST /login")
flow.connect(gateway, auth, label="verify_credentials()")
flow.connect(auth, db, label="SELECT * FROM users")
```

### Regras de Quebra Automática de Rótulos (Label Wrapping)
Quando o texto de uma aresta é longo (como chamadas de query ou payloads complexos), o animaflow analisa a distância física entre os retângulos dos nós e ajusta o rótulo para não sobrepor as bordas:

```python
# O texto é envolvido proporcionalmente à extensão da aresta
flow.connect(
    worker, 
    analytics, 
    label="process_batch_events(chunk_size=5000, compression='gzip')"
)
```
