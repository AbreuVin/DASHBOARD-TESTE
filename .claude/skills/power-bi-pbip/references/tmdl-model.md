# Modelo semântico TMDL — sintaxe, relacionamentos, medidas DAX

> Extraído de `pbir_research_and_learnings.md` (aprendizados práticos em projetos TJBA). Seções mantidas na íntegra; a numeração original foi preservada.

> **Erratas (conferidas com a documentação oficial de TMDL da Microsoft):**
> - Comentários `// ...` que aparecem em exemplos TMDL abaixo (ex.: seção 18) **não são válidos** fora de expressões DAX/M: são só anotações didáticas. Use `///` para descrição.
> - Alguns exemplos (ex.: seção 37) estão indentados com espaços por formatação do markdown. Em arquivo `.tmdl` real, use TAB.
> - Profundidade do DAX multilinha: **sem crases**, a expressão fica um nível abaixo das propriedades (ex.: 3 tabs para medida em tabela). **Com crases**, o conteúdo é lido literalmente e pode ficar no nível das propriedades, que é o que o Desktop gera.
> - Onde houver `DIVIDE(...) * 100`, isso é para exibir o número em HTML/texto. Para medida exibida como percentual, use `DIVIDE(...)` com `formatString: 0.0%`.
> - `lineageTag` é opcional ao criar objetos novos.

## Índice

- 3. TMDL Syntax Patterns
- 3.1. Relationships (relationships.tmdl)
- 3.2. model.tmdl Extended Reference
- 18. Semantic Model Patterns (TMDL)
- Section 31: Best Practices for Programmatic Generation of PBIR & TMDL
- 37. `displayFolder` em Medidas TMDL
- 39. DAX Time Intelligence — Biblioteca Completa (Projeto Databricks Gov)
- Seção 46 — Padrões de Medidas DAX
- Seção 52 — Arquivos Completos do SemanticModel para Mode C (CSV/Excel)

---

## 3. TMDL Syntax Patterns

### Calculated Tables

> [!WARNING]
> The keyword `calculatedTable` does NOT exist in TMDL. Use a `partition` block.

```tmdl
table SampleData
    lineageTag: <guid>

    column MyColumn
        lineageTag: <guid>
        isNameInferred
        sourceColumn: [MyColumn]

    measure MyMeasure = SUM(SampleData[Value])
        formatString: #,##0
        lineageTag: <guid>

    partition SampleData = calculated
        mode: import
        source =
                DATATABLE(
                    "MyColumn", STRING,
                    "Value", DOUBLE,
                    {
                        {"Row1", 100},
                        {"Row2", 200}
                    }
                )
```

Key discoveries:
- Use `partition <name> = calculated` + `source =` (not `expression =`)
- Columns use `isNameInferred` + `sourceColumn: [ColumnName]` (with brackets)
- PBI auto-generates `lineageTag` GUIDs for columns on first load
- PBI removes `dataType` from columns — they're inferred from the calculated table

### Multi-line DAX Measures

> [!WARNING]
> `lineageTag` at the same indentation as expression lines gets parsed as DAX!

```tmdl
# ❌ Wrong — lineageTag parsed as part of DAX expression
    measure MyMeasure =
        VAR x = 1
        RETURN x
        lineageTag: <guid>

# ✅ Correct — expression at 3 tabs, properties at 2 tabs
    measure MyMeasure =
            VAR x = 1
            RETURN x
        lineageTag: <guid>
```

**Rule**: Multi-line expressions must be indented **one level deeper** than properties to disambiguate from TMDL keywords.

### Backtick-Fenced DAX Syntax (Discovered in Governança BI)

