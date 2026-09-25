# Relatório PBIR — estrutura, visuais, páginas, slicers, bookmarks

> Extraído de `pbir_research_and_learnings.md` (aprendizados práticos em projetos TJBA). Seções mantidas na íntegra; a numeração original foi preservada.

> **Erratas:**
> - Versões de schema citadas nos títulos (ex.: `visualContainer 2.6.0`) são as da época do teste. Sempre espelhe a versão que o projeto atual já usa.
> - A tabela de objetos do `cardVisual` (seção 4) veio de outro projeto. No `nucleo_de_convenios_tjba`, o card novo usa `calloutValue`, `label` e `accent` sem selector. Em caso de divergência, copie de um visual existente do próprio projeto.

## Índice

- 1. Project Structure (PBIR Format)
- 2. Color Format — The #1 Gotcha
- 4. Visual Container Schema (v2.6.0)
- 4.1. Slicer Visual Schema
- 4.2. Textbox Visual Schema
- 4.3. Shape Visual Schema
- 4.4. Image Visual Schema
- 4.5. Visual Group (Container)
- 4.6. Additional Container Objects
- 4.7. Selector Patterns (Conditional Formatting)
- 4.8. Chart Visual Objects Reference
- 5. Page Schema (v2.0.0)
- 6. Pages Metadata
- 8. PBI Desktop Behavior on Load
- 9. JSON Schemas Reference
- 13. PBI Desktop Auto-Normalization Patterns
- 19. Quick Reference — Files to Edit for Common Tasks
- 23. Creating Pages from JSON — Complete Workflow
- 24. Visual Container Objects — Extended Patterns
- 30. PBIR Deep Dive: Native Slicers & Stateful Bookmarks
- 35. Bookmark JSON Schema (v2.1.0) — Documentação Completa
- 36. Propriedades de Visual Não Documentadas (Descobertas no Projeto)
- 38. `tableEx` Visual — Schema Completo
- Seção 44 — Catálogo de Padrões de Slicer (Segmentação de Dados)
- Seção 45 — Padrões de Interatividade (Bookmarks, Botões, Gavetas)
- Seção 48 — Novos Visual Types: Governança BI e projeto.pbip
- Seção 51 — Templates Canônicos de Chart visual.json + Gaps Resolvidos

---

## 1. Project Structure (PBIR Format)

```
projeto.pbip                              ← entry point
├── projeto.Report/
│   ├── definition.pbir                   ← version + semantic model reference
│   ├── definition/
│   │   ├── report.json                   ← themes, settings
│   │   ├── version.json                  ← PBIR version (2.0.0)
│   │   └── pages/
│   │       ├── pages.json                ← page order + active page
│   │       └── <pageId>/
│   │           ├── page.json             ← page definition
│   │           └── visuals/
│   │               └── <visualId>/
│   │                   └── visual.json   ← individual visual
│   └── StaticResources/                  ← themes, images
├── projeto.SemanticModel/
│   └── definition/
│       ├── model.tmdl                    ← data model root
│       ├── database.tmdl                 ← compat level
│       ├── tables/<tableName>.tmdl       ← one file per table
│       └── cultures/pt-BR.tmdl           ← localization
└── .gitignore
```

---

## 2. Color Format — The #1 Gotcha

> [!CAUTION]
> Plain hex strings like `"color": "#FFFFFF"` are **silently ignored** by Power BI Desktop. They get replaced with `"solid": {}` (theme default) on save.

### ❌ Wrong — plain string (silently ignored)
```json
"color": {
  "solid": {
    "color": "#162447"
  }
}
```

### ✅ Correct — Literal expression with single-quoted hex
```json
"color": {
  "solid": {
    "color": {
      "expr": {
        "Literal": {
          "Value": "'#162447'"
        }
      }
    }
  }
}
```

### ✅ Also valid — ThemeDataColor reference (PBI generates this)
```json
"color": {
  "solid": {
    "color": {
      "expr": {
        "ThemeDataColor": {
          "ColorId": 1,
          "Percent": 0
        }
      }
    }
  }
}
```

**Rule**: All property values in PBIR use the `expr → Literal → Value` wrapper. Hex colors must be wrapped in **single quotes** inside the Value string: `"'#FF0000'"`.

---

## 4. Visual Container Schema (v2.6.0)

### Required properties
```json
{
  "$schema": "...visualContainer/2.6.0/schema.json",
  "name": "unique_visual_id",       // required
  "position": {                      // required
    "x": 40, "y": 80,               // required
    "height": 180, "width": 370,    // required
    "z": 1000,                      // stacking order
    "tabOrder": 0                   // keyboard nav
  },
  "visual": { ... }                  // or "visualGroup"
}
```

### Visual Configuration (v2.2.0)

```json
"visual": {
  "visualType": "card",              // required: card, clusteredBarChart, etc.
  "query": {
    "queryState": {
      "Values": {                    // role name (varies by visual type)
        "projections": [{
          "field": {
            "Measure": {
              "Expression": {
                "SourceRef": { "Entity": "TableName" }
              },
              "Property": "MeasureName"
            }
          },
          "queryRef": "TableName.MeasureName"
        }]
      }
    }
  },
  "objects": { ... },                // visual-specific formatting
  "visualContainerObjects": { ... }  // container formatting (bg, border, title)
}
```

### Visual Container Objects (formatting that works)

| Object | Properties | Notes |
|--------|-----------|-------|
| `background` | `show`, `color`, `transparency` | Card background |
| `border` | `show`, `color`, `radius` | Rounded corners with `radius` |
| `title` | `show`, `text`, `fontColor`, `fontSize`, `fontFamily`, `bold` | Visual title |
| `visualHeader` | `show` | Hide the hover header icons |
| `padding` | `top`, `left` | Internal padding |

### Visual-specific Objects (for `card` type)

| Object | Properties | Notes |
|--------|-----------|-------|
| `labels` | `color`, `fontSize`, `fontFamily` | Main value display |
| `categoryLabels` | `show`, `color`, `fontSize` | Subtitle under the value |

### Visual-specific Objects (for `cardVisual` — new card)

> [!IMPORTANT]
> The new `cardVisual` type uses role name `Data` (not `Values` like the old `card`). It also uses `selector: {"id": "default"}` on most objects.

| Object | Properties | Notes |
|--------|-----------|-------|
| `value` | `show`, `horizontalAlignment`, `fontColor` | Main value display |
| `accentBar` | `show`, `position` | Accent decoration bar |
| `outline` | `show` | Card outline |
| `layout` | `rectangleRoundedCurveCustomStyle`, `backgroundShow`, `backgroundFillColor`, `backgroundTransparency` | Card shape/layout |
| `fillCustom` | `fillColor` | Custom fill color |
| `label` | `fontColor` | Category label |

```json
// cardVisual query uses "Data" role (not "Values"):
"query": {
  "queryState": {
    "Data": {
      "projections": [{
        "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "TABLE" } }, "Property": "MEASURE" } },
        "queryRef": "TABLE.MEASURE",
        "nativeQueryRef": "Display Name",
        "displayName": "Display Name"
      }]
    }
  }
}
```

---

## 4.1. Slicer Visual Schema

