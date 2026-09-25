---
name: power-bi-pbip
description: Edita projetos Power BI no formato PBIP (relatório PBIR em JSON + modelo semântico TMDL) direto nos arquivos, com validação antes de abrir no Power BI Desktop. Use SEMPRE que a tarefa envolver arquivos .pbip, pastas .Report/.SemanticModel, visual.json, page.json, pages.json, arquivos .tmdl, medidas DAX em TMDL, relacionamentos, ou pedidos como "cria um card/gráfico/página no dashboard", "muda a cor do visual", "adiciona uma medida", "conserta o relatório que não abre no Desktop", "edita o Power BI pelo código", mesmo que o usuário não diga "PBIP" ou "PBIR". Também use para revisar ou depurar erros de carregamento do Desktop (UnknownKeyword, Indentation, schema) em projetos PBIP.
---

# Edição de projetos Power BI (PBIP)

Um projeto PBIP é o `.pbix` "aberto" em pastas de texto:

```
projeto.pbip
├── projeto.Report/definition/          ← PBIR: JSON, um arquivo por página/visual
│   ├── report.json, version.json
│   └── pages/pages.json, pages/<pageId>/page.json, pages/<pageId>/visuals/<visualId>/visual.json
└── projeto.SemanticModel/definition/   ← TMDL: texto indentado com TAB
    ├── model.tmdl, database.tmdl, relationships.tmdl
    └── tables/<tabela>.tmdl
```

O Power BI Desktop é implacável com esses arquivos: um erro de schema ou de indentação impede o projeto de abrir, e alguns erros são **silenciosos** (o Desktop descarta a propriedade e a formatação some). Por isso o fluxo abaixo termina sempre em validação.

## Ferramentas oficiais da Microsoft (use se estiverem disponíveis)

A Microsoft publica skills e ferramentas oficiais em `microsoft/skills-for-fabric` (plugin `powerbi-authoring`, compatível com Claude Code). Antes de editar arquivos na mão, verifique se há algo disso na sessão:

- **MCP `powerbi-modeling-mcp`** (Power BI Authoring MCP): se estiver conectado ao modelo, use-o para tabelas, colunas, medidas e relacionamentos. Ele edita o modelo vivo e roda DAX para testar a medida, o que é mais seguro do que escrever TMDL na mão.
- **CLI `powerbi-report-author`** (`npm @microsoft/powerbi-report-authoring-cli`): tem `validate` oficial de PBIR e `preview` com screenshot. Se existir, rode-o além do validador desta skill.
- **Power BI Desktop Bridge**: recarrega o projeto aberto no Desktop após edição externa.

Nada disso roda em sessão na nuvem (precisam de Windows + Desktop). Sem elas, edite os arquivos seguindo esta skill. Se o usuário quiser instalar: no Claude Code local, `/plugin marketplace add microsoft/skills-for-fabric` e depois `/plugin install powerbi-authoring@fabric-collection`.

## Fluxo de trabalho

1. **Localize e leia antes de escrever.** Encontre o `.pbip`, leia `definition.pbir` (qual modelo o relatório usa) e 1–2 `visual.json` parecidos com o que vai criar. Copiar a estrutura de um visual que já funciona no mesmo projeto é o caminho mais confiável.
2. **Espelhe as versões de `$schema` existentes.** Cada arquivo declara um schema versionado (ex.: `visualContainer/2.7.0`). Use a mesma versão que o projeto já usa, não a mais nova que você conhece: um schema mais novo que o Desktop instalado dá erro "This report was edited in a newer version".
3. **Confirme os nomes reais no modelo.** Todo campo em visual referencia `Entity` (tabela) + `Property` (coluna ou medida) com o nome exato do TMDL. Grep em `tables/*.tmdl` antes de usar. Coluna e medida usam wrappers diferentes (`"Column"` vs `"Measure"`); trocar um pelo outro quebra o visual.
4. **Edite** seguindo as regras abaixo e o arquivo de referência do assunto. Mexa só no que a tarefa pede.
   - Se incluir um visual exigir rearranjar outros (linha de cards cheia, por exemplo), proponha o layout ao usuário antes. Se ele já pediu o resultado final, faça e deixe claro no relatório quais visuais existentes mudaram de posição ou tamanho.
   - Ao inserir um visual, dê `tabOrder` coerente com a ordem de leitura e `z` acima do fundo. O Desktop renumera tudo ao salvar, então não precisa ser perfeito.
   - Achou um erro que **já existia** (ex.: o validador acusa algo que você não tocou)? Se ele impede o projeto de abrir, corrija e avise em destaque. Se não, só avise e pergunte.