> [!IMPORTANT]
> Power BI Desktop uses **triple backticks** (`` ``` ``) to fence multi-line DAX in both measures and calculated table partitions. This is an alternative to the indentation-based approach above.

```tmdl
	measure 'Disponibilidade %' = ```
		VAR MinutosIndisponiveisNoContexto = [Total Minutos Indisponíveis]
		VAR DiasNoContexto = COUNTROWS('dCalendario')
		VAR TotalMinutosNoContexto = DiasNoContexto * 1440
		RETURN
		    IF(
		        DiasNoContexto = 0,
		        BLANK(),
		        1 - DIVIDE( MinutosIndisponiveisNoContexto, TotalMinutosNoContexto )
		    )
		```
		formatString: 0.00%;-0.00%;0.00%
		lineageTag: <guid>
```

Also works for calculated table partitions:
```tmdl
	partition dCalendario = calculated
		mode: import
		source = ```
			VAR MinhaDataMinima = MIN('Tabela'[Data])
			VAR MinhaDataMaxima = MAX('Tabela'[Data])
			RETURN
			    ADDCOLUMNS(
			        CALENDAR(MinhaDataMinima, MinhaDataMaxima),
			        "Ano", YEAR([Date]),
			        "Mês Num", MONTH([Date]),
			        "Nome Mês", FORMAT([Date], "mmmm")
			    )
			```
```

> [!TIP]
> The backtick syntax is what PBI Desktop generates when it saves. Both approaches (backticks and indentation-only) work correctly.

### Power Query/M Partitions (`partition = m`)

> [!IMPORTANT]
> Real data sources (SharePoint, SQL, Excel, etc.) use `partition = m` with Power Query/M code — NOT `partition = calculated`.

```tmdl
	partition 'MeuDados' = m
		mode: import
		source =
			let
			    Fonte = SharePoint.Tables("https://site.sharepoint.com/sites/MeuSite", [Implementation="2.0", ViewMode="All"]),
			    #"tabela-id" = Fonte{[Id="tabela-guid-aqui"]}[Items],
			    #"Colunas Removidas" = Table.RemoveColumns(#"tabela-id", {"ID", "Título", "Modificado", "Criado"}),
			    #"Tipo Alterado" = Table.TransformColumnTypes(#"Colunas Removidas", {{"Data", type date}, {"Valor", Int64.Type}})
			in
			    #"Tipo Alterado"

	annotation PBI_NavigationStepName = Navegação
	annotation PBI_ResultType = Table
```

**Partition types**: `calculated` (DAX/DATATABLE), `m` (Power Query/M)

### Calculated Columns (Inline DAX)

Calculated columns use inline DAX directly in the column definition:
```tmdl
	column '% Executado' = 'MinhaTabela'[REALIZADO] / 'MinhaTabela'[PREVISTO]
		formatString: 0.00%;-0.00%;0.00%
		lineageTag: <guid>
		summarizeBy: sum
		annotation SummarizationSetBy = Automatic

	column 'Data Chave' = DATE([ANO], 1, 1)
		formatString: General Date
		lineageTag: <guid>
		summarizeBy: none
		annotation SummarizationSetBy = Automatic
```

### Column Properties (Full Reference)

| Property | Example | Notes |
|----------|---------|-------|
| `dataType` | `string`, `int64`, `double`, `decimal`, `dateTime` | Data type |
| `formatString` | `0`, `0.00%`, `#,0.00`, `Long Date`, `General Date` | Display format |
| `lineageTag` | `<guid>` | Unique identifier |
| `summarizeBy` | `sum`, `none` | Default aggregation |
| `sourceColumn` | `Column Name` | Source column name (without brackets for M sources) |
| `isNameInferred` | (flag) | Auto-inferred name (calculated tables only) |
| `sortByColumn` | `'Mês Num'` | Sort this column by another |
| `dataCategory` | `Years`, `Months`, `DayOfMonth`, `PaddedDateTableDates` | Semantic category |
| `isHidden` | (flag) | Column is hidden from users |
| `changedProperty` | `= DataType`, `= IsHidden`, `= SortByColumn` | Tracks manual changes |

### `variation` Block (Date Column Auto-Hierarchy)

Date columns auto-generate local date tables via `variation`:
```tmdl
	column 'Data Início'
		dataType: dateTime
		formatString: Long Date
		lineageTag: <guid>
		summarizeBy: none
		sourceColumn: Data Início
		variation Variation
			isDefault
			relationship: <relationship-guid>
			defaultHierarchy: LocalDateTable_<guid>.'Hierarquia de datas'
		annotation SummarizationSetBy = Automatic
		annotation UnderlyingDateTimeDataType = Date
```

### `hierarchy` Block (Date Hierarchies)

```tmdl
	hierarchy 'Data da Resposta Hierarquia'
		lineageTag: <guid>

		level 'Data da Resposta'
			lineageTag: <guid>
			column: 'Data da Resposta'

		changedProperty = IsHidden
```

System date tables have a standard 4-level hierarchy:
```tmdl
	hierarchy 'Hierarquia de datas'
		lineageTag: <guid>

		level Ano
			lineageTag: <guid>
			column: Ano

		level Trimestre
			lineageTag: <guid>
			column: Trimestre

		level Mês
			lineageTag: <guid>
			column: Mês

		level Dia
			lineageTag: <guid>
			column: Dia

		annotation TemplateId = DateHierarchy
```

### Table-Level Properties

| Property | Notes |
|----------|-------|
| `isHidden` | Table hidden from users |
| `isPrivate` | System table (e.g., DateTableTemplate) |
| `showAsVariationsOnly` | Auto-generated local date tables |
| `changedProperty = IsHidden` | Tracks manual hide |

> [!WARNING]
> **`isDataTable` does NOT exist in TMDL.** Using it causes `UnknownKeyword` parse error.
> "Mark as date table" is done via Power BI Desktop UI (Modelagem → Marcar como tabela de datas)
> or via annotation. The `dataCategory: Time` on the date column is the only TMDL-side config needed.

> [!WARNING]
> **Power BI reads ALL `.tmdl` files in `tables/`, not just those referenced in `model.tmdl`.**
> If a LocalDateTable file with `showAsVariationsOnly` exists on disk but has no `variation` pointing
> to it (e.g. after you delete the relationship), Power BI will error even if you removed its `ref`
> from `model.tmdl`. Fix: **delete the `.tmdl` file from disk**.

### Annotations (Metadata)

Common PBI-generated annotations:
```tmdl
	annotation SummarizationSetBy = Automatic
	annotation PBI_FormatHint = {"isGeneralNumber":true}
	annotation PBI_FormatHint = {"isDateTimeCustom":true}
	annotation PBI_FormatHint = {"currencyCulture":"pt-BR"}
	annotation UnderlyingDateTimeDataType = Date
	annotation PBI_NavigationStepName = Navegação
	annotation PBI_ResultType = Table
	annotation __PBI_TemplateDateTable = true
	annotation DefaultItem = DateHierarchy
	annotation TemplateId = Year
```

---

## 3.1. Relationships (relationships.tmdl)

```tmdl
relationship <guid>
	fromColumn: 'SourceTable'.'ColumnName'
	toColumn: 'TargetTable'.'ColumnName'
```

### Relationship Properties

| Property | Values | Notes |
|----------|--------|-------|
| `crossFilteringBehavior` | `bothDirections` | Default is single direction (omitted) |
| `joinOnDateBehavior` | `datePartOnly` | Date-only join (ignores time) |
| `toCardinality` | `many` | Many-to-many (default is many-to-one, omitted) |

> [!WARNING]
> **`cardinality: manyToOne` does NOT exist.** Causes `UnknownKeyword` parse error.
> Many-to-one is the default — simply omit the property. Only `toCardinality: many` exists (for many-to-many).

> [!WARNING]
> **When replacing a LocalDateTable relationship with a custom Calendario relationship:**
> 1. Remove the old relationship from `relationships.tmdl`
> 2. Remove the `variation` block from the source column (e.g. `mes/ano`) in its `.tmdl` file —
>    the variation stores the relationship GUID and will cause a dangling-reference error if left
> 3. Delete the orphaned `LocalDateTable_<guid>.tmdl` file from disk (removing `ref` from
>    `model.tmdl` is NOT enough — PBI still reads the file)

### Example: Various Relationship Types
```tmdl
# Simple (many-to-one, single direction)
relationship <guid>
	fromColumn: 'Vendas'.'Data'
	toColumn: 'Calendario'.'Date'

# Bi-directional
relationship <guid>
	crossFilteringBehavior: bothDirections
	fromColumn: 'Categorias'.'Data Chave'
	toColumn: 'Calendario'.'Date'

# Many-to-many + bi-directional
relationship <guid>
	crossFilteringBehavior: bothDirections
	toCardinality: many
	fromColumn: 'Calendario'.'Ano'
	toColumn: 'Dotação'.'Ano'

# Date-only join
relationship <guid>
	joinOnDateBehavior: datePartOnly
	fromColumn: 'Contratos'.'Data Vigência'
	toColumn: LocalDateTable_<guid>.Date
```

---

## 3.2. model.tmdl Extended Reference

```tmdl
model Model
	culture: pt-BR
	defaultPowerBIDataSourceVersion: powerBI_V3
	sourceQueryCulture: pt-BR
	dataAccessOptions
		legacyRedirects
		returnErrorValuesAsNull

annotation PBI_QueryOrder = ["Table1","Table2","Table3"]
annotation __PBI_TimeIntelligenceEnabled = 1
annotation PBI_ProTooling = ["DevMode"]

ref table 'Table1'
ref table 'Table2'
ref table dCalendario

ref cultureInfo pt-BR
```

> [!NOTE]
> `PBI_QueryOrder` controls the order tables appear in Power Query Editor. `PBI_ProTooling = ["DevMode"]` is set for PBIP projects.

---

## 18. Semantic Model Patterns (TMDL)

### Complete Table Structure
```tmdl
table TableName
	lineageTag: <guid>

	// --- Measures ---
	measure SimpleMeasure = SUM(TableName[Column])
		formatString: #,##0
		lineageTag: <guid>

	measure FilteredMeasure = CALCULATE(SUM(TableName[Value]), TableName[Category] = "X")
		formatString: R$ #,##0
		lineageTag: <guid>

	// Multi-line DAX with backtick fencing (preferred by PBI Desktop)
	measure ComplexMeasure = ```
		VAR _x = [SimpleMeasure]
		VAR _total = CALCULATE([SimpleMeasure], ALL(TableName))
		RETURN
		    DIVIDE(_x, _total, 0)
		```
		formatString: 0.00%;-0.00%;0.00%
		lineageTag: <guid>

	// Multi-line DAX with indentation-only
	measure HtmlMeasure =
			VAR _x = [SimpleMeasure]
			RETURN
			"<div>" & FORMAT(_x, "#,##0") & "</div>"
		lineageTag: <guid>

	// --- Calculated Columns ---
	column PercentColumn = TableName[Realizado] / TableName[Previsto]
		formatString: 0.00%;-0.00%;0.00%
		lineageTag: <guid>
		summarizeBy: sum
		annotation SummarizationSetBy = Automatic

	column DateKey = DATE([Ano], 1, 1)
		formatString: General Date
		lineageTag: <guid>
		summarizeBy: none
		annotation SummarizationSetBy = Automatic

	// --- Columns (from data source or calculated table) ---
	column ColumnName
		dataType: string
		lineageTag: <guid>
		summarizeBy: none
		sourceColumn: Column Name
		annotation SummarizationSetBy = Automatic

	column DateColumn
		dataType: dateTime
		formatString: Long Date
		lineageTag: <guid>
		summarizeBy: none
		sourceColumn: Date Column
		variation Variation
			isDefault
			relationship: <relationship-guid>
			defaultHierarchy: LocalDateTable_<guid>.'Hierarquia de datas'
		annotation SummarizationSetBy = Automatic
		annotation UnderlyingDateTimeDataType = Date

	column SortedColumn
		lineageTag: <guid>
		summarizeBy: none
		sourceColumn: Month Name
		sortByColumn: MonthNumber
		annotation SummarizationSetBy = Automatic

	// --- Columns (auto-generated by PBI for calculated tables) ---
	column InferredColumn
		lineageTag: <guid>
		isNameInferred
		sourceColumn: [InferredColumn]

	// --- Partition: Calculated (DAX) ---
	partition TableName = calculated
		mode: import
		source =
				DATATABLE(
					"Column1", STRING,
					"Column2", DOUBLE,
					{
						{"Row1", 100},
						{"Row2", 200}
					}
				)

	// --- Partition: M (Power Query - real data sources) ---
	// partition TableName = m
	//     mode: import
	//     source =
	//         let
	//             Fonte = SharePoint.Tables("https://site.sharepoint.com/sites/MySite"),
	//             Table = Fonte{[Id="guid"]}[Items]
	//         in
	//             Table

	annotation PBI_NavigationStepName = Navegação
	annotation PBI_ResultType = Table
```

### TMDL Indentation Rules (Critical!)

| Element | Indentation |
|---------|-------------|
| `table` keyword | 0 tabs |
| Properties (`lineageTag`) | 1 tab |
| `measure`, `column`, `partition` | 1 tab |
| Measure properties (`formatString`, `lineageTag`) | 2 tabs |
| Multi-line DAX expressions | 3 tabs |
| Partition `source =` expression | 4 tabs |

> [!CAUTION]
> If a multi-line DAX expression shares the same indentation as `lineageTag`, PBI parses `lineageTag` as DAX code and throws a syntax error!

### DAX Patterns for Measures

```dax
// Simple aggregation
SUM(Table[Column])

// Filtered aggregation
CALCULATE(SUM(Table[Value]), Table[Category] = "X")

// Percentage calculation
DIVIDE([Measure1], [Measure2], 0) * 100

// Difference from target
VAR _valor = [ActualMeasure]
VAR _meta = CALCULATE(SUM(Table[Meta]), Table[Cat] = "X")
RETURN DIVIDE(_valor - _meta, _meta, 0) * 100

// SVG gauge math (circle circumference)
VAR _percent = [MyPercent]
VAR _circumference = 339.292   // 2 × π × radius (r=54)
VAR _dashoffset = _circumference * (1 - _percent / 100)
```

### model.tmdl Reference
```tmdl
model Model
	culture: pt-BR
	defaultPowerBIDataSourceVersion: powerBI_V3
	sourceQueryCulture: pt-BR
	dataAccessOptions
		legacyRedirects
		returnErrorValuesAsNull

annotation PBI_QueryOrder = ["Table1","Table2","Table3"]
annotation __PBI_TimeIntelligenceEnabled = 1
annotation PBI_ProTooling = ["DevMode"]

ref table TableName
ref table 'Table With Spaces'

ref cultureInfo pt-BR
```

> [!NOTE]
> Each table gets its own `.tmdl` file in `definition/tables/`. The `model.tmdl` only contains `ref table` references. Table names with spaces must be wrapped in single quotes. `PBI_QueryOrder` controls order in Power Query Editor.

---

## Section 31: Best Practices for Programmatic Generation of PBIR & TMDL

When programmatically generating `.pbip` files (TMDL semantic models and JSON report definitions), it is crucial to adhere perfectly to schema versions and parsing rules. If these files are malformed, Power BI Desktop will fail to open the project entirely.

### 1. TMDL Lexing and Indentation Strictness
TMDL (Tabular Model Definition Language) does not use brackets for scope; it uses whitespace (indentation) similarly to Python or YAML. Moreover, the parser reads literal newlines and tabs to construct the object tree *before* evaluating DAX expressions.
*   **The Error**: `TMDL Format Error: Parsing error type - Indentation`
*   **The Cause**: We generated DAX string literals (e.g., HTML code inside double quotes `""`) that spanned multiple lines and contained raw literal tabs and spaces. The TMDL AST lexer interpreted those literal tabs inside the DAX string as structural object properties, completely breaking the parser.
*   **The Rule**: 
    1.  **NEVER** use raw multi-line strings (e.g., `" \n \t "`) for DAX measures when programmatically generating `.tmdl` files.
    2.  Instead, completely flatten strings onto a single line without raw newlines/tabs, OR use DAX string concatenation on subsequent lines (with proper `&` operators), or use the explicit TMDL multi-line formula syntax (`'''`). The safest programmatic method is compressing all DAX HTML into a single-line string.
    3.  All properties belonging to an object (e.g., `formatString`, `lineageTag`) must be indented exactly one tab further than the parent object declaration.

### 2. GUID Lineage Tags
TMDL requires unique identifiers (`lineageTag`) for all objects to resolve dependencies and metadata state.
*   **The Error**: Model load failure or corruption warnings.
*   **The Cause**: Accidentally using invalid hex characters (e.g., `#` instead of `a-f` or `0-9`) in a generated GUID.
*   **The Rule**: Whenever generating a mock `lineageTag` for new tables, columns, or measures in TMDL, the string must strictly enforce the `8-4-4-4-12` hex format (e.g., `f9e8d7c6-b5a4-0000-0001-1234567890ab`).

### 3. PBIR Schema Version Compatibility
Power BI projects are tightly bound to specific JSON schema versions.
*   **The Error**: `Can't resolve schema '1.0.0' in 'pages/pages.json'. This report was edited in a newer version of Power BI.`
*   **The Cause**: We overwrote the registry file (`pages.json`) using a schema version (`pages/1.0.0`) that was newer than the version the project was originally built on (`pagesMetadata/1.0.0`). The newer schema expects an array of page *objects*, while the older one expects an array of strings (`pageOrder`). 
*   **The Rule**: Always dynamically ingest the existing `$schema` URL and mirror its required object structure before applying `replace_file_content` macros. Do not assume the newest schema version is applicable unless explicitly prompted to upgrade the project.

---

## 37. `displayFolder` em Medidas TMDL

Organiza medidas em pastas no painel de campos do Power BI Desktop:

```tmdl
table _Medidas
    lineageTag: b5f8d3e2-94a6-4cab-ae17-8e4d2a39c156

    measure 'Valor Total' = SUM('licitacoes'[valor])
        formatString: R$ #,##0.00
        displayFolder: 01 Valores Base
        lineageTag: a1000001-0000-0000-0000-000000000001

    measure 'Valor YoY %' = DIVIDE([Valor Delta YoY], [Valor Ano Anterior])
        formatString: 0.0%
        displayFolder: 03 Time Intelligence
        lineageTag: a1000001-0000-0000-0000-000000000013
```

### Convenção de nomes de displayFolder

Prefixar com número garante ordenação correta no painel (PBI ordena alfabeticamente):

| Folder | Conteúdo |
|--------|----------|
| `01 Valores Base` | SUM, COUNT, DISTINCTCOUNT simples |
| `02 Medias e Ticket` | DIVIDE, MEDIAN, AVERAGE |
| `03 Time Intelligence` | SAMEPERIODLASTYEAR, TOTALYTD, DATESINPERIOD |
| `04 Participacao` | % do total, % da categoria (ALL, ALLEXCEPT) |
| `05 Rankings` | RANKX, TOPN, SELECTEDVALUE |
| `06 Concentracao` | Top 5/10 fornecedores, HHI |
| `07 Forecast` | Medidas de previsão (IC Superior/Inferior) |

> [!TIP]
> Tabelas de medidas sem colunas (só medidas) não precisam de `partition`. O PBI as trata como "measure tables" — boas práticas é criar uma única tabela `_Medidas` para centralizar todas as métricas calculadas.

---

## 39. DAX Time Intelligence — Biblioteca Completa (Projeto Databricks Gov)

Medidas validadas em produção no modelo de licitações 2019–2024:

```tmdl
// --- Comparação Período Anterior ---
measure 'Valor Ano Anterior' = CALCULATE([Valor Total], SAMEPERIODLASTYEAR(Calendario[Date]))
    formatString: R$ #,##0.00
    displayFolder: 03 Time Intelligence

measure 'Valor Delta YoY' = [Valor Total] - [Valor Ano Anterior]
    formatString: R$ #,##0.00
    displayFolder: 03 Time Intelligence

measure 'Valor YoY %' = DIVIDE([Valor Delta YoY], [Valor Ano Anterior])
    formatString: 0.0%
    displayFolder: 03 Time Intelligence

measure 'Valor Mes Anterior' = CALCULATE([Valor Total], DATEADD(Calendario[Date], -1, MONTH))
    formatString: R$ #,##0.00
    displayFolder: 03 Time Intelligence

// --- Acumulados ---
measure 'Valor YTD' = TOTALYTD([Valor Total], Calendario[Date])
    formatString: R$ #,##0.00
    displayFolder: 03 Time Intelligence

measure 'Valor YTD Ano Anterior' = CALCULATE([Valor YTD], SAMEPERIODLASTYEAR(Calendario[Date]))
    formatString: R$ #,##0.00
    displayFolder: 03 Time Intelligence

// --- Rolling Window ---
measure 'Valor 12M Moveis' = CALCULATE(
        [Valor Total],
        DATESINPERIOD(Calendario[Date], LASTDATE(Calendario[Date]), -12, MONTH)
    )
    formatString: R$ #,##0.00
    displayFolder: 03 Time Intelligence

// --- Rankings ---
measure 'Rank Categoria' = IF(
        HASONEVALUE('licitacoes'[categoria_ia]),
        RANKX(ALL('licitacoes'[categoria_ia]), [Valor Total],, DESC, DENSE)
    )
    displayFolder: 05 Rankings

measure 'Rank Fornecedor' = IF(
        HASONEVALUE('licitacoes'[nome]),
        RANKX(ALLSELECTED('licitacoes'[nome], 'licitacoes'[cpfCnpjVencedor]), [Valor Total],, DESC, DENSE)
    )
    displayFolder: 05 Rankings

// --- TOP N ---
measure 'Fornecedor #1 Nome' = CALCULATE(
        SELECTEDVALUE('licitacoes'[nome]),
        TOPN(1, VALUES('licitacoes'[nome]), [Valor Total], DESC)
    )
    displayFolder: 05 Rankings

// --- Concentração (HHI-like) ---
measure 'Valor Top 5 Fornecedores' =
        VAR Top5 = TOPN(5, VALUES('licitacoes'[cpfCnpjVencedor]), [Valor Total], DESC)
        RETURN CALCULATE([Valor Total], Top5)
    formatString: R$ #,##0.00
    displayFolder: 06 Concentracao

measure '% Concentracao Top 5 Fornecedores' = DIVIDE(
        [Valor Top 5 Fornecedores],
        CALCULATE([Valor Total], ALL('licitacoes'[cpfCnpjVencedor]))
    )
    formatString: 0.0%
    displayFolder: 06 Concentracao
```

---

## Seção 46 — Padrões de Medidas DAX

> Extraído dos 5 semantic models. Data: 2026-04-23

### 46.1 Organização canônica (Databrick Gov como referência)

Databrick Gov é o único com `displayFolder` definidos. Serve de template para o DashForge AI:

| Pasta | Padrão DAX principal |
|---|---|
| `01 Valores Base` | `SUM`, `DISTINCTCOUNT` |
| `02 Médias` | `DIVIDE([A], [B])` com proteção BLANK |
| `03 Time Intelligence` | `SAMEPERIODLASTYEAR`, `DATEADD`, `TOTALYTD`, `DATESINPERIOD` |
| `04 Participação` | `CALCULATE([M], ALLEXCEPT(T, T[col]))` |
| `05 Rankings` | `IF(HASONEVALUE(T[col]), RANKX(...))` |
| `06 Concentração` | `TOPN + VAR` complexas |
| `07 Qualidade` | `FILTER + COUNTROWS`, `ISBLANK` |
| `08 Auxiliares` | Formatação texto/cor |
| `09 Forecast` | Regressão, DATESINPERIOD |

### 46.2 Padrões críticos de protecão

```dax
// Proteção de divisão por zero
Ticket Medio = DIVIDE([Valor Total], [Qtd Licitacoes])

// Proteção de contexto múltiplo em ranking
Rank Fornecedor = IF(HASONEVALUE(T[nome]), RANKX(ALL(T[nome]), [Valor Total]))

// Garantir retorno numérico mesmo com CALCULATE vazio
Projetos Em Risco = CALCULATE([Total Ativos], T[Status] = "Em risco") + 0

// Tolerância em reconciliação
Status_Validacao = IF(ABS([Calculado] - [Real]) <= 0.01, "✅ Conciliado", "❌ Divergência")
```

### 46.3 Medidas de controle visual (macros para mostrar/ocultar)

Estas medidas são aplicadas como filtros de nível visual para mostrar/ocultar visuais dinamicamente:

```dax
// Mostrar painel de detalhe somente quando um item é filtrado
ExibirHistorico = IF(ISFILTERED(Projetos[Projeto]), 1, 0)
// Aplicar no visual como filtro: ExibirHistorico = 1

// Mostrar somente linhas com problema
Filtro Linhas com Problema =
    VAR TemAlvara = ISBLANK([AlvaraId]) || [AlvaraId] = ""
    VAR TemValorErrado = [Valor] <= 0
    RETURN IF(TemAlvara || TemValorErrado, 1, 0)
// Aplicar no visual como filtro: Filtro Linhas com Problema = 1
```

### 46.4 Medidas auxiliares de cor (formatação condicional)

```dax
// Retorna HEX diretamente para usar em conditional formatting
Cor YoY =
    SWITCH(
        TRUE(),
        [Valor YoY %] > 0,    "#16A34A",  // verde
        [Valor YoY %] < 0,    "#DC2626",  // vermelho
        "#71717A"                           // cinza (neutro)
    )
```

### 46.5 Medidas de texto dinâmico

Usadas em `cardVisual` ou `textbox` para títulos e legendas que refletem filtros ativos:

```dax
// Período selecionado
Periodo Selecionado =
    VAR MinD = MIN(T[PrimeiroDiaMes])
    VAR MaxD = MAX(T[UltimoDiaMes])
    RETURN IF(
        ISBLANK(MinD), "Período: (sem filtro)",
        "Período: " & FORMAT(MinD, "dd/mm/yyyy") & " a " & FORMAT(MaxD, "dd/mm/yyyy")
    )

// Timestamp com fuso (UTC-3)
Ultima Atualizacao =
    "Atualizado em " & FORMAT(NOW() - TIME(3,0,0), "dd/MM/yyyy") &
    " às " & FORMAT(NOW() - TIME(3,0,0), "HH:mm")

// Valor formatado para KPI (sem notação científica)
Valor Total Formatado =
    VAR v = [Valor Total]
    RETURN SWITCH(TRUE(),
        v >= 1e9, FORMAT(v/1e9, "0.0") & " bi",
        v >= 1e6, FORMAT(v/1e6, "0.0") & " mi",
        v >= 1e3, FORMAT(v/1e3, "0.0") & " mil",
        FORMAT(v, "#,##0"))

// Título dinâmico (mostra item selecionado)
Titulo Projeto = SELECTEDVALUE(Projetos[Projeto], "Todos os Projetos")
```

### 46.6 Colunas calculadas (padrões recorrentes)

```dax
// Status derivado com lógica temporal
StatusCalculado =
    VAR Hoje = TODAY()
    RETURN SWITCH(TRUE(),
        [Status] IN {"CANCELADO", "SUSPENSO"}, [Status],
        [Status] = "ENTREGUE", "ENTREGUE",
        Hoje > [DataEntrega], "ATRASADO",
        [Status])

// Normalização de percentual (aceita 0.87 ou 87)
PctConcluido =
    VAR Bruto = IF(ISBLANK([pct_campo]), [Progresso], [pct_campo])
    VAR Num = IFERROR(VALUE(Bruto), 0)
    RETURN TRUNC(IF(Num > 1, Num / 100, Num), 4)

// Classificação de domínio de texto
DominioEmail =
    VAR e = LOWER([Email])
    RETURN IF(ISBLANK(e), "Sem email",
        IF(RIGHT(e, 12) = "@tjba.jus.br", "Interno", "Externo"))
```

### 46.7 Tabela de lookup criada em DAX (DATATABLE)

```dax
// Tabela estática para filtro de status visual
FiltroStatus = DATATABLE("Status", STRING, {{"✅"}, {"❌"}})
```
Usada como tabela auxiliar para slicers ou para cruzamento com medida de status.

---

## Seção 52 — Arquivos Completos do SemanticModel para Mode C (CSV/Excel)

> Adicionado em 2026-04-24. Fecha GAP-C3. Fonte: projeto `vendas.pbip` gerado pelo PBI Desktop a partir de um CSV real.

---

### 52.1 ~~GAP-C3~~ RESOLVIDO: M Query para CSV

Formato gerado automaticamente pelo PBI Desktop ao carregar um CSV:

```tmdl
partition vendas = m
    mode: import
    source =
            let
                Fonte = Csv.Document(File.Contents("C:\caminho\completo\arquivo.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
                #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
                #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"Data", type date}, {"Produto", type text}, {"Regiao", type text}, {"Vendedor", type text}, {"Status", type text}, {"Valor", Int64.Type}, {"Quantidade", Int64.Type}})
            in
                #"Tipo Alterado"
```

**Parâmetros obrigatórios:**
- `Delimiter=","` — vírgula para CSV padrão (usar `";"` para CSV europeu/brasileiro)
- `Columns=N` — número de colunas do CSV (otimização de parser)
- `Encoding=65001` — UTF-8. Alternativas: `1252` (Windows-1252/ANSI), `1200` (UTF-16)
- `QuoteStyle=QuoteStyle.None` — padrão quando não há aspas duplas nos dados

**Mapeamento de tipos M → TMDL:**

| M type | TMDL dataType | TMDL formatString |
|---|---|---|
| `type date` | `dateTime` | `Long Date` |
| `type text` | `string` | *(omitir)* |
| `Int64.Type` | `int64` | `0` |
| `type number` / `Currency.Type` | `decimal` | `0.00` ou `"R$ #,##0.00"` |
| `type logical` | `boolean` | *(omitir)* |

**Coluna de data gera automaticamente o bloco `variation`:**
```tmdl
column Data
    dataType: dateTime
    formatString: Long Date
    lineageTag: <uuid>
    summarizeBy: none
    sourceColumn: Data

    variation Variation
        isDefault
        relationship: <uuid-do-relacionamento>
        defaultHierarchy: LocalDateTable_<uuid>.'Hierarquia de datas'

    annotation SummarizationSetBy = Automatic
    annotation UnderlyingDateTimeDataType = Date
```

O bloco `variation` conecta a coluna de data ao LocalDateTable auto-gerado. O UUID do relacionamento e do LocalDateTable são interdependentes — **gerados pelo PBI Desktop na primeira abertura.**

---

### 52.2 Estratégia de geração para Mode C (decisão arquitetural)

**Problema:** `variation`, `LocalDateTable_<UUID>` e o relacionamento em `relationships.tmdl` referenciam UUIDs gerados dinamicamente pelo PBI Desktop — não podem ser hardcoded.

**Solução:** O agente gera apenas o mínimo; o PBI Desktop completa o resto na primeira abertura.

| Arquivo | O agente gera? | Observação |
|---|---|---|
| `model.tmdl` | ✅ Sim | Com `__PBI_TimeIntelligenceEnabled = 1` |
| `database.tmdl` | ✅ Sim | Fixo: `compatibilityLevel: 1600` |
| `tables/<nome>.tmdl` | ✅ Sim | Sem o bloco `variation` — PBI adiciona |
| `relationships.tmdl` | ❌ Não | PBI cria ao reconhecer a coluna de data |
| `cultures/pt-BR.tmdl` | ❌ Não | PBI gera na primeira abertura |
| `DateTableTemplate_<UUID>.tmdl` | ❌ Não | PBI gera automaticamente |
| `LocalDateTable_<UUID>.tmdl` | ❌ Não | PBI gera automaticamente |
| `.platform` (Report e SemanticModel) | ✅ Sim | Com UUID gerado pelo agente |
| `definition.pbism` | ✅ Sim | Fixo (ver 52.4) |
| `definition.pbir` | ✅ Sim | Já documentado na Seção 50 |
| `.pbip` (raiz) | ✅ Sim | Já documentado na Seção 50 |

---

### 52.3 definition.pbism (novo — entry point do SemanticModel)

Análogo ao `definition.pbir` do Report. Conecta o SemanticModel ao schema do Fabric.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
  "version": "4.2",
  "settings": {}
}
```

Arquivo fixo — não mudar.

---

### 52.4 .platform (Report e SemanticModel)

Arquivo de integração com Fabric/Git. Necessário em ambas as pastas.

**vendas.Report/.platform:**
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "Report",
    "displayName": "<NomeProjeto>"
  },
  "config": {
    "version": "2.0",
    "logicalId": "<uuid-v4>"
  }
}
```