```json
{
  "$schema": "...visualContainer/2.6.0/schema.json",
  "name": "unique_id",
  "position": { "x": 48, "y": 7, "z": 1000, "height": 50, "width": 686, "tabOrder": 1000 },
  "visual": {
    "visualType": "slicer",
    "query": {
      "queryState": {
        "Values": {
          "projections": [{
            "field": { "Column": { "Expression": { "SourceRef": { "Entity": "TABLE" } }, "Property": "COLUMN" } },
            "queryRef": "TABLE.COLUMN",
            "nativeQueryRef": "COLUMN",
            "active": true
          }]
        }
      }
    },
    "objects": {
      "data": [{
        "properties": {
          "mode": { "expr": { "Literal": { "Value": "'Dropdown'" } } },
          "isInvertedSelectionMode": { "expr": { "Literal": { "Value": "true" } } }
        }
      }],
      "general": [{
        "properties": {
          "orientation": { "expr": { "Literal": { "Value": "0D" } } }
        }
      }],
      "selection": [{
        "properties": {
          "selectAllCheckboxEnabled": { "expr": { "Literal": { "Value": "true" } } },
          "strictSingleSelect": { "expr": { "Literal": { "Value": "false" } } }
        }
      }],
      "items": [{
        "properties": {
          "textSize": { "expr": { "Literal": { "Value": "15D" } } },
          "bold": { "expr": { "Literal": { "Value": "true" } } },
          "fontColor": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 1, "Percent": 0 } } } } },
          "background": { "solid": { "color": { "expr": { "ThemeDataColor": { "ColorId": 0, "Percent": 0 } } } } }
        }
      }],
      "header": [{
        "properties": {
          "textSize": { "expr": { "Literal": { "Value": "12D" } } },
          "show": { "expr": { "Literal": { "Value": "false" } } }
        }
      }]
    },
    "visualContainerObjects": {
      "background": [{ "properties": { "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#0097B2'" } } } } } } }],
      "border": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } }, "radius": { "expr": { "Literal": { "Value": "25D" } } } } }],
      "title": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }],
      "padding": [{ "properties": { "left": { "expr": { "Literal": { "Value": "20D" } } }, "top": { "expr": { "Literal": { "Value": "0D" } } } } }],
      "dropShadow": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }]
    },
    "syncGroup": {
      "groupName": "SlicerGroupName",
      "fieldChanges": true,
      "filterChanges": true
    },
    "drillFilterOtherVisuals": true
  },
  "parentGroupName": "parent_group_id"
}
```

### Slicer objects reference

| Object | Property | Values | Notes |
|--------|----------|--------|-------|
| `data` | `mode` | `'Dropdown'`, `'List'` | Display mode |
| `data` | `isInvertedSelectionMode` | `true`/`false` | "Select All" default behavior |
| `general` | `orientation` | `0D` (vertical), `1D` (horizontal) | Slicer orientation |
| `selection` | `selectAllCheckboxEnabled` | `true`/`false` | Show "Select All" checkbox |
| `selection` | `strictSingleSelect` | `true`/`false` | Single selection only |
| `items` | `textSize`, `bold`, `fontColor`, `background` | — | Dropdown item formatting |
| `header` | `textSize`, `show`, `fontColor`, `background` | — | Slicer header formatting |

### `syncGroup` (Cross-Page Slicer Sync)

```json
"syncGroup": {
  "groupName": "Ano",       // Slicers with the same groupName sync across pages
  "fieldChanges": true,      // Sync field changes
  "filterChanges": true      // Sync filter selection changes
}
```

---

## 4.2. Textbox Visual Schema

```json
{
  "$schema": "...visualContainer/2.6.0/schema.json",
  "name": "unique_id",
  "position": { "x": 14, "y": 16, "z": 2000, "height": 35, "width": 50, "tabOrder": 2000 },
  "visual": {
    "visualType": "textbox",
    "objects": {
      "general": [{
        "properties": {
          "paragraphs": [{
            "textRuns": [{
              "value": "My Text Here",
              "textStyle": {
                "fontSize": "12pt",
                "color": "#ffffff"
              }
            }],
            "horizontalTextAlignment": "center"
          }]
        }
      }]
    },
    "visualContainerObjects": {
      "background": [{
        "properties": {
          "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#0097B2'" } } } } }
        }
      }]
    },
    "drillFilterOtherVisuals": true
  }
}
```

> [!NOTE]
> Textbox uses plain color strings in `textStyle` (not the `expr → Literal → Value` pattern). Only `visualContainerObjects` uses the expression pattern.

---

## 4.3. Shape Visual Schema

