# ⚛️ Acompanhamento de Pós-Doc — Vantagem Quântica

**Vantagem quântica na detecção óptica de baixas concentrações**  
PNPD/CAPES · UFMG/UFF

App Streamlit para acompanhamento das etapas e geração de relatório do pós-doutorado.

## Estrutura do projeto

11 Blocos de execução paralela com 4 Eixos:

| Eixo | Descrição |
|------|-----------|
| A | Síntese & Funcionalização de nanobastões |
| B | Modelagem Computacional (BEM/FDTD) |
| C | Fonte Quântica SPDC (~810 nm) |
| D | Medida Quântica sub-shot-noise |

## Como rodar localmente

```bash
pip install streamlit
streamlit run posdoc_tracker.py
```

## Como publicar no Streamlit Community Cloud

1. Suba este repositório no GitHub (pode ser privado)
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte sua conta GitHub
3. Clique em **New app** → selecione o repositório → `posdoc_tracker.py` como arquivo principal
4. Clique em **Deploy** — o app fica online em segundos

## Persistência de dados

O progresso é salvo em `posdoc_state.json` na mesma pasta.  
No Streamlit Cloud, os dados **não persistem entre reinicializações do servidor** — use a função **Exportar JSON** na página Relatório para fazer backup, e coloque o arquivo no repositório ou restaure quando necessário.

> Para persistência permanente no Cloud, a solução recomendada é conectar um banco de dados externo (ex.: Supabase, Google Sheets via API). Abra uma issue se quiser essa extensão.
