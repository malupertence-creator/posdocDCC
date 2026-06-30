"""
Acompanhamento de Etapas — Pós-doutorado
Vantagem quântica na detecção óptica de baixas concentrações (PNPD/CAPES, UFMG/UFF)
"""

import streamlit as st
import json
import os
from datetime import datetime, date
from io import BytesIO

# ── Paleta por Eixo ──────────────────────────────────────────────────────────
EIXO_COLOR = {"A": "#2E86AB", "B": "#A23B72", "C": "#F18F01", "D": "#3BB273"}
EIXO_LABEL = {
    "A": "Eixo A — Síntese & Funcionalização",
    "B": "Eixo B — Modelagem Computacional",
    "C": "Eixo C — Fonte Quântica (SPDC)",
    "D": "Eixo D — Medida Quântica",
}
STATUS_EMOJI = {
    "Não iniciado": "⬜",
    "Em andamento": "🔄",
    "Concluído": "✅",
    "Bloqueado": "🚫",
}

# ── Dados completos do projeto ────────────────────────────────────────────────
BLOCOS = [
    {
        "id": 1,
        "titulo": "Bloco 1 — Largada: três frentes em paralelo",
        "prereq": "Nenhum. Todos os três eixos podem iniciar no dia 1.",
        "gonogo": None,
        "tarefas": [
            {
                "id": "A.1", "eixo": "A",
                "titulo": "Síntese inicial e varredura de aspect ratio",
                "objetivo": "Localizar a razão de aspecto que posiciona a banda longitudinal de LSPR perto de 810 nm.",
                "passos": [
                    "Preparar a solução de sementes de ouro (seed-mediated growth).",
                    "Crescer série de lotes variando a razão CTAB/sal de ouro para obter nanobastões com diferentes razões de aspecto ao redor do valor nominal (~4,9; D≈10 nm, L≈36 nm).",
                    "Para cada lote, medir o espectro de extinção UV-Vis-NIR.",
                ],
                "criterio": "Pelo menos um lote com banda longitudinal de LSPR entre 795–815 nm.",
                "risco": "Dispersão de tamanho/forma pode alargar a banda além do tolerável — mitigado por purificação por centrifugação e repetição da síntese.",
            },
            {
                "id": "B.1", "eixo": "B",
                "titulo": "Modelo eletromagnético nominal",
                "objetivo": "Ter uma primeira previsão da posição de banda antes de os dados experimentais de A estarem prontos.",
                "passos": [
                    "Construir o modelo BEM (ou FDTD) com a geometria nominal (D=10 nm, L=36 nm, dielétrico do ouro por Drude + 2 osciladores de Lorentz).",
                    "Simular o espectro de extinção em água (n≈1,33).",
                    "Comparar com a curva de referência da Fig. 1 do projeto.",
                ],
                "criterio": "Modelo reproduz a banda nua em ~781 nm dentro de alguns nm de tolerância.",
                "risco": None,
            },
            {
                "id": "C.1", "eixo": "C",
                "titulo": "Decisão de arquitetura da fonte",
                "objetivo": "Escolher a configuração de cristal não-linear, em articulação com o grupo da UFF.",
                "passos": [
                    "Avaliar BBO tipo-I como ponto de partida (mais simples; ideal para fóton único anunciado, coincidência e emaranhamento).",
                    "Planejar extensão para estágio ppKTP/ppLN quando for necessária compressão brilhante por diferença de intensidade.",
                    "Documentar a escolha com justificativa baseada na Tabela 1 do projeto.",
                ],
                "criterio": "Arquitetura definida por escrito com plano de transição BBO → ppKTP/ppLN explicitado.",
                "risco": None,
            },
        ],
    },
    {
        "id": 2,
        "titulo": "Bloco 2 — Caracterização, validação cruzada e montagem da fonte",
        "prereq": "A.1 concluído (ao menos um lote candidato); B.1 concluído; C.1 concluído. A.2 e B.2 têm dependência bidirecional entre si — iteram juntos até o critério ser atingido.",
        "gonogo": "Banda de LSPR em 795–815 nm E modelo B reproduz a banda dentro de 5 nm? Se não → repetir A.1 antes de avançar para A.3 e B.3.",
        "tarefas": [
            {
                "id": "A.2", "eixo": "A",
                "titulo": "Caracterização estrutural",
                "objetivo": "Confirmar tamanho, forma e estabilidade coloidal do lote selecionado em A.1.",
                "passos": [
                    "TEM/SEM do lote — medir distribuição de tamanho e razão de aspecto (n ≥ 100 partículas).",
                    "Potencial zeta — verificar estabilidade coloidal (idealmente |ζ| > 30 mV).",
                    "Comparar banda de LSPR observada com a prevista pelo modelo B.2 (validação cruzada A↔B).",
                ],
                "criterio": "Razão de aspecto medida em TEM consistente (±10%) com o valor que o modelo B prevê para a banda observada; dispersão de tamanho < 15%.",
                "risco": None,
            },
            {
                "id": "B.2", "eixo": "B",
                "titulo": "Validação cruzada com dados experimentais",
                "objetivo": "Ajustar o modelo com os dados reais de TEM/UV-Vis do Eixo A.",
                "passos": [
                    "Inserir a geometria real medida em TEM (A.2) no modelo.",
                    "Reexecutar a simulação e comparar com o espectro experimental observado.",
                    "Iterar geometria/parâmetros dielétricos até o modelo reproduzir a banda observada com boa fidelidade.",
                ],
                "criterio": "Erro entre banda simulada e observada dentro de ~5 nm.",
                "risco": "Loop A↔B: se o modelo ajustado sugerir um aspect ratio ligeiramente diferente, isso realimenta A.1 para uma nova rodada de síntese antes de prosseguir para A.3.",
            },
            {
                "id": "C.2", "eixo": "C",
                "titulo": "Montagem do bombeamento e da conversão paramétrica",
                "objetivo": "Montar fisicamente a fonte SPDC em ~810 nm.",
                "passos": [
                    "Montar o bombeamento (~405 nm) com ópticas de condicionamento e casamento de modo.",
                    "Posicionar o cristal não-linear e ajustar o casamento de fase para degenerescência em ~810 nm.",
                    "Verificar visualmente/espectralmente a geração do par sinal-idler centrado em ~810 nm.",
                ],
                "criterio": "Sinal de fluorescência paramétrica detectável nos dois braços (sinal e idler) com espectro centrado próximo a 810 nm.",
                "risco": None,
            },
        ],
    },
    {
        "id": 3,
        "titulo": "Bloco 3 — Funcionalização, modelo de camada molecular e primeiras coincidências",
        "prereq": "Bloco 2 concluído (A.2 + B.2 fechados com critérios atingidos; C.2 operacional).",
        "gonogo": None,
        "tarefas": [
            {
                "id": "A.3", "eixo": "A",
                "titulo": "Definição do par ligante/bioreceptor e protocolo de funcionalização",
                "objetivo": "Estabelecer a química de superfície que vai ligar o analito-alvo ao nanobastão.",
                "passos": [
                    "Selecionar o par ligante/bioreceptor adequado ao biomarcador de interesse (em conjunto com o Prof. Flávio Guimarães da Fonseca, ICB/UFMG).",
                    "Funcionalizar a superfície do nanobastão: troca de CTAB por camada estável e conjugação do bioreceptor.",
                    "Adicionar etapa de passivação (ex.: PEGuilação) para minimizar ligação não específica.",
                ],
                "criterio": "Protocolo de funcionalização escrito, replicável, com etapas e tempos definidos.",
                "risco": None,
            },
            {
                "id": "B.3", "eixo": "B",
                "titulo": "Modelo da camada molecular ligada e previsão de Δλ",
                "objetivo": "Prever o deslocamento espectral esperado por evento de ligação do analito.",
                "passos": [
                    "Adicionar ao modelo validado (B.2) uma casca molecular de índice efetivo n_shell e espessura t (modelo de meio efetivo, conforme Eq. da Fig. 1 do projeto).",
                    "Simular o deslocamento Δλ_long esperado para a espessura/índice estimados do bioreceptor + analito.",
                ],
                "criterio": "Δλ previsto documentado e pronto para comparação com o Δλ medido em A.4.",
                "risco": None,
            },
            {
                "id": "C.3", "eixo": "C",
                "titulo": "Mapeamento de coincidências sinal-idler e taxa de pares",
                "objetivo": "Primeira caracterização quantitativa da fonte.",
                "passos": [
                    "Detectar fótons individualmente nos dois braços com detectores de fóton único.",
                    "Medir a taxa de coincidências (correlação temporal) entre os braços sinal e idler.",
                    "Calcular a taxa de pares gerados por unidade de potência de bombeamento.",
                ],
                "criterio": "Taxa de coincidências significativamente acima do nível de acidentais (ruído não-correlacionado).",
                "risco": None,
            },
        ],
    },
    {
        "id": 4,
        "titulo": "Bloco 4 — Validação da bioconjugação, curva de calibração e eficiência de heralding",
        "prereq": "Bloco 3 concluído.",
        "gonogo": None,
        "tarefas": [
            {
                "id": "A.4", "eixo": "A",
                "titulo": "Validação da bioconjugação",
                "objetivo": "Confirmar experimentalmente que a funcionalização ocorreu e produz o deslocamento espectral esperado.",
                "passos": [
                    "Medir o espectro de extinção antes e depois da funcionalização.",
                    "Comparar o deslocamento observado (Δλ) com o previsto por B.3.",
                ],
                "criterio": "Deslocamento de banda mensurável, na direção e ordem de grandeza esperada (mesmo que o valor absoluto difira do modelo simplificado).",
                "risco": None,
            },
            {
                "id": "B.4", "eixo": "B",
                "titulo": "Curva de calibração de absorção",
                "objetivo": "Estabelecer a relação entre concentração do analito e sinal de absorção esperado.",
                "passos": [
                    "A partir do modelo validado (B.2 + B.3), calcular a seção de choque de extinção em função da fração de sítios ocupados pelo analito.",
                    "Converter em curva de calibração: absorbância esperada vs. concentração.",
                ],
                "criterio": "Curva de calibração com base física (não apenas ajuste empírico), pronta para o cálculo do benchmark.",
                "risco": None,
            },
            {
                "id": "C.4", "eixo": "C",
                "titulo": "Medida da eficiência de heralding",
                "objetivo": "Quantificar quão bem a detecção de um fóton anuncia a presença do parceiro.",
                "passos": [
                    "A partir das taxas de contagem simples e de coincidência, calcular a eficiência de heralding (razão entre coincidências e contagens simples em cada braço).",
                    "Mapear a curva eficiência vs. potência de bombeamento.",
                ],
                "criterio": "Eficiência de heralding documentada e estável dentro da faixa de operação pretendida.",
                "risco": None,
            },
        ],
    },
    {
        "id": 5,
        "titulo": "Bloco 5 — Matrizes de teste, benchmark SNL e medida do NRF",
        "prereq": "Bloco 4 concluído.",
        "gonogo": "σ < 1 foi obtido? Se não → revisar perdas ópticas e eficiência de detecção antes de continuar. Sem σ < 1, nenhum resultado do Eixo D é defensável.",
        "tarefas": [
            {
                "id": "A.5", "eixo": "A",
                "titulo": "Preparação de matrizes de teste",
                "objetivo": "Preparar as condições de medida realistas para o Eixo D.",
                "passos": [
                    "Testar a curva de resposta em tampão (matriz simples) primeiro.",
                    "Evoluir para soro (matriz biológica complexa), em conjunto com o ICB/UFMG.",
                    "Preparar série de diluição do analito em cada matriz, cobrindo a faixa picomolar a nanomolar.",
                ],
                "criterio": "Curva de resposta (sinal vs. concentração) mensurável em tampão antes de avançar para soro.",
                "risco": None,
            },
            {
                "id": "B.5", "eixo": "B",
                "titulo": "Benchmark clássico (SNL) e ponto de diluição crítico",
                "objetivo": "Estabelecer o 'alvo a vencer' — a fronteira que a medida quântica do Eixo D precisa superar.",
                "passos": [
                    "Para cada concentração da curva de calibração (B.4), calcular a incerteza Δα ∝ 1/√N de um estado coerente ideal com eficiência unitária.",
                    "Comparar, concentração por concentração, o sinal esperado com essa incerteza.",
                    "Identificar a concentração em que o sinal cruza a incerteza do SNL — esse é o ponto de diluição crítico.",
                ],
                "criterio": "Valor numérico do ponto de diluição crítico calculado e documentado. Este número orienta toda a série de diluição do Eixo D.",
                "risco": None,
            },
            {
                "id": "C.5", "eixo": "C",
                "titulo": "Determinação do fator de redução de ruído (NRF, σ)",
                "objetivo": "Obter a assinatura central de não-classicalidade exigida pelo projeto.",
                "passos": [
                    "Medir a diferença de intensidade entre os dois feixes (sinal – idler) em função do tempo/amostragem.",
                    "Calcular σ = Var(N_s − N_i) / ⟨N_s + N_i⟩ (Eq. 1 do projeto).",
                ],
                "criterio": "σ < 1 documentado com a respectiva incerteza experimental. Esta é a condição obrigatória para qualquer reivindicação de vantagem sub-SNL.",
                "risco": "Go/no-go após C.5: σ ≥ 1 → revisar perdas ópticas e eficiência de detecção antes de continuar.",
            },
        ],
    },
    {
        "id": 6,
        "titulo": "Bloco 6 — Matrizes em soro, revisão do benchmark e medida de g⁽²⁾(0)",
        "prereq": "Bloco 5 concluído. C.5 com σ < 1 confirmado.",
        "gonogo": "g⁽²⁾(0) < 1 foi obtido? Se não → revisar alinhamento HBT e potência de bombeamento.",
        "tarefas": [
            {
                "id": "A.5b", "eixo": "A",
                "titulo": "Testes em soro (A.5 continuação)",
                "objetivo": "Validar a curva de resposta em matriz biológica real.",
                "passos": [
                    "Com a curva em tampão validada, evoluir para soro com o ICB/UFMG.",
                    "Os dados de soro realimentam B.5 para um refinamento do ponto de diluição crítico na matriz real.",
                ],
                "criterio": "Curva de resposta mensurável em soro; dados prontos para realimentar B.5 revisado.",
                "risco": None,
            },
            {
                "id": "B.5r", "eixo": "B",
                "titulo": "Refinar ponto crítico com dados de A.5 em soro (B.5 revisão)",
                "objetivo": "Atualizar o benchmark com os dados experimentais reais da matriz de soro.",
                "passos": [
                    "Inserir os dados experimentais de A.5 (soro) na curva de calibração.",
                    "Recalcular o ponto de diluição crítico na matriz biológica real.",
                ],
                "criterio": "Ponto de diluição crítico final documentado para a matriz de soro.",
                "risco": None,
            },
            {
                "id": "C.6", "eixo": "C",
                "titulo": "Medida de g⁽²⁾(0) via HBT (anti-bunching)",
                "objetivo": "Qualificar a operação no regime de fóton único anunciado.",
                "passos": [
                    "Montar a configuração Hanbury Brown–Twiss: o braço sinal (ou idler) é dividido em dois caminhos (i1, i2) por um divisor de feixe 50:50.",
                    "Medir as coincidências triplas (sinal anunciador + i1 + i2) e duplas (sinal-i1, sinal-i2).",
                    "Calcular g⁽²⁾(0) = R_{s,i1,i2} · R_s / (R_{s,i1} · R_{s,i2}).",
                ],
                "criterio": "g⁽²⁾(0) < 1, idealmente próximo a ~0,1 — confirma anti-bunching e operação no regime de fóton único anunciado.",
                "risco": "Go/no-go após C.6: g⁽²⁾(0) ≥ 1 → revisar alinhamento HBT e potência de bombeamento.",
            },
        ],
    },
    {
        "id": 7,
        "titulo": "Bloco 7 — Convergência: consolidação de todos os insumos para o Eixo D",
        "prereq": "Blocos 5 e 6 concluídos. Este bloco fecha a Fase 1 e prepara a Fase 2.",
        "gonogo": "⚠️ Go/no-go TOTAL antes do Eixo D: A, B e C entregaram todos os seus critérios de aceite? Prosseguir para o Bloco 8 somente com todos confirmados.",
        "tarefas": [
            {
                "id": "AB.7", "eixo": "A",
                "titulo": "Checklist de entregáveis A e B",
                "objetivo": "Verificar que todos os entregáveis de A e B estão documentados.",
                "passos": [
                    "Lote de nanobastões funcionalizado, com LSPR em ~810 nm confirmada.",
                    "Bioconjugação validada por deslocamento espectral (A.4).",
                    "Protocolo de diluição em tampão e soro (A.5).",
                    "Curva de calibração de absorção (B.4).",
                    "Benchmark SNL e ponto de diluição crítico final, na matriz de soro (B.5 revisado).",
                ],
                "criterio": "Todos os cinco itens acima documentados e aprovados.",
                "risco": None,
            },
            {
                "id": "C.7", "eixo": "C",
                "titulo": "Orçamento de erro da fonte",
                "objetivo": "Fechar a qualificação da fonte com todos os parâmetros documentados em um único relatório.",
                "passos": [
                    "Reunir: taxa de pares, eficiência de heralding, σ, g⁽²⁾(0) e suas incertezas.",
                    "Definir os limites de operação seguros para uso da fonte no Eixo D.",
                ],
                "criterio": "Documento de orçamento de erro completo. Sem ele, nenhuma medida do Eixo D é defensável perante um parecerista.",
                "risco": None,
            },
        ],
    },
    {
        "id": 8,
        "titulo": "Bloco 8 — Montagem do arranjo experimental e prova de conceito",
        "prereq": "Bloco 7 completo. Primeiro bloco exclusivo do Eixo D.",
        "gonogo": None,
        "tarefas": [
            {
                "id": "D.1", "eixo": "D",
                "titulo": "Montagem do esquema de diferença de intensidade",
                "objetivo": "Montar o arranjo experimental central da demonstração.",
                "passos": [
                    "Posicionar a amostra de nanobastões funcionalizados no caminho do feixe sinal (feixe-sonda).",
                    "Manter o feixe complementar como referência, sem interagir com a amostra.",
                    "Configurar a detecção para medir a diferença de intensidade entre os dois feixes.",
                ],
                "criterio": "Arranjo montado e alinhado, com σ medido na presença do setup de medida (não apenas na fonte isolada) ainda < 1.",
                "risco": None,
            },
            {
                "id": "D.2", "eixo": "D",
                "titulo": "Primeira medida de absorção sub-shot-noise em tampão",
                "objetivo": "Confirmar que o esquema produz medida com ruído reduzido em condição simples antes de ir para a diluição crítica.",
                "passos": [
                    "Medir a absorção da amostra em tampão em concentração intermediária.",
                    "Comparar a incerteza obtida com o benchmark clássico de B.5, para o mesmo N de fótons-sonda.",
                ],
                "criterio": "Incerteza da medida quântica menor que o benchmark clássico equivalente.",
                "risco": None,
            },
            {
                "id": "D.3", "eixo": "D",
                "titulo": "Controle clássico equivalente",
                "objetivo": "Ter, para cada medida quântica, uma medida-controle estritamente comparável.",
                "passos": [
                    "Substituir a fonte SPDC por um estado coerente (laser) com o mesmo número médio de fótons-sonda.",
                    "Repetir a medida nas mesmas condições experimentais (alinhamento, tempo de integração, eficiência de detecção).",
                ],
                "criterio": "Controle clássico executado nas mesmas condições da medida quântica e registrado.",
                "risco": None,
            },
        ],
    },
    {
        "id": 9,
        "titulo": "Bloco 9 — Série de diluição e estimadores (experimento central)",
        "prereq": "D.1 + D.2 + D.3 concluídos com critérios atingidos. D.4 e D.5 estão acoplados: a análise estatística (D.5) é aplicada a cada lote de medidas de D.4 à medida que os dados chegam.",
        "gonogo": "Cruzamento claro do limiar do SNL nos dados? Se não → estender a série de diluição ou revisar o ponto crítico de B.5.",
        "tarefas": [
            {
                "id": "D.4", "eixo": "D",
                "titulo": "Série de diluição controlada",
                "objetivo": "O experimento central do projeto — atravessar o ponto onde o SNL clássico supera o sinal a ser medido.",
                "passos": [
                    "Preparar uma série de diluições cobrindo concentrações acima e abaixo do ponto de diluição crítico (B.5).",
                    "Para cada concentração: executar medida quântica (esquema D.1) e medida clássica de controle (D.3).",
                    "Registrar variação de sinal e incerteza em cada ponto.",
                ],
                "criterio": "Dados coletados em concentrações suficientes para visualizar claramente o cruzamento do limiar do SNL clássico (ao menos um ponto bem acima, um próximo e um ou mais abaixo do ponto crítico).",
                "risco": None,
            },
            {
                "id": "D.5", "eixo": "D",
                "titulo": "Estimadores otimizados e caracterização de eficiências",
                "objetivo": "Garantir que a reivindicação de vantagem seja estatisticamente não-enviesada.",
                "passos": [
                    "Aplicar estimadores não-enviesados (Losero et al.; Mueller/Samantaray/Matthews) aos dados brutos de D.4.",
                    "Caracterizar de forma independente as eficiências de detecção dos dois canais.",
                ],
                "criterio": "Análise estatística documentada, com orçamento de erro propagado a partir das eficiências medidas.",
                "risco": "Go/no-go após D.4: os dados mostram cruzamento claro do limiar do SNL? Se não → estender a série de diluição ou revisar o ponto crítico de B.5.",
            },
        ],
    },
    {
        "id": 10,
        "titulo": "Bloco 10 — Quantificação da vantagem e trilha complementar",
        "prereq": "D.4 com cruzamento do limiar confirmado; D.5 concluído. D.6 e D.7 podem correr em paralelo — D.7 é opcional e não bloqueia D.6.",
        "gonogo": None,
        "tarefas": [
            {
                "id": "D.6", "eixo": "D",
                "titulo": "Quantificação da vantagem quântica absoluta por fóton",
                "objetivo": "Produzir o resultado central do projeto.",
                "passos": [
                    "Calcular a razão de incertezas (quântico/clássico) no ponto de diluição crítico e ao redor dele.",
                    "Calcular equivalentemente a razão de fótons-sonda necessários para a mesma precisão.",
                    "Comparar com os ganhos já reportados na literatura (Moreau: 1,76×; Dowran: 56%).",
                ],
                "criterio": "Vantagem quântica absoluta por fóton demonstrada com significância estatística (múltiplos desvios-padrão de separação da fronteira clássica), no regime em que a estratégia clássica equivalente falha.",
                "risco": None,
            },
            {
                "id": "D.7", "eixo": "D",
                "titulo": "(Opcional) Detecção em coincidência tipo Kalashnikov",
                "objetivo": "Trilha complementar de rejeição de ruído para amostras fotossensíveis.",
                "passos": [
                    "Se o fluxo precisar ser reduzido por fotossensibilidade da amostra, aplicar detecção em coincidência com janela estreita.",
                    "Rotular explicitamente este resultado como ganho técnico de rejeição de ruído — nunca como evidência de operação abaixo do SNL.",
                ],
                "criterio": "Separação clara e explícita, no relatório final, entre os resultados desta trilha e os de D.6.",
                "risco": None,
            },
        ],
    },
    {
        "id": 11,
        "titulo": "Bloco 11 — Consolidação e redação (todos os eixos encerrados)",
        "prereq": "D.6 concluído; D.7 concluído (se executado). Os dois manuscritos podem ser redigidos em paralelo.",
        "gonogo": None,
        "tarefas": [
            {
                "id": "D.8a", "eixo": "D",
                "titulo": "Manuscrito 1: instrumentação e qualificação da fonte",
                "objetivo": "Publicar os resultados do Eixo C.",
                "passos": [
                    "Consolidar os resultados de C (taxa de pares, heralding, σ, g⁽²⁾(0)) e seu orçamento de erro.",
                    "Redigir o manuscrito com foco na construção, qualificação e caracterização da fonte SPDC em ~810 nm.",
                ],
                "criterio": "Manuscrito finalizado e submetido.",
                "risco": None,
            },
            {
                "id": "D.8b", "eixo": "D",
                "titulo": "Manuscrito 2: vantagem quântica em biossensoriamento plasmônico",
                "objetivo": "Publicar os resultados centrais do projeto (Eixos A, B, D).",
                "passos": [
                    "Consolidar a cadeia completa: síntese (A) → benchmark (B) → demonstração (D).",
                    "Redigir o manuscrito com ênfase na vantagem quântica absoluta por fóton em nanoplataforma plasmônica funcionalizada.",
                ],
                "criterio": "Manuscrito finalizado e submetido.",
                "risco": None,
            },
            {
                "id": "D.8c", "eixo": "D",
                "titulo": "Protocolo replicável",
                "objetivo": "Garantir que qualquer laboratório com a infraestrutura adequada possa reproduzir o experimento.",
                "passos": [
                    "Documentar passo a passo cada eixo (A, B, C, D) com critérios de aceite, decisões de contingência e parâmetros-chave.",
                ],
                "criterio": "Protocolo completo, revisado pelos colaboradores da UFF e do ICB/UFMG.",
                "risco": None,
            },
        ],
    },
]