```json
{
  "$schema": "...visualContainer/2.6.0/schema.json",
  "name": "unique_id",
  "position": { "x": 0, "y": 0, "z": 0, "height": 547, "width": 746, "tabOrder": 1000 },
  "visual": {
    "visualType": "shape",
    "objects": {
      "shape": [{
        "properties": {
          "tileShape": { "expr": { "Literal": { "Value": "'rectangle'" } } }
        }
      }],
      "rotation": [{
        "properties": {
          "shapeAngle": { "expr": { "Literal": { "Value": "0L" } } },
          "angle": { "expr": { "Literal": { "Value": "270D" } } }
        }
      }],
      "fill": [{
        "properties": {
          "fillColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#0097B2'" } } } } }
        },
        "selector": { "id": "default" }
      }],
      "outline": [{
        "properties": {
          "lineColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#007DA4'" } } } } }
        },
        "selector": { "id": "default" }
      }],
      "text": [
        { "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } },
        {
          "properties": {
            "text": { "expr": { "Literal": { "Value": "'MY TEXT'" } } },
            "fontSize": { "expr": { "Literal": { "Value": "8D" } } },
            "bold": { "expr": { "Literal": { "Value": "true" } } }
          },
          "selector": { "id": "default" }
        }
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

### Shape object reference

| Object | Property | Values | Notes |
|--------|----------|--------|-------|
| `shape` | `tileShape` | `'rectangle'`, `'rectangleRounded'` | Shape type |
| `rotation` | `shapeAngle` | `0L` | Rotation in legacy format |
| `rotation` | `angle` | `270D` | Actual rotation degrees |
| `fill` | `fillColor` | Color expr | Background fill |
| `outline` | `lineColor` | Color expr | Border line color |
| `text` | `show`, `text`, `fontSize`, `bold` | — | Text overlay on shape |

> [!NOTE]
> Shape objects use `selector: { "id": "default" }` on `fill`, `outline`, and `text` blocks.

---

## 4.4. Image Visual Schema

```json
{
  "$schema": "...visualContainer/2.6.0/schema.json",
  "name": "unique_id",
  "position": { "x": 0, "y": 0, "z": 4500, "height": 149, "width": 120, "tabOrder": 0 },
  "visual": {
    "visualType": "image",
    "objects": {
      "general": [{
        "properties": {
          "imageUrl": {
            "expr": {
              "ResourcePackageItem": {
                "PackageName": "RegisteredResources",
                "PackageType": 1,
                "ItemName": "MyImage123456789.png"
              }
            }
          }
        }
      }]
    },
    "visualContainerObjects": {
      "title": [{
        "properties": {
          "text": { "expr": { "Literal": { "Value": "'Image Label'" } } }
        }
      }],
      "visualLink": [{
        "properties": {
          "show": { "expr": { "Literal": { "Value": "true" } } },
          "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
          "navigationSection": { "expr": { "Literal": { "Value": "'target_page_name'" } } }
        }
      }]
    },
    "drillFilterOtherVisuals": true
  },
  "howCreated": "InsertVisualButton"
}
```

### Image source: `ResourcePackageItem`

Images are referenced from `report.json` → `resourcePackages`:
```json
// In report.json:
"resourcePackages": [{
  "name": "RegisteredResources",
  "type": "RegisteredResources",
  "items": [
    { "name": "MyImage123456789.png", "path": "MyImage123456789.png", "type": "Image" }
  ]
}]
```

Image files are stored in: `projeto.Report/StaticResources/RegisteredResources/`

### `visualLink` (Page Navigation Action)

```json
"visualLink": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
    "navigationSection": { "expr": { "Literal": { "Value": "'target_page_name'" } } },
    "tooltip": { "expr": { "Literal": { "Value": "'Click to navigate'" } } }
  }
}]
```

---

## 4.5. Visual Group (Container)

```json
{
  "$schema": "...visualContainer/2.6.0/schema.json",
  "name": "group_unique_id",
  "position": { "x": 1568, "y": 83, "z": 4500, "height": 543, "width": 122, "tabOrder": 4000 },
  "visualGroup": {
    "displayName": "Group Display Name",
    "groupMode": "ScaleMode"
  },
  "parentGroupName": "outer_group_id"
}
```

### Nesting visuals in groups: `parentGroupName`

Any visual container can belong to a group by setting `parentGroupName`:
```json
{
  "name": "child_visual_id",
  "position": { ... },
  "visual": { ... },
  "parentGroupName": "group_unique_id"
}
```

Visual groups can be nested (groups inside groups) with `parentGroupName` referencing another group's `name`.

### `howCreated` property

Tracks how the visual was inserted: `"InsertVisualButton"`. This is auto-added by PBI Desktop.

---

## 4.6. Additional Container Objects

| Object | Properties | Notes |
|--------|-----------|-------|
| `dropShadow` | `show` | Drop shadow effect |
| `visualLink` | `show`, `type`, `navigationSection`, `tooltip` | Page navigation action |
| `general` | `keepLayerOrder`, `altText` | Layer order + accessibility |
| `padding` | `top`, `left`, `bottom`, `right` | All use `"ND"` format |

### Dynamic Title from Measure

Visual titles can be driven by a DAX measure instead of static text:
```json
"title": [{
  "properties": {
    "text": {
      "expr": {
        "Measure": {
          "Expression": { "SourceRef": { "Entity": "TABLE" } },
          "Property": "TITLE_MEASURE"
        }
      }
    },
    "fontSize": { "expr": { "Literal": { "Value": "20D" } } },
    "bold": { "expr": { "Literal": { "Value": "true" } } },
    "alignment": { "expr": { "Literal": { "Value": "'center'" } } }
  }
}]
```

---

## 4.7. Selector Patterns (Conditional Formatting)

### `selector: {"id": "default"}`
Used for default formatting on shapes, new cards, etc.:
```json
"fill": [{
  "properties": { "fillColor": { ... } },
  "selector": { "id": "default" }
}]
```

### `selector: {"metadata": "..."}`
Used for coloring data series by their query reference:
```json
"dataPoint": [{
  "properties": { "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#0097B2'" } } } } } },
  "selector": { "metadata": "Sum(4 iGovTIC.MÉDIAS ESTADUAIS)" }
}]
```

### `selector: {"data": [...]}` — Conditional by value
Used to color specific data values differently:
```json
"dataPoint": [{
  "properties": { "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#00C800'" } } } } } },
  "selector": {
    "data": [{
      "scopeId": {
        "Comparison": {
          "ComparisonKind": 0,
          "Left": {
            "Column": {
              "Expression": { "SourceRef": { "Entity": "TABLE" } },
              "Property": "COLUMN"
            }
          },
          "Right": { "Literal": { "Value": "'ValueToMatch'" } }
        }
      }
    }]
  }
}]
```

`ComparisonKind`: 0 = Equal

---

## 4.8. Chart Visual Objects Reference

### Chart query roles

| Visual Type | Roles |
|-------------|-------|
| `clusteredColumnChart` | `Category`, `Y`, `Series` |
| `lineClusteredColumnComboChart` | `Category`, `Y`, `Y2` |
| `lineStackedColumnComboChart` | `Category`, `Y`, `Y2` |
| `card` | `Values` |
| `cardVisual` (new) | `Data` |
| `slicer` | `Values` |
| `htmlContent...` | `content` |
| `deneb...` | `dataset` |

### Common chart objects

| Object | Key Properties |
|--------|---------------|
| `categoryAxis` | `fontSize`, `bold`, `labelColor`, `showAxisTitle`, `gridlineShow`, `innerPadding` |
| `valueAxis` | `fontSize`, `bold`, `show`, `showAxisTitle`, `secShow` (secondary), `labelPrecision` |
| `labels` | `show`, `fontSize`, `bold`, `color`, `labelDensity`, `labelPosition` (`'OutsideEnd'`) |
| `legend` | `show`, `showTitle`, `position` (`'TopRight'`), `labelColor` |
| `dataPoint` | `fill` (with optional `selector`) |
| `lineStyles` | `strokeWidth`, `lineChartType` (`'linear'`), `strokeLineJoin` |
| `zoom` | `show`, `showOnValueAxis` |

### Reference Lines (`y1AxisReferenceLine`)

```json
"y1AxisReferenceLine": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "displayName": { "expr": { "Literal": { "Value": "'Meta'" } } },
    "value": { "expr": { "Literal": { "Value": "90D" } } },
    "lineColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#00E600'" } } } } },
    "transparency": { "expr": { "Literal": { "Value": "0D" } } },
    "dataLabelShow": { "expr": { "Literal": { "Value": "true" } } },
    "dataLabelText": { "expr": { "Literal": { "Value": "'Name'" } } },
    "dataLabelColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#00EA00'" } } } } }
  },
  "selector": { "id": "2" }
}]
```

Multiple reference lines use sequential `selector.id`: `"2"`, `"3"`, `"4"`, etc.

### `HierarchyLevel` field type (for chart axes)

```json
"field": {
  "HierarchyLevel": {
    "Expression": {
      "Hierarchy": {
        "Expression": { "SourceRef": { "Entity": "TABLE" } },
        "Hierarchy": "HierarchyName"
      }
    },
    "Level": "LevelName"
  }
}
```

### `Aggregation` field type (explicit aggregation)

```json
"field": {
  "Aggregation": {
    "Expression": {
      "Column": {
        "Expression": { "SourceRef": { "Entity": "TABLE" } },
        "Property": "COLUMN"
      }
    },
    "Function": 0
  }
}
```

`Function`: 0 = Sum, 1 = Avg, 2 = Min, 3 = Max, 4 = Count, 5 = CountNonNull

## 5. Page Schema (v2.0.0)

> [!WARNING]
> The old `config` property is **invalid** in PBIR v2.0.0 — use `objects` instead.

```json
{
  "$schema": "...page/2.0.0/schema.json",
  "name": "dashboard01",
  "displayName": "Dashboard",
  "displayOption": "FitToPage",
  "height": 720,
  "width": 1280,
  "pageBinding": {
    "name": "hex_id_here",
    "type": "Default",
    "parameters": []
  },
  "objects": {
    "background": [
      {
        "properties": {
          "color": {
            "solid": {
              "color": {
                "expr": {
                  "Literal": { "Value": "'#1B1B2F'" }
                }
              }
            }
          }
        }
      }
    ],
    "outspace": [
      {
        "properties": {
          "color": {
            "solid": {
              "color": {
                "expr": {
                  "Literal": { "Value": "'#1B1B2F'" }
                }
              }
            }
          }
        }
      }
    ]
  }
}
```

> [!NOTE]
> `pageBinding` is auto-generated by PBI Desktop. `outspace` controls the color outside the page area (when the viewport is larger than the page).

---

## 6. Pages Metadata

```json
{
  "$schema": "...pagesMetadata/1.0.0/schema.json",
  "pageOrder": ["page1_id", "page2_id"],
  "activePageName": "page2_id"
}
```

- Page/visual IDs can be human-readable names (e.g., `dashboard01`)
- PBI preserves your custom names after save

---

## 8. PBI Desktop Behavior on Load

What PBI Desktop does when it opens a PBIP project:

1. **Validates JSON** against the declared `$schema`
2. **Strips unrecognized properties** (e.g., `config` → error)
3. **Replaces plain color strings** with `"solid": {}` (theme default)
4. **Regenerates column definitions** with `isNameInferred`, auto lineageTags
5. **Adds `filterConfig`** blocks to visuals automatically
6. **Re-indents JSON** to 2-space indentation
7. **Reorders certain properties** (e.g., `height` before `width`)

---

## 9. JSON Schemas Reference

All schemas published at: [github.com/microsoft/json-schemas/fabric/item/report/definition](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition)

| Schema | Version | Purpose |
|--------|---------|---------|
| `visualContainer` | 2.6.0 | Individual visual definition |
| `visualConfiguration` | 2.2.0 | Visual type, query, objects |
| `page` | 2.0.0 | Page layout and background |
| `pagesMetadata` | 1.0.0 | Page ordering |
| `report` | 3.1.0 | Report settings, themes |
| `versionMetadata` | 1.0.0 | PBIR format version |
| `formattingObjectDefinitions` | 1.4.0 | Formatting property types |
| `semanticQuery` | 1.3.0 | Data query expressions |

---

## 13. PBI Desktop Auto-Normalization Patterns

When Power BI Desktop opens and saves a PBIP project, it normalizes several things:

### z-index (`z` property)
- PBI uses **increments of ~1000** for z-ordering
- First visual: `z: 0`, second: `z: 1000`, third: `z: 2000`, new: `z: 2001`
- Our original `z: 1000` for all 3 cards was renumbered to 0, 1000, 2000

### Tab Order (`tabOrder` property)
- Also uses **increments of 1000**: 0, 1000, 2000
- Our original `tabOrder: 0, 1, 2` was renumbered to 0, 1000, 2000

### filterConfig
- PBI **auto-generates** a `filterConfig` block for each visual
- Contains a unique `name` (hex ID) and the bound field reference
- Filter `type` is typically `"Advanced"`

### Summary of auto-generated properties
| Property | Behavior |
|----------|----------|
| `z` | Renumbered with 1000 increments |
| `tabOrder` | Renumbered with 1000 increments |
| `filterConfig` | Auto-added with unique name |
| `drillFilterOtherVisuals` | Set to `true` by default |
| `howCreated` | Set to `"InsertVisualButton"` on new visuals |
| `pageBinding` | Auto-added to pages with name/type/parameters |
| Column `isNameInferred` | Added to calculated table columns |
| Column `sourceColumn` | Wrapped in brackets: `[ColumnName]` |
| Column `annotation SummarizationSetBy` | Set to `Automatic` |
| Column `changedProperty` | Tracks manual changes (DataType, IsHidden, etc.) |
| TMDL `expression` | Changed to `source` in calculated partitions |
| JSON indentation | Normalized to 2-space indent |

---

## 19. Quick Reference — Files to Edit for Common Tasks

| Task | Files to Edit |
|------|--------------|
| Add new page | `pages/<id>/page.json` + `pages/pages.json` |
| Add built-in visual | `pages/<page>/visuals/<id>/visual.json` |
| Add HTML Content visual | Same as above + `report.json` (`publicCustomVisuals`) |
| Add image visual | visual.json + `report.json` (`resourcePackages`) + image file in `StaticResources/RegisteredResources/` |
| Add slicer | visual.json (+ `syncGroup` for cross-page sync) |
| Add visual group | visual.json with `visualGroup` + set `parentGroupName` on child visuals |
| Add DAX measure | `tables/<table>.tmdl` |
| Add calculated column | `tables/<table>.tmdl` (inline DAX in column definition) |
| Add new table | `tables/<name>.tmdl` + `model.tmdl` (`ref table`) |
| Add relationship | `relationships.tmdl` |
| Change page background | `pages/<id>/page.json` → `objects.background` |
| Change active page | `pages/pages.json` → `activePageName` |
| Change theme | `report.json` → `themeCollection` |
| Add page navigation | visual.json → `visualContainerObjects.visualLink` |
| Add reference line | visual.json → `objects.y1AxisReferenceLine` |

---

## 23. Creating Pages from JSON — Complete Workflow

### Step-by-step: Add a new page via IDE

1. **Create page folder**: `pages/<page_name>/page.json`
2. **Create visuals folder**: `pages/<page_name>/visuals/`
3. **Create each visual**: `pages/<page_name>/visuals/<visual_id>/visual.json`
4. **Register the page**: Add `<page_name>` to `pages/pages.json` → `pageOrder` array
5. **Set active (optional)**: Set `activePageName` in `pages/pages.json`

### Light Theme Color Palette (Proven)

| Role | Color | Hex |
|------|-------|-----|
| Page Background | Soft gray | `#F7F9FB` |
| Card Background | White | `#FFFFFF` |
| Card Border | Very light gray | `#F1F5F9` |
| Primary Text | Near black | `#1C1C1C` |
| Muted Text | Slate gray | `#64748B` |
| Accent Blue | Bright blue | `#3B82F6` |
| Dark Card BG | Near black | `#1F2937` |
| Accent Purple | Violet | `#A855F7` |
| Accent Green | Emerald | `#10B981` |
| Axis/Grid Lines | Light slate | `#E2E8F0` |

