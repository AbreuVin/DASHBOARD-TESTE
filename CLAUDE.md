# Controle de Demandas · CGPRES — contexto para o Claude Code

Painel Power BI do **Controle de Demandas da CGPRES** (Chefia de Gabinete da Presidência, TJBA),
salvo no formato **PBIP** (arquivos de texto: JSON para o relatório, TMDL para o modelo).
O Power BI Desktop é usado só para abrir, atualizar e conferir; toda a edição é feita nos arquivos.

## Estrutura

```
controle_demandas_cgpres.pbip                 ← abrir no Power BI Desktop
controle_demandas_cgpres.md                   ← regras de negócio e colunas esperadas
controle_demandas_cgpres.SemanticModel/
  definition/model.tmdl                       ← lista de tabelas (ref table)
  definition/relationships.tmdl
  definition/tables/diligencias.tmdl          ← fato: Power Query + colunas calculadas + medidas
  definition/tables/metas.tmdl                ← metas mensais (Power Query)
  definition/tables/calendario.tmdl           ← tabela calculada DAX
controle_demandas_cgpres.Report/
  definition/report.json, pages/pages.json
  definition/pages/<pagina>/page.json
  definition/pages/<pagina>/visuals/<visual>/visual.json
  StaticResources/RegisteredResources/CGPRES_TJBA.json   ← tema
```

Páginas: `visao_geral`, `metas`, `diligencias`.

## A lista do SharePoint (fonte real)

- Site: `https://tjbacotec.sharepoint.com/sites/CGPRES-ControledeDemandas`
- Lista: `/sites/CGPRES-ControledeDemandas/Lists/ControleDemandas`

| Nome de exibição | Nome interno | Tipo | Uso no painel |
| --- | --- | --- | --- |
| Título | `Title` | Texto | — |
| Processo SEI | `processoSEI` | Texto | identificação |
| Processo Externo | `processoExterno` | Texto | detalhe |
| Tipo de Diligência | `tipoDiligencia` | **Múltipla escolha** | filtro e gráfico por tipo |
| Origem | `origem` | Escolha | filtro/gráfico extra |
| Meio de Recebimento | `meioRecebimento` | Escolha | detalhe |
| Interessado | `interessado` | Texto | detalhe |
| Objeto | `objeto` | **Múltipla escolha** | barras dentro/fora do prazo por objeto |
| Observação | `observacao` | Várias linhas | não usar no painel |
| Data de Entrada | `dataEntrada` | Data | período, recebidas por mês |
| Prazo (Dias) | `prazo` | Número | data-limite = dataEntrada + prazo (a confirmar) |
| Unidade Destino | `Unidade_x0020_Destino` | Escolha | filtro/gráfico extra |
| Prioridade | `Prioridade` | Sim/Não | filtro "Prioritária / Normal" |
| Data de Conclusão do Processo | `dataFinalizacao` | Data | vazia = em andamento |
| Prazo para Orientação Complementar | `prazoOrientacaoComplementar` | Data | significado a confirmar |

Opções das colunas de escolha:
- **tipoDiligencia:** Informações; Decisão Judicial; Orientação; Envio de documentos; Mandado de Citação; Notificação; Providências administrativas; Solicitações provenientes de outros órgãos; Outros
- **objeto:** Gratificação por Condições Especiais de Trabalho (CET); Gratificação de Atividade Externa (GAE); Imposto de Renda (IR); Adicional de Função Incorporado (AFI); Substituição; Concurso 2023; Concurso 2014; Concurso Diverso; Outro
- **origem:** PGE; GPRES; Órgão Especial; AEP-I; AEP-II; TRT; Juízo; MP; CNJ; Outra
- **meioRecebimento:** Email; Malote; SEI; Ofício; Outros

As colunas calculadas da lista ainda não foram levantadas (a consulta usada filtrou `ReadOnlyField eq false`).

## Pendências (perguntar ao usuário antes de assumir)