**vendas.SemanticModel/.platform:**
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "SemanticModel",
    "displayName": "<NomeProjeto>"
  },
  "config": {
    "version": "2.0",
    "logicalId": "<uuid-v4>"
  }
}
```

`logicalId` = UUID v4 único por artefato. Em Python: `str(uuid.uuid4())`.

---

### 52.5 database.tmdl (fixo)

```tmdl
database
    compatibilityLevel: 1600
```

Sempre idêntico. Nunca mudar.

---

### 52.6 model.tmdl mínimo para Mode C (tabela única)

```tmdl
model Model
    culture: pt-BR
    defaultPowerBIDataSourceVersion: powerBI_V3
    sourceQueryCulture: pt-BR
    dataAccessOptions
        legacyRedirects
        returnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 1
annotation PBI_QueryOrder = ["<NomeTabela>"]
annotation PBI_ProTooling = ["DevMode"]

ref table <NomeTabela>
ref cultureInfo pt-BR
```

**Notas:**
- `__PBI_TimeIntelligenceEnabled = 1` → PBI auto-cria LocalDateTable + DateTableTemplate + relacionamento para cada coluna de data
- `PBI_QueryOrder` → ordem das tabelas no painel de campos (lista JSON de strings)
- `ref cultureInfo pt-BR` → requerido para localização

---

### 52.7 Template completo de tabela TMDL para CSV (Mode C)

```tmdl
table <NomeTabela>
    lineageTag: <uuid-v4>

    column <ColunaCategorica>
        dataType: string
        lineageTag: <uuid-v4>
        summarizeBy: none
        sourceColumn: <ColunaCategorica>

        annotation SummarizationSetBy = Automatic

    column <ColunaData>
        dataType: dateTime
        formatString: Long Date
        lineageTag: <uuid-v4>
        summarizeBy: none
        sourceColumn: <ColunaData>

        annotation SummarizationSetBy = Automatic
        annotation UnderlyingDateTimeDataType = Date

    column <ColunaInteira>
        dataType: int64
        formatString: 0
        lineageTag: <uuid-v4>
        summarizeBy: sum
        sourceColumn: <ColunaInteira>

        annotation SummarizationSetBy = Automatic

    column <ColunaDecimal>
        dataType: decimal
        lineageTag: <uuid-v4>
        summarizeBy: sum
        sourceColumn: <ColunaDecimal>

        annotation SummarizationSetBy = Automatic

    partition <NomeTabela> = m
        mode: import
        source =
                let
                    Fonte = Csv.Document(File.Contents("<caminho-absoluto>.csv"),[Delimiter=",", Columns=<N>, Encoding=65001, QuoteStyle=QuoteStyle.None]),
                    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
                    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"<ColunaData>", type date}, {"<ColunaCategorica>", type text}, {"<ColunaInteira>", Int64.Type}, {"<ColunaDecimal>", type number}})
                in
                    #"Tipo Alterado"

    annotation PBI_ResultType = Table