### Light Theme KPI Card Pattern (DAX)

```tmdl
	measure LightKpiViews =
			VAR _value = SUM(MonthlyMetrics[ThisYear])
			VAR _change = DIVIDE(_value - SUM(MonthlyMetrics[LastYear]), SUM(MonthlyMetrics[LastYear]), 0) * 100
			RETURN
			"<div style='font-family:Segoe UI,sans-serif; background:#3B82F6; border-radius:16px; padding:min(16px,3vh) min(20px,3vw); color:white; width:100%; height:100vh; box-sizing:border-box; display:flex; flex-direction:column; justify-content:space-between;'>" &
			"<div style='display:flex; justify-content:space-between; align-items:center;'>" &
			"<span style='font-size:clamp(10px,2.5vw,13px); opacity:0.85;'>Views</span>" &
			"<svg width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.7)' stroke-width='2'><polyline points='22 12 18 12 15 21 9 3 6 12 2 12'/></svg>" &
			"</div>" &
			"<div style='font-size:clamp(20px,5vw,32px); font-weight:700;'>" & FORMAT(_value, "#,##0") & "</div>" &
			"<div style='font-size:clamp(9px,2vw,11px); opacity:0.75; text-align:right;'>+" & FORMAT(_change, "0.00") & "%</div>" &
			"</div>"
		lineageTag: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

---

## 24. Visual Container Objects — Extended Patterns

### Border with Rounded Corners (from PBI Desktop)

When you add borders in PBI Desktop, it generates this structure:

```json
"border": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } },
    "color": {
      "solid": {
        "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } }
      }
    },
    "radius": { "expr": { "Literal": { "Value": "20D" } } },
    "width": { "expr": { "Literal": { "Value": "2D" } } }
  }
}]
```

### Border with ThemeDataColor (PBI auto-generates this)
```json
"color": {
  "solid": {
    "color": {
      "expr": {
        "ThemeDataColor": { "ColorId": 0, "Percent": 0 }
      }
    }
  }
}
```

### Visual Tooltip Transparency
```json
"visualTooltip": [{
  "properties": {
    "transparency": { "expr": { "Literal": { "Value": "100D" } } }
  }
}]
```

### Background Show = false (hides card background entirely)
```json
"background": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "false" } } },
    "transparency": { "expr": { "Literal": { "Value": "100D" } } }
  }
}]
```

### Drop Shadow
```json
"dropShadow": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "true" } } }
  }
}]
```

> [!TIP]
> PBI reformats all JSON to **2-space indent** on save. Our 4-space files get normalized automatically.

---

## 30. PBIR Deep Dive: Native Slicers & Stateful Bookmarks

> [!CAUTION]
> When building custom UI flows (like a Filter Drawer), it is a mistake to think of Bookmarks purely as "Visibility Toggles." In Power BI PBIR schema, **Bookmarks are Dashboard State Snapshots.**

### Native Slicer Architecture in PBIR
When a user interacts with a standard Power BI slicer (e.g., selecting "Beta" in the Team dropdown), the state is not saved in a simple string. It is saved in the visual's `objects.general.filter` property as an Abstract Syntax Tree (AST).

**Example of an active Slicer selection (`Team = 'Beta'`):**
```json
"objects": {
  "general": [
    {
      "properties": {
        "filter": {
          "filter": {
            "Version": 2,
            "From": [{"Name": "s", "Entity": "SalesTeamData", "Type": 0}],
            "Where": [
              {
                "Condition": {
                  "In": {
                    "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "s"}}, "Property": "Team"}}],
                    "Values": [[{"Literal": {"Value": "'Beta'"}}]]
                  }
                }
              }
            ]
          }
        }
      }
    }
  ]
}
```

### Stateful Bookmarks
Because slicers mutate the data state, Bookmarks have to accurately capture whether they intend to **restore data state** or **just toggle UI layout**. 

A true "Dashboard State Snapshot" Bookmark (like one created manually in PBI Desktop) doesn't just toggle a `visualContainerGroup`'s `isHidden` property. It maps through every single `visualContainer` on the page and caches the exact active filters (`byExpr`) assigned to them.

**Example of a Stateful Bookmark (`explorationState.sections.page_name.visualContainers.visual_name`):**
```json
"visualContainers": {
  "my_bar_chart": {
    "filters": {
      "byExpr": [
        {
          "name": "random_guid",
          "type": "Categorical",
          "expression": {
            "Column": {
              "Expression": {"SourceRef": {"Entity": "TrafficData"}},
              "Property": "Category"
            }
          },
          "howCreated": 0
        }
      ]
    }
  }
}
```

### The Takeaway for PBIR Code Editing
1. **Never hand-write data filters in PBIR JSON**: The AST for `objects.general.filter` inside slicers, or `filters.byExpr` inside bookmarks, is far too rigid and complex to manually guess. 
2. **If you need a Data Snapshot**: Let the user create the slicers and the bookmarks via the Power BI Desktop GUI. 
3. **If you are only doing UI Animation (like opening a drawer)**: You can hand-write a bare-bones bookmark JSON that **ONLY** contains a `visualContainerGroups` array toggling `isHidden`, avoiding the `visualContainers` filter snapshot entirely. Ensure `options.suppressData` is set to `true` to prevent the bookmark from accidentally resetting user slicer selections when they open the drawer.

---

## 35. Bookmark JSON Schema (v2.1.0) — Documentação Completa

> [!IMPORTANT]
> Seção 30 descreve bookmarks conceitualmente. Esta seção documenta o **esquema real dos arquivos `.bookmark.json`** e `bookmarks.json`, extraídos do projeto Databricks Gov.

### bookmarks.json — Índice de Bookmarks

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmarksMetadata/1.0.0/schema.json",
  "items": [
    { "name": "bm_abrir_gaveta" },
    { "name": "34ca1d6b40e18ee13081" }
  ]
}
```

