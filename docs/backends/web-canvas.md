# Backend Web Canvas (HTML & SVG)

O renderizador **Web Canvas** (`backends.web.canvas`) transforma seu diagrama em uma página web independente, leve e interativa, baseada em SVG e JavaScript puro.

---

## 🌐 Gerando o HTML

Você pode exportar a string HTML completa diretamente pelo objeto `Flow`:

```python
import animaflow as af

flow = af.Flow(title="Cloud Architecture")
# ... configure nós e conexões ...

# Exporta a página completa pronta para exibição
html_code = flow.export_html()

with open("dashboard_arquitetura.html", "w", encoding="utf-8") as f:
    f.write(html_code)
```

---

## ✨ Recursos da Visualização Web

1. **Zero Dependências Externas**: Não requer Node.js, React ou bibliotecas pesadas de terceiros; roda direto no browser com JavaScript vanilla.
2. **Vetores Nativos SVG**: Escala infinitamente para qualquer resolução ou tela sem perder nitidez ou gerar artefatos de compressão.
3. **Simulação de Partículas em JS**: Utiliza temporizadores assíncronos para simular streams contínuos de partículas através das conexões SVG.
4. **Botões de Interação**: Inclui controles de reprodução para reiniciar o fluxo de animação a qualquer momento.

---

## 📦 Incorporando em Documentações e Dashboards

O HTML gerado pode ser embutido como um `<iframe>` em documentações MkDocs, Notion, Confluence ou ferramentas internas de engenharia:

```html
<iframe src="dashboard_arquitetura.html" width="100%" height="600" frameborder="0"></iframe>
```