5. **Valide:** `python <skill>/scripts/validate_pbip.py <pasta do projeto>`. Corrija todo `[ERRO]`. Leia os `[AVISO]` e decida.
6. **Informe o usuário** (formato na última seção), incluindo que ele precisa fechar e reabrir o projeto no Desktop (ou usar o Bridge) para ver a mudança.

O arquivo em disco é a fonte da verdade. Se o usuário tiver alterações não salvas no Desktop, elas serão perdidas ou sobrescritas; peça para salvar e fechar antes de editar. Se o projeto está em git, sugira commit antes de mudanças grandes, para facilitar reverter.

## Regras que mais quebram projetos

**Cores precisam de expressão Literal com aspas simples.** `"color": "#162447"` é ignorado em silêncio (o Desktop troca por cor do tema). O correto:
```json
"color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#162447'" } } } } }
```
Exceção única: textbox, em `textRuns[].textStyle.color`, usa CSS puro (`"#162447"`).

**Literais têm sufixo de tipo.** Números decimais levam `D` (`"12D"`, `"0D"`), inteiros `L` (`"3L"`), texto vai entre aspas simples (`"'Segoe UI'"`), booleano puro (`"true"`). É o formato que o Desktop gera; sem ele, o valor pode ser rejeitado ou ignorado.

**TMDL é indentado com TAB**, igual Python: o nível define a quem a linha pertence. `table` fica em 0 tabs, `column`/`measure`/`partition` em 1, propriedades em 2. Em DAX multilinha, use o bloco com crases (é o que o Desktop gera):
```tmdl
	measure 'Taxa Vigência' = ```
		VAR _v = [Instrumentos Vigentes]
		RETURN DIVIDE(_v, [Total Instrumentos])
		```
		formatString: 0.0%
		displayFolder: 01 KPIs
		lineageTag: 3f2a...-...
```
Sem crases, a expressão precisa ficar um nível **mais fundo** que `lineageTag`; senão o `lineageTag` vira DAX e dá erro. Strings HTML longas em DAX: mantenha numa linha só ou concatene com `&`; tabs/quebras literais dentro da string confundem o parser TMDL.

**`lineageTag` é opcional em objeto novo** (o Desktop gera ao salvar). Se incluir, use um GUID real e único: `python -c "import uuid;print(uuid.uuid4())"`. Nunca invente padrões com caracteres fora de hex nem reutilize tags. **Toda medida deve ter `formatString`.** Para percentual, use `DIVIDE(a, b)` com `formatString: 0.0%`, sem `* 100`.

**Comentário `//` não existe em TMDL** (só dentro do código DAX/M). Para documentar um objeto, use `///` na linha acima da declaração: vira a descrição que aparece no Desktop.

**Palavras-chave que não existem em TMDL** (erro `UnknownKeyword`): `isDataTable`, `cardinality: manyToOne` (muitos-para-um é o padrão, omita; só existe `toCardinality: many`), `calculatedTable` (use `partition X = calculated` com `source =`).

**Nomes de pasta e `name`** de páginas e visuais: só letras, dígitos, `_` ou `-`, e o `name` do JSON igual ao nome da pasta. Fora disso o Desktop ignora a pasta sem avisar. Nomes descritivos (`card_vigentes`, `bar_tipos`) são permitidos e facilitam a manutenção.

**Página nova só aparece se estiver em `pages.json` → `pageOrder`.**

**LocalDateTable órfã:** o Desktop lê *todo* `.tmdl` em `tables/`, com ou sem `ref table` no `model.tmdl`. Ao remover um relacionamento de data, remova também o bloco `variation` da coluna e **apague o arquivo** `LocalDateTable_<guid>.tmdl`.

**Arquivos que não devem ser editados fora do Desktop:** `definition.pbir`, `report.json` no formato PBIR-Legacy (relatório sem pasta `definition/`), `mobileState.json`, `semanticModelDiagramLayout.json`, `.pbi/cache.abf`. Se o relatório estiver em PBIR-Legacy, peça ao usuário para ativar o PBIR no Desktop (*Opções > Recursos de visualização > Store reports using enhanced metadata format*) e salvar de novo.