- Localização: `Report/definition/bookmarks/bookmarks.json`
- `items` é uma array de objetos com apenas `"name"` — o nome do arquivo `.bookmark.json` (sem extensão)
- PBI Desktop usa hex IDs quando cria automaticamente; nomes legíveis como `bm_abrir_gaveta` também são aceitos e preservados

### .bookmark.json — UI Toggle (gaveta de filtros)

Bookmark **mínimo** para alternar visibilidade de elementos — sem capturar estado de slicers:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json",
  "displayName": "Abrir Gaveta de Filtros",
  "name": "bm_abrir_gaveta",
  "options": {
    "suppressData": true
  },
  "explorationState": {
    "version": "1.0",
    "activeSection": "00_visao_geral",
    "sections": {
      "00_visao_geral": {
        "visualContainers": {
          "sli_ano": {
            "singleVisual": {
              "visualType": "slicer",
              "objects": {}
            }
          },
          "sli_gaveta_label": {
            "singleVisual": {
              "visualType": "textbox",
              "objects": {}
            }
          }
        }
      }
    }
  }
}
```

### Regras do Bookmark de UI Toggle

| Propriedade | Valor | Obrigatório | Função |
|-------------|-------|-------------|--------|
| `options.suppressData` | `true` | **Sim** | Impede que o bookmark redefina os filtros ativos dos slicers |
| `activeSection` | nome da página | Sim | Página onde o bookmark atua |
| `visualContainers` | objeto vazio `{}` por visual | Sim | Lista os visuais presentes na página |
| `objects` | `{}` | Sim | Vazio = não sobrescreve estado de formatação do visual |

> [!CAUTION]
> **`suppressData: true` é obrigatório em bookmarks de UI.** Sem ele, clicar no bookmark reseta as seleções de slicer do usuário para o estado salvo no momento da criação do bookmark — comportamento indesejado em gavetas/sidebars.

> [!WARNING]
> O `visualContainers` precisa listar **todos** os visuais da página (incluindo shapes, textboxes, slicers) — mesmo que o objeto seja `{}`. Visuais omitidos podem ter comportamento imprevisível ao aplicar o bookmark.

### Workflow: Criação de Bookmark de UI via IDE

1. Criar o arquivo `.bookmark.json` na pasta `Report/definition/bookmarks/`
2. Adicionar o `name` ao array `items` em `bookmarks.json`
3. No visual que deve ser mostrado/ocultado, adicionar `visualLink` com `type: 'BookmarkNavigation'` e `bookmarkName` apontando para o bookmark

---

## 36. Propriedades de Visual Não Documentadas (Descobertas no Projeto)

### 36.1 `subTitle` em visualContainerObjects

Subtítulo abaixo do título principal do visual — ideal para disclaimers, unidade de medida, ou contexto da análise:

```json
"visualContainerObjects": {
  "title": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "text": { "expr": { "Literal": { "Value": "'Título Principal'" } } },
      "fontSize": { "expr": { "Literal": { "Value": "13D" } } },
      "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#09090B'" } } } } },
      "alignment": { "expr": { "Literal": { "Value": "'left'" } } }
    }
  }],
  "subTitle": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "text": { "expr": { "Literal": { "Value": "'Estimativa indicativa · variabilidade histórica ±53% · não usar para metas precisas'" } } },
      "fontSize": { "expr": { "Literal": { "Value": "9D" } } },
      "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#71717A'" } } } } }
    }
  }]
}
```

> [!TIP]
> `subTitle` é perfeito para colocar disclaimers em gráficos de forecast, indicar a fonte dos dados, ou contextualizar a métrica sem poluir o título principal.

### 36.2 Schema v2.7.0 do visualContainer

O projeto Databricks Gov usa `visualContainer/2.7.0` (a versão documentada anteriormente era 2.6.0). A URL do schema é:

```
https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json
```

> [!NOTE]
> As propriedades são compatíveis com 2.6.0. A mudança de versão ocorre ao salvar com versões mais novas do Power BI Desktop. Sempre espelhe a versão existente no projeto — não assuma a mais nova.

### 36.3 `displayName` em Projeções (Alias de Coluna)

Para renomear uma coluna na visualização sem alterar o modelo, use `displayName` na projeção:

```json
"projections": [
  {
    "field": {
      "Column": {
        "Expression": { "SourceRef": { "Entity": "licitacoes_2019_2024" } },
        "Property": "nome"
      }
    },
    "queryRef": "licitacoes_2019_2024.nome",
    "nativeQueryRef": "nome",
    "displayName": "Fornecedor"
  }
]
```

- `displayName`: nome exibido ao usuário (cabeçalho da coluna na tabela)
- `nativeQueryRef`: nome original no modelo
- `queryRef`: referência interna usada pelo engine de query

### 36.4 `selector.data.scopeId.Measure` — Colorir Série por Medida

Diferente de colorir por valor de coluna (`scopeId.Comparison`), para colorir uma **linha específica num gráfico com múltiplas medidas** usa-se `scopeId.Measure`:

```json
// ✅ Colorir a série "Valor Total" de azul num lineChart com múltiplas medidas
"dataPoint": [
  {
    "properties": {
      "fill": {
        "solid": {
          "color": { "expr": { "Literal": { "Value": "'#3B82F6'" } } }
        }
      }
    },
    "selector": {
      "data": [{
        "scopeId": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "_Medidas" } },
            "Property": "Valor Total"
          }
        }
      }]
    }
  },
  {
    "properties": {
      "fill": {
        "solid": {
          "color": { "expr": { "Literal": { "Value": "'#F59E0B'" } } }
        }
      }
    },
    "selector": {
      "data": [{
        "scopeId": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "_Medidas" } },
            "Property": "Valor Previsto"
          }
        }
      }]
    }
  }
]
```

**Resumo dos tipos de `scopeId`:**

| Tipo | Quando usar |
|------|-------------|
| `scopeId.Measure` | Colorir série num gráfico com múltiplas medidas no mesmo eixo |
| `scopeId.Comparison` | Colorir barra/ponto de um valor específico de uma coluna |
| `selector.metadata` | Colorir por `queryRef` (nome da série como string) |
| Sem selector | Cor padrão da primeira série |

---

## 38. `tableEx` Visual — Schema Completo

`tableEx` é o `visualType` da tabela nativa do Power BI (não confundir com `matrix`).

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "tbl_top10_forn",
  "position": { "x": 24, "y": 526, "z": 7000, "height": 186, "width": 1231, "tabOrder": 7000 },
  "visual": {
    "visualType": "tableEx",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "licitacoes_2019_2024" } },
                  "Property": "nome"
                }
              },
              "queryRef": "licitacoes_2019_2024.nome",
              "nativeQueryRef": "nome",
              "displayName": "Fornecedor"
            },
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "_Medidas" } },
                  "Property": "Qtd Licitacoes"
                }
              },
              "queryRef": "_Medidas.Qtd Licitacoes",
              "nativeQueryRef": "Qtd Licitacoes"
            },
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "_Medidas" } },
                  "Property": "Valor Total"
                }
              },
              "queryRef": "_Medidas.Valor Total",
              "nativeQueryRef": "Valor Total"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

**Diferenças do tableEx vs outros visuais:**
- Role única: `Values` (todas as colunas e medidas vão na mesma projeção)
- `displayName` em cada projeção para renomear colunas
- Colunas e medidas podem ser misturadas livremente no mesmo array `Values`
- Sem `objects` é válido — usa formatação padrão do tema

---

## Seção 44 — Catálogo de Padrões de Slicer (Segmentação de Dados)

> Extraído de 54+ slicers reais em 5 dashboards. Data: 2026-04-23

### 44.1 Distribuição por modo
- **Dropdown**: 96% dos casos — modo padrão absoluto
- **Between**: apenas para ranges de data (DataAlvará, etc.)
- **Tile / List / Relative Date**: não observados nesses dashboards

### 44.2 Configurações canônicas

```json
// Dropdown padrão mínimo
{
  "visualType": "slicer",
  "singleVisual": {
    "objects": {
      "data": [{ "properties": { "mode": { "expr": { "Literal": { "Value": "'Dropdown'" } } } } }],
      "header": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }],
      "items": [{ "properties": { "textSize": { "expr": { "Literal": { "Value": "12D" } } } } }]
    }
  }
}
```

```json
// Between (intervalo de datas)
{
  "data": [{ "properties": { "mode": { "expr": { "Literal": { "Value": "'Between'" } } } }],
  "slider": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }],
  "date": [{ "properties": { "textSize": { "expr": { "Literal": { "Value": "15D" } } } } }]
}
```

### 44.3 Recursos avançados observados

**Seleção invertida** (filtro "todos exceto"):
```json
"filterConfig": [{ "properties": {
  "isInvertedSelectionMode": { "expr": { "Literal": { "Value": "true" } } }
} }]
```
Usado em: ESTRATÉGICO (Projeto, Fornecedor), Databrick Gov (categoria_ia).

**Seleção única obrigatória**:
```json
"general": [{ "properties": {
  "strictSingleSelect": { "expr": { "Literal": { "Value": "true" } } }
} }]
```

**Sincronização entre páginas**:
```json
// Em syncSlicers.json da página ou diretamente no visual
"syncConfig": { "group": "NomeDoGrupo", "filterChanges": true, "fieldChanges": true }
```
SyncGroups observados: `"FiltroAno"` (Databrick Gov), `"Projeto"` e `"Fornecedores"` (ESTRATÉGICO).

### 44.4 Dimensões por canvas

| Canvas      | Largura típica | Altura típica | font items | font título |
|-------------|----------------|---------------|------------|-------------|
| 1280×720    | 247px          | 90px          | 8–10D      | 10D         |
| 1800×900    | 230px          | 107px         | 14D        | 14D         |
| 1920×1080   | 262–554px      | 75–102px      | 18D        | 20D         |
| 2200×1200   | 250px          | 93–96px       | 16D        | 16D         |

### 44.5 Padrão de título: header oculto + visualContainerObjects.title

Em 100% dos casos observados, o header interno do slicer fica oculto e o título vem do container:
```json
// Dentro do visual
"header": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }]

