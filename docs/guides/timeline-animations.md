# Linha do Tempo e Ações

A classe `Timeline` permite encadear eventos em ordem sequencial para contar a história do funcionamento da arquitetura.

---

## :material-movie-open-outline: Métodos da Linha do Tempo

### 1. `reveal_sequence`
Faz os nós do sistema aparecerem na tela de forma gradual e elegante:

```python
# Revela cada nó com um intervalo de 0.25s entre eles
flow.timeline.reveal_sequence(delay=0.25)
```

### 2. `reveal_all`
Faz todos os nós e arestas aparecerem instantaneamente na tela:

```python
flow.timeline.reveal_all()
```

### 3. `send_packet`
Envia um pacote ou mensagem discreta de um nó de origem até o nó de destino com efeito de pulso:

```python
flow.timeline.send_packet(
    from_node=client, 
    to_node=api, 
    label="POST /order", 
    duration=0.8
)
```

### 4. `highlight_node`
Aplica um pulso de realce no nó selecionado (aumenta o brilho da borda e retorna suavemente):

```python
flow.timeline.highlight_node(database)
```

### 5. `wait`
Insere uma pausa na animação para permitir a leitura de legendas ou visualização de estados:

```python
flow.timeline.wait(1.5)
```

