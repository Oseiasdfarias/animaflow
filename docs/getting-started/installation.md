# Guia de Instalação

O **animaflow** pode ser instalado de forma modular dependendo do caso de uso e dos motores de renderização desejados.

---

## 📦 Instalação via pip

### 1. Pacote Básico (Core + Web Canvas)
Para criar fluxos, rodar layouts e exportar visualizações interativas em HTML/SVG independente:

```bash
pip install animaflow
```

### 2. Com suporte ao Renderizador Manim (Vídeo & GIF)
Para gerar animações em vídeo MP4 e GIFs em alta definição para LinkedIn, YouTube ou apresentações:

```bash
pip install "animaflow[manim]"
```

### 3. Instalação Completa (Desenvolvimento)
Instala todas as dependências do core, Manim, Web Canvas e ferramentas de desenvolvimento:

```bash
pip install "animaflow[all]"
```

---

## ⚙️ Dependências de Sistema

### FFmpeg (Obrigatório para o Manim)
Para compilar vídeos e extrair GIFs através do Manim Community Edition, o binário do `ffmpeg` precisa estar presente no seu `PATH`:

=== "Ubuntu / Debian"
    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```

=== "macOS (Homebrew)"
    ```bash
    brew install ffmpeg
    ```

=== "Windows (Winget / Chocolatey)"
    ```powershell
    winget install Gyan.FFmpeg
    # ou com chocolatey:
    choco install ffmpeg
    ```

---

## 🧪 Verificando a Instalação

Abra um terminal interativo Python e execute:

```python
import animaflow as af

flow = af.Flow(title="Teste de Instalação")
node = flow.add_node("API Gateway")
print(f"animaflow instalado com sucesso! Nó criado: {node.name}")
```

Se o comando executar sem erros, sua instalação está pronta para o [Primeiro Diagrama](quickstart.md)!