1. **Prazo (Dias):** conta a partir da Data de Entrada? Dias corridos ou úteis? É o prazo externo?
2. **Prazo interno:** o e-mail pede prazo interno e externo diferenciados; a lista não tem um prazo
   interno claro. "Prazo para Orientação Complementar" é o prazo interno?
3. **Prioridade:** Sim/Não basta, ou querem níveis (Alta/Média/Baixa)? Se níveis, a mudança é na lista.

## Regras já decididas

- As quatro situações (Entregue no prazo, Entregue com atraso, Em andamento no prazo, Em andamento
  com prazo vencido) são calculadas **no Power BI**, contra o prazo externo, porque dependem de HOJE.
  Coluna do SharePoint com HOJE só recalcula quando o item é editado.
- Status: Finalizada se há data de conclusão; senão Em tramitação.
- Metas comparadas pelo **mês da conclusão** (relação inativa `dataEntrega → calendario`, usada com
  `USERELATIONSHIP`). O resto usa o mês de entrada.
- Múltipla escolha (tipo, objeto): criar tabelas-ponte (`diligenciaTipo`, `diligenciaObjeto`: ID + valor)
  ligadas a `diligencias[ID]` com filtro cruzado nos dois sentidos. Avisar no painel que a soma das
  barras pode passar do total.
- Manter os dados fictícios disponíveis: parâmetro `UsarDadosFicticios` (true/false) escolhe entre a
  consulta fictícia e `SharePoint.Tables`. Como os nomes de coluna devolvidos pelo conector podem ser
  o de exibição ou o interno, renomear com `Table.RenameColumns(..., MissingField.Ignore)` cobrindo os dois.

## Regras de edição PBIP (aprendidas na prática)

- **Cores em visual.json:** sempre `{"solid":{"color":{"expr":{"Literal":{"Value":"'#RRGGBB'"}}}}}`
  (hex entre aspas simples). Hex solto como string é ignorado em silêncio. Exceção: `textStyle` de
  textbox usa string simples (`"color": "#111827"`).
- Todo valor de propriedade usa `{"expr":{"Literal":{"Value":...}}}`: números com sufixo `D` (`"12D"`),
  booleanos `"true"`, textos entre aspas simples.
- `cardVisual` usa o papel `Data`; objetos com `"selector": {"id": "default"}`.
- **TMDL:** tabulações, não espaços. Medida/coluna em 1 tab, propriedades em 2 tabs, DAX de várias
  linhas em 3 tabs. Se o DAX ficar no mesmo nível do `lineageTag`, o Power BI lê o `lineageTag` como DAX.
- `lineageTag` precisa ser um GUID único. Tabela nova → adicionar `ref table` em `model.tmdl`.
- Página nova → pasta em `pages/` + entrada em `pages/pages.json`.
- Mexer em JSON com um script (Python `json`), nunca com substituição de texto às cegas.
- Depois de editar, validar os JSON contra os schemas oficiais em
  https://github.com/microsoft/json-schemas (`fabric/item/report/definition/...`).

## Identidade visual

Fundo `#F4F5F7`; cartões brancos com borda 1px `#E4E7EC`, raio 8, **sem sombra**; texto `#111827`,
secundário `#5F6368`; cor única nos dados `#1F4E8C`; status: no prazo `#247B50`, atraso `#92400E`,
vencido `#B42318`; meta em cinza `#C9CED6`. Fonte Segoe UI. Rótulo cinza acima do número nos
indicadores; nada de ícones decorativos, gradientes ou cores por barra sem significado.

## Cuidados

- Não copiar dados reais da lista (nomes, processos) para arquivos versionados, prompts ou mensagens.
  Trabalhar com a estrutura; os dados ficam no SharePoint e no cache local do Power BI.
- `.pbi/localSettings.json` e `.pbi/cache.abf` são locais; não editar à mão.
- Fechar o projeto no Power BI Desktop antes de editar os arquivos e reabrir depois. O Desktop
  sobrescreve as alterações externas quando salva.
