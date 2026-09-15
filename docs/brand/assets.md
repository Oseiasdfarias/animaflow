# Assets da Marca para Download

Todos os arquivos vetoriais e rasterizados de alta resolução da marca **animaflow** estão disponíveis na raiz do projeto dentro da pasta [`brand/`](https://github.com/Oseiasdfarias/animaflow/tree/main/brand).

---

## :material-folder-multiple-image: Variantes Disponíveis

### 1. Arquivos Vetoriais SVG (`brand/svg/`)

- **[Ícone Colorido (Dark)](../brand/svg/icone.svg)**: Símbolo oficial em formato vetorial.
- **[Ícone Sólido Escuro (Light)](../brand/svg/icone-solido.svg)**: Para aplicações em papel ou fundos claros.
- **[Logo Horizontal Completo](../brand/svg/logo-horizontal.svg)**: Símbolo e tipografia alinhados horizontalmente.
- **[Logo Vertical Completo](../brand/svg/logo-vertical.svg)**: Assinatura empilhada centralizada.
- **[Favicon](../brand/svg/favicon.svg)**: Otimizado para 16px e 32px.
- **[Banner Hero](../brand/svg/banner-hero.svg)**: 1280x640px para Open Graph e mídias sociais.

---

### 2. Arquivos PNG em Alta Fidelidade (`brand/png/`)

Rasterizados nativamente via PyCairo com antialiasing subpixel:

| Recurso | Resoluções Disponíveis |
| --- | --- |
| **Ícone** | 1024x1024, 512x512, 256x256, 128x128, 64x64 |
| **Favicon** | 180x180 (Apple Touch), 64x64, 32x32, 16x16 |
| **Logo Horizontal** | 1600px de largura, 800px de largura |
| **Logo Vertical** | 800px de largura |
| **Banner Hero** | 1280x640px |

---

## :material-refresh: Como Regenerar Automaticamente

Se você modificar alguma constante ou proporção do símbolo, basta rodar o script gerador:

```bash
python brand/scripts/gen_brand.py
```

