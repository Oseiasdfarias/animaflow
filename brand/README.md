# animaflow — Identidade Visual Oficial

Identidade visual e sistema de design do **animaflow** baseada na estética **Nordic Sage & Carbon** (design escandinavo sóbrio e técnico).

---

## O Símbolo

<p align="center">
  <img width="180" src="./png/icone-512.png" alt="Símbolo animaflow Nordic Sage">
</p>

O símbolo sintetiza a essência do **animaflow**:
- **Três Nós Fundamentais**: entrada/ingestão, processamento/orquestração e destino dos dados.
- **Fluxo Orbital Contínuo**: o circuito contínuo de dados (`stream_packets`).
- **Nó Acento Sálvia / Jade**: geometria calibrada para legibilidade técnica sem ruídos gráficos.

---

## Paleta Oficial: Nordic Sage & Carbon

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./png/logo-horizontal-800.png">
    <img height="100" src="./png/logo-horizontal-solido-800.png" alt="animaflow">
  </picture>
</p>

| Papel | Nome | Hex | Aplicação |
| --- | --- | --- | --- |
| **Dark Background** | Carvão Mineral | `#121619` | Fundo principal da identidade e modo escuro |
| **Dark Surface** | Ardósia Profunda | `#1A2024` | Fundo de cartões, badges e superfícies |
| **Dark Border** | Carvão Técnico | `#242D33` | Bordas e divisores de interface |
| **Sage Light** | Sálvia Mineral | `#9EC8B9` | Nó acento e tipografia secundária |
| **Sage Ice** | Sálvia Gélido | `#D7EBE3` | Tipografia principal (Dark) e partículas |
| **Jade Conductor**| Jade Técnico | `#5C9E89` | Traçado principal do circuito de fluxo |
| **Light Background** | Papel Nórdico | `#F2F6F4` | Fundo para documentação clara e impressão |
| **Light Ink** | Tinta Grafite Escura | `#162420` | Logotipo e nós principais em fundo claro |
| **Light Stroke** | Verde Conífera | `#37594E` | Traçado em superfícies claras |

---

## Arquivos e Variantes

### 1. SVG (`svg/`)
- [`icone.svg`](./svg/icone.svg): Símbolo padrão (modo escuro).
- [`icone-solido.svg`](./svg/icone-solido.svg): Símbolo para fundos claros.
- [`icone-mono.svg`](./svg/icone-mono.svg): Símbolo com `currentColor`.
- [`logo-horizontal.svg`](./svg/logo-horizontal.svg): Assinatura horizontal para fundo escuro.
- [`logo-horizontal-solido.svg`](./svg/logo-horizontal-solido.svg): Assinatura horizontal para fundo claro.
- [`logo-vertical.svg`](./svg/logo-vertical.svg) e [`logo-vertical-solido.svg`](./svg/logo-vertical-solido.svg): Versões empilhadas.
- [`favicon.svg`](./svg/favicon.svg) e [`favicon-branco.svg`](./svg/favicon-branco.svg): Favicons vetoriais.
- [`banner-hero.svg`](./svg/banner-hero.svg): Banner 1280x640 para redes sociais e documentação.

### 2. PNG (`png/`)
Rasterizados nativamente em alta definição via PyCairo:
- Ícones em 1024, 512, 256, 128 e 64px.
- Favicons em 180, 64, 32 e 16px.
- Logos horizontais em 1600 e 800px.
- Logos verticais em 800px.
- Banner hero em 1280x640px.

---

## Como Regenerar

```bash
python brand/scripts/gen_brand.py
```