STATE_FILE = "posdoc_state.json"

# ── Persistência ──────────────────────────────────────────────────────────────
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def get_task_state(state, tid):
    return state.get(tid, {
        "status": "Não iniciado",
        "notas": "",
        "data_inicio": "",
        "data_fim": "",
        "resultado": "",
    })

# ── Métricas ──────────────────────────────────────────────────────────────────
def calc_metrics(state):
    total, done, prog, block_ = 0, 0, 0, 0
    by_eixo = {e: {"total": 0, "done": 0} for e in "ABCD"}
    by_bloco = {}
    for bloco in BLOCOS:
        b_done, b_total = 0, 0
        for t in bloco["tarefas"]:
            s = get_task_state(state, t["id"])["status"]
            total += 1
            b_total += 1
            eixo = t["eixo"] if t["eixo"] in "ABCD" else "A"
            by_eixo[eixo]["total"] += 1
            if s == "Concluído":
                done += 1
                b_done += 1
                by_eixo[eixo]["done"] += 1
            elif s == "Em andamento":
                prog += 1
            elif s == "Bloqueado":
                block_ += 1
        by_bloco[bloco["id"]] = (b_done, b_total)
    return total, done, prog, block_, by_eixo, by_bloco

# ── Relatório em texto ────────────────────────────────────────────────────────
def gerar_relatorio(state):
    total, done, prog, block_, by_eixo, by_bloco = calc_metrics(state)
    pct = round(done / total * 100) if total else 0
    lines = [
        "=" * 70,
        "RELATÓRIO DE PROGRESSO — PÓS-DOUTORADO",
        "Vantagem quântica na detecção óptica de baixas concentrações",
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "=" * 70,
        "",
        f"RESUMO GERAL: {done}/{total} tarefas concluídas ({pct}%)",
        f"  Em andamento: {prog}  |  Bloqueadas: {block_}  |  Não iniciadas: {total - done - prog - block_}",
        "",
        "PROGRESSO POR EIXO:",
    ]
    for eixo, v in by_eixo.items():
        pct_e = round(v["done"] / v["total"] * 100) if v["total"] else 0
        lines.append(f"  {EIXO_LABEL[eixo]}: {v['done']}/{v['total']} ({pct_e}%)")
    lines += ["", "-" * 70, "DETALHAMENTO POR BLOCO", "-" * 70]
    for bloco in BLOCOS:
        b_done, b_total = by_bloco[bloco["id"]]
        status_bloco = "✅ CONCLUÍDO" if b_done == b_total else f"🔄 {b_done}/{b_total}"
        lines += ["", f"{'═'*60}", f"{bloco['titulo']}  [{status_bloco}]", f"{'═'*60}"]
        if bloco["gonogo"]:
            lines.append(f"⚠️  GO/NO-GO: {bloco['gonogo']}")
        for t in bloco["tarefas"]:
            ts = get_task_state(state, t["id"])
            lines += [
                "",
                f"  [{ts['status']}] {t['id']} — {t['titulo']}",
                f"  Eixo: {EIXO_LABEL.get(t['eixo'], t['eixo'])}",
                f"  Objetivo: {t['objetivo']}",
                f"  Critério de aceite: {t['criterio']}",
            ]
            if ts.get("data_inicio"):
                lines.append(f"  Data início: {ts['data_inicio']}")
            if ts.get("data_fim"):
                lines.append(f"  Data conclusão: {ts['data_fim']}")
            if ts.get("resultado"):
                lines.append(f"  Resultado: {ts['resultado']}")
            if ts.get("notas"):
                lines.append(f"  Notas: {ts['notas']}")
    lines += ["", "=" * 70, "FIM DO RELATÓRIO", "=" * 70]
    return "\n".join(lines)