```

**Atenção ao bloco `variation`:** Não gerar o bloco `variation` nas colunas de data — o PBI Desktop o adiciona automaticamente quando detecta `UnderlyingDateTimeDataType = Date` + `__PBI_TimeIntelligenceEnabled = 1`.

---

### 52.8 Estrutura completa de pastas para um .pbip gerado do zero (Mode C)

```
<Projeto>.pbip                                    ← fixo (ver Seção 50)
├── <Projeto>.Report/
│   ├── .platform                                 ← fixo com logicalId UUID
│   ├── definition.pbir                           ← fixo (ver Seção 50)
│   └── definition/
│       ├── version.json                          ← fixo (ver Seção 51.10)
│       ├── report.json                           ← mínimo (ver Seção 51.9)
│       └── pages/
│           ├── pages.json                        ← lista de páginas
│           └── <pageId>/
│               ├── page.json
│               └── visuals/
│                   └── <visualId>/
│                       └── visual.json
└── <Projeto>.SemanticModel/
    ├── .platform                                 ← fixo com logicalId UUID
    ├── definition.pbism                          ← fixo (ver Seção 52.3)
    └── definition/
        ├── model.tmdl                            ← mínimo (ver Seção 52.6)
        ├── database.tmdl                         ← fixo (ver Seção 52.5)
        └── tables/
            └── <NomeTabela>.tmdl                 ← gerado (ver Seção 52.7)