// Em visualContainerObjects
"title": [{ "properties": {
  "show":      { "expr": { "Literal": { "Value": "true" } } },
  "text":      { "expr": { "Literal": { "Value": "'Mês'" } } },
  "fontSize":  { "expr": { "Literal": { "Value": "10D" } } },
  "bold":      { "expr": { "Literal": { "Value": "false" } } },
  "alignment": { "expr": { "Literal": { "Value": "'left'" } } }
} }]
```

---

## Seção 45 — Padrões de Interatividade (Bookmarks, Botões, Gavetas)

> Extraído de 30+ bookmarks e 50+ visualLinks em 5 dashboards. Data: 2026-04-23

### 45.1 Três padrões de gaveta observados

#### Padrão A — Toggle de VisualGroup (Databrick Gov)
O grupo de visuais sai/entra do canvas via `isHidden` em bookmark:
```
BookmarkA (gaveta aberta):  VisualGroup.isHidden = false
BookmarkB (gaveta fechada): VisualGroup.isHidden = true
Botão funil → BookmarkA
Botão X     → BookmarkB
Botão funil-x → ClearAllSlicers
```
Os slicers e labels ficam dentro do VisualGroup. Quando oculto, o grupo desliza para fora do canvas (`x > canvas_width`).

#### Padrão B — OutspacePane expand/collapse (Contratações DGT)
O painel lateral nativo do Power BI é expandido/contraído via bookmark:
```
BookmarkA (abrir):  outspacePane.expanded = true
BookmarkB (fechar): outspacePane.expanded = false
BookmarkC (limpar): suppressData=true, suppressDisplay=true → ClearAllSlicers sem mudar estado
```
3 botões dedicados: abrir, fechar, limpar (ícones distintos).

#### Padrão C — Visual Groups sobrepostos (Relatório Pagamentos)
Dois grupos ocupam a mesma área; bookmarks alternam qual está visível:
```
VisualGroup "Menu Escondido" → isHidden: false (padrão)
VisualGroup "Menu Exibido"   → isHidden: true  (padrão)
Bookmark alterna os dois estados simultaneamente
```

### 45.2 Estrutura de bookmark (campos obrigatórios)

```json
{
  "name": "id_unico",
  "displayName": "Nome Legível",
  "suppressData": true,
  "explorationState": {
    "version": "1.0",
    "activeSection": "page-id",
    "sections": {
      "page-id": {
        "visualContainers": {
          "visual-name": {
            "singleVisual": {
              "visualType": "slicer",
              "objects": {}
            }
          }
        }
      }
    }
  }
}
```

`suppressData: true` = bookmark só muda estado visual (show/hide), não dados.
`suppressActiveSection: true` = bookmark afeta todas as páginas, não só a ativa.
`suppressDisplay: true` = bookmark não muda visibilidade de visuais (só dados/filtros).

### 45.3 Tipos de visualLink (botões)

| Tipo              | Uso observado                    | Visual type que usa    |
|-------------------|----------------------------------|------------------------|
| `Bookmark`        | Abrir/fechar gaveta, navegação   | image, actionButton    |
| `ClearAllSlicers` | Resetar todos os filtros         | image                  |
| `PageNavigation`  | Navegar para outra página        | image, actionButton    |
| `URL`             | Não observado                    | —                      |

```json
// Imagem com visualLink para bookmark
"visualLink": {
  "show": { "expr": { "Literal": { "Value": "true" } } },
  "type": { "expr": { "Literal": { "Value": "'Bookmark'" } } },
  "bookmark": { "expr": { "Literal": { "Value": "'id_do_bookmark'" } } }
}

// ActionButton com texto
"visualType": "actionButton",
"singleVisual": {
  "objects": {
    "text": [{ "properties": {
      "text":      { "expr": { "Literal": { "Value": "'X'" } } },
      "fontSize":  { "expr": { "Literal": { "Value": "22D" } } }
    } }],
    "icon": [{ "properties": { "iconType": { "expr": { "Literal": { "Value": "'Blank'" } } } } }]
  },
  "vcObjects": {
    "visualLink": [{ "properties": {
      "type":     { "expr": { "Literal": { "Value": "'Bookmark'" } } },
      "bookmark": { "expr": { "Literal": { "Value": "'id_bookmark'" } } }
    } }]
  }
}
```

### 45.4 Configurações globais de report.json

Padrão observado em todos os dashboards:
```json
{
  "filterPaneHiddenInEditMode": true,
  "defaultDrillFilterOtherVisuals": true,
  "outspacePane": { "expanded": false }
}
```

### 45.5 Ícones de controle mais usados (StaticResources)

| Função        | Ícone comum             | Tipo de link     |
|---------------|-------------------------|------------------|
| Abrir filtros | funnel.svg, filter.png  | Bookmark (abrir) |
| Fechar painel | x.svg, Bot_o_fechar.png | Bookmark (fechar)|
| Limpar filtros| funnel-x.svg, clear-filter.png | ClearAllSlicers / Bookmark |
| Navegar →     | arrow-right.svg         | PageNavigation   |
| Navegar ←     | arrow-left.svg          | PageNavigation   |

---

## Seção 48 — Novos Visual Types: Governança BI e projeto.pbip

> Descobertas dos dois dashboards finais. Data: 2026-04-23

### 48.1 Canvas sizes adicionais

| Dimensão       | Dashboard          |
|----------------|--------------------|
| 1710 × 800     | Governança BI (1)  |
| 1678 × 799     | Governança BI pág 2|

### 48.2 lineClusteredColumnComboChart (combo coluna + linha)

```
Exemplo: 1252.31 × 508.33px (canvas 1710×800)
Y (coluna): métrica principal (ex: Disponibilidade %)
Y2 (linha): meta ou comparativo (ex: Meta de Disponibilidade)
Labels: fontSize=11pt, bold=true, position=OutsideEnd
enableDetailDataLabel: true
```
Ideal para mostrar realizado vs meta ao longo do tempo. Compartilha eixo X com dois eixos Y independentes.

### 48.3 Gauge customizado de marketplace

Visual type: `dg5AAA90EFEFE747CB9357C4FC19B85A58`
Campos obrigatórios: `pointerValue`, `min`, `max`, `redStart`, `redEnd`, `yellowStart`, `yellowEnd`
```dax
-- Constantes de meta para o gauge
Maximo      = 1
Minimo      = 0
targetstart = 0.9   -- início da zona verde
targetend   = 1
mediastart  = 0.7   -- início da zona amarela
mediaend    = 0.9
Meta        = 0.9
Meta_legenda = "Meta: 90%"
```
**Importante**: opaco para o LayoutValidator — não gerar via JSON diretamente, usar apenas se o custom visual estiver instalado.

### 48.4 Deneb / Vega-Lite (projeto.pbip)

Visual type: `deneb7E15AEF80B9E4D4F8E12924291ECE89A`

```json
// Configuração mínima no visual.json
{
  "visualType": "deneb7E15AEF80B9E4D4F8E12924291ECE89A",
  "singleVisual": {
    "objects": {
      "vega": [{
        "properties": {
          "jsonSpec": { "expr": { "Literal": { "Value": "'{ ... spec Vega-Lite ... }'" } } },
          "provider":  { "expr": { "Literal": { "Value": "'vegaLite'" } } },
          "themeMode": { "expr": { "Literal": { "Value": "'light'" } } }
        }
      }]
    }
  }
}
```
Permite criar qualquer tipo de chart via JSON declarativo. Não preditível pelo LayoutValidator (spec define o espaço internamente).

### 48.5 htmlContent (projeto.pbip)

Visual type: `htmlContent443BE3AD55E043BF878BED274D3A6855`

A medida DAX retorna uma string HTML/CSS completa que é renderizada dentro do visual:
```dax
HtmlKpiViews = "
<div style='font-family: Segoe UI; background: linear-gradient(135deg,#1e3a5f,#2d6a9f);
             border-radius: 12px; padding: 16px; color: white;'>
  <div style='font-size: 11px; opacity: 0.7; text-transform: uppercase;'>Views</div>
  <div style='font-size: 32px; font-weight: bold;'>" & FORMAT([TotalViews], "#,##0") & "</div>