# ── Layout Streamlit ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Acompanhamento Pós-Doc — Vantagem Quântica",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  .eixo-A { border-left: 4px solid #2E86AB; padding-left: 8px; }
  .eixo-B { border-left: 4px solid #A23B72; padding-left: 8px; }
  .eixo-C { border-left: 4px solid #F18F01; padding-left: 8px; }
  .eixo-D { border-left: 4px solid #3BB273; padding-left: 8px; }
  .gonogo-box { background: #fff3cd; border-left: 5px solid #ffc107;
                padding: 10px 14px; border-radius: 4px; margin: 8px 0; }
  .metric-card { background: #f8f9fa; border-radius: 8px; padding: 12px 16px;
                 text-align: center; }
  .bloco-header { background: #e9ecef; border-radius: 6px; padding: 8px 14px;
                  margin-top: 8px; font-weight: 600; }
  .task-done { opacity: 0.65; }
</style>
""", unsafe_allow_html=True)

# ── Estado ──────────────────────────────────────────────────────────────────
if "state" not in st.session_state:
    st.session_state.state = load_state()

state = st.session_state.state

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/UFMG.png/120px-UFMG.png",
             width=80)
    st.markdown("## ⚛️ Pós-Doc Tracker")
    st.caption("Vantagem quântica na detecção óptica\nPNPD/CAPES — UFMG/UFF")
    st.divider()
    pagina = st.radio(
        "Navegação",
        ["📊 Dashboard", "📋 Blocos & Tarefas", "📈 Por Eixo", "🗂️ Relatório"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Legenda de Eixos:**")
    for k, v in EIXO_LABEL.items():
        c = EIXO_COLOR[k]
        st.markdown(
            f'<span style="display:inline-block;width:12px;height:12px;'
            f'background:{c};border-radius:2px;margin-right:6px;"></span>{v}',
            unsafe_allow_html=True,
        )
    st.divider()
    st.markdown("**Status:**")
    for k, v in STATUS_EMOJI.items():
        st.markdown(f"{v} {k}")

total, done, prog, block_, by_eixo, by_bloco = calc_metrics(state)
pct_geral = round(done / total * 100) if total else 0

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if pagina == "📊 Dashboard":
    st.title("⚛️ Acompanhamento de Progresso — Pós-Doc")
    st.caption(
        "Vantagem quântica na detecção óptica de baixas concentrações · PNPD/CAPES · UFMG/UFF"
    )
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("✅ Concluídas", f"{done}/{total}", f"{pct_geral}%")
    with col2:
        st.metric("🔄 Em andamento", prog)
    with col3:
        st.metric("🚫 Bloqueadas", block_)
    with col4:
        st.metric("⬜ Não iniciadas", total - done - prog - block_)

    st.progress(done / total if total else 0, text=f"Progresso geral: {pct_geral}%")
    st.divider()

    # Por eixo
    st.subheader("Progresso por Eixo")
    cols = st.columns(4)
    for i, (eixo, v) in enumerate(by_eixo.items()):
        pct_e = round(v["done"] / v["total"] * 100) if v["total"] else 0
        with cols[i]:
            c = EIXO_COLOR[eixo]
            st.markdown(
                f'<div style="border-top:4px solid {c};border-radius:6px;'
                f'padding:12px;background:#fafafa;">'
                f'<b>{eixo}</b> — {v["done"]}/{v["total"]}<br>'
                f'<small>{EIXO_LABEL[eixo].split("—")[1].strip()}</small>'
                f"</div>",
                unsafe_allow_html=True,
            )
            st.progress(v["done"] / v["total"] if v["total"] else 0, text=f"{pct_e}%")

    st.divider()

    # Mapa de blocos
    st.subheader("Mapa de Blocos")
    for bloco in BLOCOS:
        b_done, b_total = by_bloco[bloco["id"]]
        b_pct = round(b_done / b_total * 100) if b_total else 0
        concluido = b_done == b_total
        bg = "#d4edda" if concluido else ("#fff3cd" if b_done > 0 else "#f8f9fa")
        icone = "✅" if concluido else ("🔄" if b_done > 0 else "⬜")
        st.markdown(
            f'<div style="background:{bg};border-radius:8px;padding:10px 16px;'
            f'margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">'
            f'<span>{icone} <b>Bloco {bloco["id"]}</b> — '
            f'{bloco["titulo"].split("—",1)[1].strip() if "—" in bloco["titulo"] else bloco["titulo"]}</span>'
            f'<span style="font-weight:600;color:#555;">{b_done}/{b_total} ({b_pct}%)</span>'
            f"</div>",
            unsafe_allow_html=True,
        )
        if bloco["gonogo"]:
            gate_ok = all(
                get_task_state(state, t["id"])["status"] == "Concluído"
                for t in bloco["tarefas"]
            )
            cor = "#28a745" if gate_ok else "#dc3545"
            emoji = "🟢" if gate_ok else "🔴"
            st.markdown(
                f'<div class="gonogo-box">{emoji} <b>Go/No-Go:</b> '
                f'<span style="color:{cor};">{"APROVADO" if gate_ok else "PENDENTE"}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )

# ══════════════════════════════════════════════════════════════════════════════
# BLOCOS & TAREFAS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📋 Blocos & Tarefas":
    st.title("📋 Blocos & Tarefas")

    bloco_sel = st.selectbox(
        "Selecionar bloco",
        options=[b["id"] for b in BLOCOS],
        format_func=lambda x: next(b["titulo"] for b in BLOCOS if b["id"] == x),
    )
    bloco = next(b for b in BLOCOS if b["id"] == bloco_sel)
    st.divider()

    st.subheader(bloco["titulo"])
    st.info(f"**Pré-requisito:** {bloco['prereq']}")
    if bloco["gonogo"]:
        st.warning(f"⚠️ **Gate Go/No-Go:** {bloco['gonogo']}")
    st.divider()

    for t in bloco["tarefas"]:
        ts = get_task_state(state, t["id"])
        eixo = t["eixo"] if t["eixo"] in "ABCD" else "A"
        cor = EIXO_COLOR[eixo]

        with st.expander(
            f"{STATUS_EMOJI[ts['status']]} **{t['id']}** — {t['titulo']}",
            expanded=(ts["status"] in ("Em andamento", "Não iniciado")),
        ):
            st.markdown(
                f'<div class="eixo-{eixo}" style="border-left-color:{cor}">'
                f"<small>Eixo: <b>{EIXO_LABEL.get(eixo, eixo)}</b></small>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**Objetivo:** {t['objetivo']}")
            st.markdown("**Passos:**")
            for i, p in enumerate(t["passos"], 1):
                st.markdown(f"&nbsp;&nbsp;&nbsp;{i}. {p}")
            st.markdown(f"**Critério de aceite:** _{t['criterio']}_")
            if t.get("risco"):
                st.warning(f"**Risco / Atenção:** {t['risco']}")

            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                novo_status = st.selectbox(
                    "Status",
                    list(STATUS_EMOJI.keys()),
                    index=list(STATUS_EMOJI.keys()).index(ts["status"]),
                    key=f"status_{t['id']}",
                )
            with c2:
                data_inicio = st.text_input(
                    "Data início (dd/mm/aaaa)",
                    value=ts.get("data_inicio", ""),
                    key=f"di_{t['id']}",
                )
            data_fim = st.text_input(
                "Data conclusão (dd/mm/aaaa)",
                value=ts.get("data_fim", ""),
                key=f"df_{t['id']}",
            )
            resultado = st.text_area(
                "Resultado / valor medido",
                value=ts.get("resultado", ""),
                key=f"res_{t['id']}",
                height=68,
            )
            notas = st.text_area(
                "Notas & observações",
                value=ts.get("notas", ""),
                key=f"notas_{t['id']}",
                height=80,
            )

            if st.button(f"💾 Salvar {t['id']}", key=f"save_{t['id']}"):
                state[t["id"]] = {
                    "status": novo_status,
                    "notas": notas,
                    "data_inicio": data_inicio,
                    "data_fim": data_fim,
                    "resultado": resultado,
                }
                save_state(state)
                st.session_state.state = state
                st.success("Salvo!")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# POR EIXO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📈 Por Eixo":
    st.title("📈 Visão por Eixo")

    eixo_sel = st.selectbox(
        "Selecionar eixo",
        list(EIXO_LABEL.keys()),
        format_func=lambda x: EIXO_LABEL[x],
    )
    cor = EIXO_COLOR[eixo_sel]
    st.markdown(
        f'<div style="border-left:6px solid {cor};padding:6px 14px;'
        f'font-size:1.1rem;font-weight:600;">{EIXO_LABEL[eixo_sel]}</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    tarefas_eixo = [
        (bloco, t)
        for bloco in BLOCOS
        for t in bloco["tarefas"]
        if (t["eixo"] if t["eixo"] in "ABCD" else "A") == eixo_sel
    ]
    concluidas = sum(
        1 for _, t in tarefas_eixo
        if get_task_state(state, t["id"])["status"] == "Concluído"
    )
    st.progress(
        concluidas / len(tarefas_eixo) if tarefas_eixo else 0,
        text=f"{concluidas}/{len(tarefas_eixo)} concluídas",
    )
    st.divider()

    for bloco, t in tarefas_eixo:
        ts = get_task_state(state, t["id"])
        with st.expander(
            f"**Bloco {bloco['id']}** · {STATUS_EMOJI[ts['status']]} {t['id']} — {t['titulo']}",
            expanded=False,
        ):
            st.markdown(f"**Objetivo:** {t['objetivo']}")
            st.markdown(f"**Critério:** _{t['criterio']}_")
            st.markdown(f"**Status atual:** {STATUS_EMOJI[ts['status']]} {ts['status']}")
            if ts.get("resultado"):
                st.markdown(f"**Resultado:** {ts['resultado']}")
            if ts.get("notas"):
                st.markdown(f"**Notas:** {ts['notas']}")

# ══════════════════════════════════════════════════════════════════════════════
# RELATÓRIO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🗂️ Relatório":
    st.title("🗂️ Relatório Final")
    st.caption("Gera um texto completo com status de todas as tarefas, datas e resultados.")
    st.divider()

    relatorio = gerar_relatorio(state)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Prévia")
    with col2:
        st.download_button(
            label="⬇️ Baixar .txt",
            data=relatorio.encode("utf-8"),
            file_name=f"relatorio_posdoc_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )

    st.text_area("", value=relatorio, height=600, label_visibility="collapsed")

    st.divider()
    st.subheader("Exportar estado (JSON)")
    st.download_button(
        label="⬇️ Baixar estado JSON",
        data=json.dumps(state, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name=f"estado_posdoc_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
    )
    st.caption(
        "Guarde este arquivo para restaurar o progresso em outra máquina "
        "(coloque-o na mesma pasta que o script com o nome `posdoc_state.json`)."
    )