```

**Arquivos que o agente NÃO cria (PBI Desktop gera na 1ª abertura):**
- `relationships.tmdl`
- `cultures/pt-BR.tmdl`
- `tables/DateTableTemplate_<UUID>.tmdl`
- `tables/LocalDateTable_<UUID>.tmdl`
- `.pbi/` (pasta de cache local)

---

### 52.8b M Query para Excel (.xlsx)

```tmdl
partition <NomeTabela> = m
    mode: import
    source =
            let
                Fonte = Excel.Workbook(File.Contents("C:\caminho\completo\arquivo.xlsx"), null, true),
                <NomePlanilha>_Sheet = Fonte{[Item="<NomePlanilha>",Kind="Sheet"]}[Data],
                #"Cabeçalhos Promovidos" = Table.PromoteHeaders(<NomePlanilha>_Sheet, [PromoteAllScalars=true]),
                #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"Data", type date}, {"Produto", type text}, {"Valor", Int64.Type}})
            in
                #"Tipo Alterado"
```

**Diferenças em relação ao CSV:**

| | CSV | Excel |
|---|---|---|
| Função | `Csv.Document(File.Contents(...), [...])` | `Excel.Workbook(File.Contents(...), null, true)` |
| Parâmetros extras | `Delimiter`, `Columns`, `Encoding` | Nenhum |
| Passo adicional | — | Selecionar planilha: `Fonte{[Item="<aba>", Kind="Sheet"]}[Data]` |
| Nome da tabela TMDL | Nome do arquivo (sem extensão) | **Nome da aba do Excel** |

**Parâmetros do `Excel.Workbook`:**
- `null` = deixar PBI inferir headers (padrão)
- `true` = `InferSheetDimensions` — detecta o range usado automaticamente (sempre `true`)

**Implicação para Mode C:** se o usuário enviar um `.xlsx`, o agente precisa saber o nome da aba para construir o M query. O nome da aba vira o nome da tabela no SemanticModel.

---

### 52.9 Status final — TODOS os gaps bloqueantes resolvidos

| Gap | Status |
|---|---|
| GAP-C1 (.pbip raiz) | ✅ Seção 50 |
| GAP-C2 (definition.pbir) | ✅ Seção 50 |
| GAP-C3 (M query CSV + arquivos SemanticModel) | ✅ **Seção 52** |
| GAP-A1 (chart templates) | ✅ Seção 51 |
| GAP-A2 (visual-level filter) | ✅ Seção 51 |
| GAP-A3 (report.json mínimo) | ✅ Seção 51 |
| GAP-M1 (version.json) | ✅ Seção 51 |
| GAP-M2 (cultures TMDL) | ✅ Seção 51 |
| GAP-M3 (convenção IDs) | ✅ Seção 50 |
| GAP-M5 (syncSlicers.json) | ✅ Seção 51 |

**Documentação completa. O desenvolvimento pode começar.**

*Seção 52 adicionada em 2026-04-24*