</div>"
```

Padrões CSS usados:
- **Glass morphism**: `backdrop-filter: blur(10px); background: rgba(255,255,255,0.1)`
- **Animated gradient**: `@keyframes br { background-position: 0%→100%→0% }`
- **SVG gauge**: `stroke-dasharray: 283; stroke-dashoffset: calculado`
- **Responsive font**: `font-size: clamp(12px, 2.5vw, 14px)`
- **HTML table dinâmica**: via `CONCATENATEX` — gera linhas de tabela por linha de dado

### 48.6 Shape como hotspot invisível para ação

```json
// Shape 100% transparente com visualLink — o "botão invisível" sobre uma imagem
{
  "visualType": "shape",
  "singleVisual": {
    "objects": {
      "fill": [{ "properties": {
        "transparency": { "expr": { "Literal": { "Value": "100D" } } }
      } }]
    },
    "vcObjects": {
      "visualLink": [{ "properties": {
        "type":     { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
        "navigationSection": { "expr": { "Literal": { "Value": "'page-id'" } } }
      } }]
    }
  }
}
```
Permite que qualquer área clicável do canvas ative uma ação sem precisar de imagem ou botão explícito.

---

## Seção 51 — Templates Canônicos de Chart visual.json + Gaps Resolvidos

> Adicionado em 2026-04-24. Fecha GAP-A1, GAP-A2, GAP-A3, GAP-M1, GAP-M2, GAP-M5 da Seção 50.

---

### 51.1 Estrutura mínima de qualquer chart (esqueleto comum)

Todo chart compartilha esta estrutura — apenas `visualType` e os `projections` mudam.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "bar_01",
  "position": { "x": 0, "y": 0, "z": 1000, "height": 300, "width": 500, "tabOrder": 1000 },
  "visual": {
    "visualType": "<tipo>",
    "query": {
      "queryState": {
        "Category": { "projections": [
          {
            "field": { "Column": { "Expression": { "SourceRef": { "Entity": "Tabela" } }, "Property": "Coluna" } },
            "queryRef": "Tabela.Coluna",
            "nativeQueryRef": "Coluna",
            "active": true
          }
        ]},
        "Y": { "projections": [
          {
            "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Medidas" } }, "Property": "Valor" } },
            "queryRef": "Medidas.Valor",
            "nativeQueryRef": "Valor"
          }
        ]}
      },
      "sortDefinition": {
        "sort": [{ "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Medidas" } }, "Property": "Valor" } }, "direction": "Descending" }],
        "isDefaultSort": true
      }
    },
    "drillFilterOtherVisuals": true
  }
}
```

**Regras críticas:**
- `queryRef` = `"Entidade.Propriedade"` (concatenação com ponto)
- `nativeQueryRef` = nome exibido no visual (pode ser diferente da propriedade)
- `active: true` na Category = dimensão principal ativa no eixo
- `objects` e `visualContainerObjects` são OPCIONAIS — se omitidos, usa defaults do tema
- Sem `objects` o visual é válido e abre no PBI Desktop

---

### 51.2 clusteredBarChart (barras horizontais — ranking)

**Quando usar:** ranking de categorias, comparação entre itens de uma lista.

**Roles:** `Category` (dimensão/coluna), `Y` (medida).

```json
"visualType": "clusteredBarChart"
```

**Observações do template real:**
- `valueAxis.show: false` + `valueAxis.showAxisTitle: false` = eixo Y oculto (padrão moderno)
- `categoryAxis.showAxisTitle: false` = sem título de eixo  
- `labels.bold: true` = rótulos em negrito

---

### 51.3 clusteredColumnChart (colunas verticais)

**Quando usar:** comparação temporal por período curto, distribuição por categoria.

**Roles:** `Category` (dimensão), `Y` (medida), `Tooltips` (medidas extras no tooltip — opcional).

```json
"visualType": "clusteredColumnChart"
```

**Role adicional Tooltips:**
```json
"Tooltips": { "projections": [{
  "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Tab" } }, "Property": "MedidaExtra" } },
  "queryRef": "Tab.MedidaExtra",
  "nativeQueryRef": "Label do Tooltip",
  "displayName": "Label do Tooltip"
}]}
```

---

### 51.4 lineChart (linha temporal)

**Quando usar:** tendência ao longo do tempo, evolução de KPI.

**Roles:** `Category` (hierarquia de data OU coluna), `Y` (medida).

**Eixo de data com hierarquia automática do PBI (mais comum):**
```json
"Category": { "projections": [
  {
    "field": { "HierarchyLevel": {
      "Expression": { "Hierarchy": { "Expression": { "PropertyVariationSource": {
        "Expression": { "SourceRef": { "Entity": "Calendario" } },
        "Name": "Variation",
        "Property": "Date"
      }}, "Hierarchy": "Hierarquia de datas" }},
      "Level": "Ano"
    }},
    "queryRef": "Calendario.Date.Variation.Hierarquia de datas.Ano",
    "nativeQueryRef": "Date Ano",
    "active": true
  },
  {
    "field": { "HierarchyLevel": {
      "Expression": { "Hierarchy": { "Expression": { "PropertyVariationSource": {
        "Expression": { "SourceRef": { "Entity": "Calendario" } },
        "Name": "Variation",
        "Property": "Date"
      }}, "Hierarchy": "Hierarquia de datas" }},
      "Level": "Mês"
    }},
    "queryRef": "Calendario.Date.Variation.Hierarquia de datas.Mês",
    "nativeQueryRef": "Date Mês",
    "active": true
  }
]}
```

**Observações:**
- Múltiplos níveis (Ano + Mês) = permite drill-down
- `active: false` em níveis inferiores (Dia) = visível no drill mas não exibido por default
- Para eixo de data simples (sem hierarquia): usar `Column` normal

---

### 51.5 donutChart (rosca)

**Quando usar:** composição de partes do todo (máx 5-6 fatias — anti-padrão com muitas fatias).

**Roles:** `Category` (dimensão), `Y` (medida).

```json
"visualType": "donutChart"
```

**objects relevantes:**
```json
"labels": [{ "properties": {
  "labelStyle": { "expr": { "Literal": { "Value": "'Category, data value, percent of total'" } } },
  "labelDisplayUnits": { "expr": { "Literal": { "Value": "1D" } } }
}}],
"legend": [{ "properties": { "show": { "expr": { "Literal": { "Value": "true" } } } } }]
```

---

### 51.6 stackedAreaChart (área empilhada)

**Quando usar:** composição ao longo do tempo (ex: execução vs. previsto por período).

**Roles:** `Category` (HierarchyLevel de data OU coluna), `Y` (medida).

```json
"visualType": "stackedAreaChart"
```

**Novidades descobertas neste tipo:**
- `visualContainerObjects.title.heading: "'Heading3'"` — define hierarquia tipográfica do título
- `visualContainerObjects.title.titleWrap: true` — permite quebra de linha no título
- `visualContainerObjects.divider` — linha separadora entre título e visual
- `visualContainerObjects.visualHeader.show` — controla visibilidade do header completo
- `selector.metadata: "Sum(Tabela.Coluna)"` — colore serie específica pelo nome da agregação

---

### 51.7 lineClusteredColumnComboChart (combo coluna + linha)

**Quando usar:** realizado (coluna) vs. meta (linha) no mesmo gráfico.

**Roles:** `Category` (eixo X compartilhado), `Y` (colunas — eixo primário), `Y2` (linha — eixo secundário).

```json
"visualType": "lineClusteredColumnComboChart"
// também existe: "lineStackedColumnComboChart" (coluna empilhada + linha)
```

**Estrutura com Y2 (eixo secundário para a linha):**
```json
"queryState": {
  "Category": { "projections": [/* coluna de data ou categoria */] },
  "Y":  { "projections": [/* medida para as colunas */] },
  "Y2": { "projections": [
    {
      "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "TabMeta" } }, "Property": "Meta" } },
      "queryRef": "TabMeta.Meta",
      "nativeQueryRef": "Meta"
    }
  ]}
}
```

**objects exclusivos do combo:**
```json
"valueAxis": [{ "properties": {
  "show": { "expr": { "Literal": { "Value": "false" } } },
  "secShow": { "expr": { "Literal": { "Value": "false" } } },
  "secLabelColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#FF0000'" } } } } }
}}],
"lineStyles": [{ "properties": {
  "strokeLineJoin": { "expr": { "Literal": { "Value": "'miter'" } } },
  "lineStyle": { "expr": { "Literal": { "Value": "'solid'" } } },
  "showMarker": { "expr": { "Literal": { "Value": "false" } } }
}}],
"seriesLabels": [{ "properties": {
  "show": { "expr": { "Literal": { "Value": "false" } } },
  "seriesPosition": { "expr": { "Literal": { "Value": "'Left'" } } }
}}]
```

**Colorir serie específica por medida (selector.metadata):**
```json
"dataPoint": [
  { "properties": { "fill": { "solid": { "color": { "expr": { "Literal": { "Value": "'#0097B2'" } } } } } },
    "selector": { "metadata": "TabMeta.Meta" } }
]
```

---

### 51.8 ~~GAP-A2~~ RESOLVIDO: filterConfig de visual-level filter (ExibirHistorico)

O `filterConfig` é o filtro aplicado ao visual via painel de filtros do PBI Desktop. O padrão para ocultar/mostrar visuals com medida de controle é **"medida is NOT null"**:

```json
"filterConfig": {
  "filters": [
    {
      "name": "4933e43dd14fec8ce815",
      "field": {
        "Measure": {
          "Expression": { "SourceRef": { "Entity": "Medidas" } },
          "Property": "ExibirHistorico"
        }
      },
      "type": "Advanced",
      "filter": {
        "Version": 2,
        "From": [{ "Name": "m", "Entity": "Medidas", "Type": 0 }],
        "Where": [{
          "Condition": {
            "Not": {
              "Expression": {
                "Comparison": {
                  "ComparisonKind": 0,
                  "Left": { "Measure": { "Expression": { "SourceRef": { "Source": "m" } }, "Property": "ExibirHistorico" } },
                  "Right": { "Literal": { "Value": "null" } }
                }
              }
            }
          }
        }]
      },
      "howCreated": "User"
    }
  ]
}
```

**Por que "NOT null" e não "= 1":** A medida `ExibirHistorico = IF(ISFILTERED(T[col]), 1, BLANK())`. O PBI trata BLANK() como null. O filtro "NOT null" passa qualquer valor não-blank — ou seja, mostra o visual quando a medida retornar 1.

**`name` do filtro:** hex de 20 chars gerado aleatoriamente. Usar `uuid.uuid4().hex[:20]` em Python.

---

### 51.9 ~~GAP-A3~~ RESOLVIDO: report.json mínimo completo

Versão sem custom visuals, sem imagens, tema base padrão do PBI:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.2.0/schema.json",
  "themeCollection": {
    "baseTheme": {
      "name": "CY25SU10",
      "reportVersionAtImport": {
        "visual": "2.1.0",
        "report": "3.0.0",
        "page": "2.3.0"
      },
      "type": "SharedResources"
    }
  },
  "settings": {
    "useStylableVisualContainerHeader": true,
    "exportDataMode": "AllowSummarized",
    "defaultDrillFilterOtherVisuals": true,
    "allowChangeFilterTypes": true,
    "useEnhancedTooltips": true,
    "useDefaultAggregateDisplayName": true
  }
}
```

**Para adicionar gaveta de filtros (outspacePane oculto por padrão):**
```json
"objects": {
  "outspacePane": [{ "properties": { "expanded": { "expr": { "Literal": { "Value": "false" } } } } }],
  "section": [{ "properties": { "verticalAlignment": { "expr": { "Literal": { "Value": "'Top'" } } } } }]
}
```

---

### 51.10 ~~GAP-M1~~ RESOLVIDO: version.json

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
  "version": "2.0.0"
}
```