**Encoding:** UTF-8 **sem BOM**. Preserve o final de linha que o arquivo já usa (CRLF ou LF); converter em massa gera diffs enormes no git. Em JSON, mantenha a indentação de 2 espaços.

**O Desktop normaliza ao salvar.** Ele renumera `z`/`tabOrder` em passos de 1000, adiciona `filterConfig`, reindenta o JSON etc. Diffs desse tipo depois de abrir e salvar são esperados, não são erro seu.

## Onde mexer para cada tarefa

| Tarefa | Arquivos |
|---|---|
| Nova página | `pages/<id>/page.json` + incluir `<id>` em `pages/pages.json` |
| Novo visual | `pages/<página>/visuals/<id>/visual.json` |
| Formatar visual (cor, fonte, borda, título) | `visual.json` → `visual.objects` (específico do tipo) ou `visual.visualContainerObjects` (moldura: background, border, title, dropShadow, padding) |
| Nova medida | `tables/_Medidas.tmdl` (ou a tabela de medidas do projeto) |
| Coluna calculada | `tables/<tabela>.tmdl` |
| Nova tabela | `tables/<nome>.tmdl` + `ref table` em `model.tmdl` |
| Relacionamento | `relationships.tmdl` (GUID novo como nome) |
| Fonte de dados / Power Query | bloco `partition <nome> = m` da tabela |
| Tema | `report.json` → `themeCollection` + arquivo em `StaticResources/` |

## Referências: leia só a do assunto

| Arquivo | Quando ler |
|---|---|
| `references/pbir-report.md` | Criar ou formatar visuais (card, cardVisual, gráficos, tableEx, slicer, textbox, shape, imagem, grupos), selectors e formatação condicional, bookmarks, botões/navegação, páginas, schemas |
| `references/tmdl-model.md` | Medidas, colunas calculadas, tabelas calculadas, partições M (SharePoint etc.), relacionamentos, `model.tmdl`, time intelligence, displayFolder |
| `references/html-deneb-visuals.md` | Visual HTML Content, Deneb/Vega-Lite, SVG em DAX, animações CSS, registro de custom visuals |
| `references/design-layout.md` | Layout de página, grids, paletas, padrões de dashboard, storytelling |

São arquivos longos com índice no topo: use grep pelo tipo de visual ou propriedade em vez de ler tudo. Eles registram experimentos em projetos de várias versões do Desktop. **Quando um exemplo da referência divergir de um visual que já funciona no projeto atual (nomes de objetos de formatação, versão de schema), siga o projeto.** O cabeçalho de cada referência lista as erratas conhecidas.

## Convenções dos projetos TJBA

Estas convenções vêm do projeto `nucleo_de_convenios_tjba`. Confira se valem para o projeto atual antes de aplicar.

- Modelo em `pt-BR` (`culture`/`sourceQueryCulture`). Nomes de medidas em português, com acentos e espaços (entre aspas simples no TMDL).
- Fonte de dados: listas do SharePoint via `SharePoint.Tables(...)`. Colunas de pesquisa (lookup) aparecem como `campo.lookupValue` e pessoas como `campo.title`/`campo.email`: use esses nomes exatos como `Property`.
- Medidas centralizadas em `_Medidas`, organizadas com `displayFolder` numerado (`01 KPIs`, `03 Tendencias`…).
- Visual claro: página `#F1F5F9`, cards brancos `#FFFFFF` com borda `#E2E8F0`, `radius` 12D, sombra ligada, título do container oculto; texto secundário `#64748B`. Cada card KPI tem uma cor de destaque própria (`#3B82F6`, `#059669`, …). Antes de escolher uma cor nova, veja as já usadas na página para não repetir a cor de outro KPI com outro significado.
- `cardVisual` (card novo) neste projeto usa os objetos `calloutValue`, `label` e `accent`. Copie de `card_vigentes`.
- Canvas 1280×720, `displayOption: FitToPage`.

## Como reportar o resultado ao usuário

Termine com um resumo curto:
1. **O que mudou.** Arquivos criados ou alterados, um por linha, com o motivo.
2. **Validação.** Saída resumida do `validate_pbip.py` (e do `powerbi-report-author validate`, se rodou).
3. **Próximo passo no Desktop.** "Feche e reabra o `.pbip`" (ou recarregue pelo Bridge). Diga o que conferir visualmente e qualquer coisa que só dá para testar com dados (ex.: resultado de uma medida nova).