Arquivo fixo — nunca mudar.

---

### 51.11 ~~GAP-M2~~ RESOLVIDO: cultures/pt-BR.tmdl

**Não gerar.** O arquivo é auto-gerado pelo PBI Desktop com metadata linguística de cada medida e coluna. Tem 46k+ tokens por projeto de tamanho médio. Omitir completamente — o PBI cria na primeira abertura.

---

### 51.12 ~~GAP-M5~~ RESOLVIDO: syncSlicers.json

**Não existe.** Confirmado por busca em todos os projetos. O sync de slicer fica 100% dentro do `visual.json` do slicer:

```json
"syncConfig": {
  "group": "FiltroAno",
  "filterChanges": true,
  "fieldChanges": true
}
```

Fica dentro de `visual.objects.general[0].properties` ou diretamente em `visual.syncConfig` (depender da versão — verificar no visual.json real do slicer existente).

---

### 51.13 Status final dos Gaps (pós Seção 51)

| Gap | Status |
|---|---|
| GAP-C1 (.pbip raiz) | ✅ RESOLVIDO (Seção 50) |
| GAP-C2 (definition.pbir) | ✅ RESOLVIDO (Seção 50) |
| GAP-C3 (M query CSV/Excel) | ⚠️ PENDENTE — única ação que requer PBI Desktop |
| GAP-A1 (chart templates) | ✅ RESOLVIDO (Seção 51.2–51.7) |
| GAP-A2 (visual-level filter) | ✅ RESOLVIDO (Seção 51.8) |
| GAP-A3 (report.json mínimo) | ✅ RESOLVIDO (Seção 51.9) |
| GAP-M1 (version.json) | ✅ RESOLVIDO (Seção 51.10) |
| GAP-M2 (cultures TMDL) | ✅ RESOLVIDO (Seção 51.11) |
| GAP-M3 (convenção IDs) | ✅ RESOLVIDO (Seção 50.4) |
| GAP-M4 (Mode B leitura) | Planejado para Fase 2 |
| GAP-M5 (syncSlicers.json) | ✅ RESOLVIDO (Seção 51.12) |
| GAP-B1 (tooltip page ref) | Baixa prioridade — Fase 2+ |
| GAP-B2 (conditional format tableEx) | Baixa prioridade — Fase 2+ |

**Única pendência bloqueante para Fase 1:** GAP-C3 (M query CSV/Excel para Mode C). Mode A e Mode B podem começar sem isso.

*Seção 51 adicionada em 2026-04-24*

---

