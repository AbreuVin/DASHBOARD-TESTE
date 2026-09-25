# Design, layout e padrões de dashboards

> Extraído de `pbir_research_and_learnings.md` (aprendizados práticos em projetos TJBA). Seções mantidas na íntegra; a numeração original foi preservada.

## Índice

- 26. Dashboard Design Reference Library (from Screenshots)
- 27. Layout Wireframe Patterns (from Templates)
- 28. Advanced Layout Patterns — Part 2
- 29. Rules of Engagement: Visual Technology Strategy
- Section 34: Data Storytelling & Visual Narrative (Governança BI)
- Section 33: DAX Logical Patterns for Advanced KPIS (Governança BI Layout)
- Section 32: Dynamic Titles, Textboxes (Markdowns), and Slicers (Governança BI Layout)
- 29. Modern Web Dashboard Design — Princípios e Implementação no PBIR
- Seção 41 — Constantes de Layout para LayoutValidator
- Seção 42 — Constantes de Layout: CONTRATAÇÕES - DGT
- Seção 43 — Constantes de Layout: Relatório Pagamentos + ESTRATÉGICO - PROJETOS + Elos Minuta
- Seção 49 — Análise de Qualidade: 7 Dashboards

---

## 26. Dashboard Design Reference Library (from Screenshots)

> [!TIP]
> These patterns were extracted from real dashboard designs. Use them as a reference when creating new Power BI pages.

### Design A — Purple Monochromatic (CRM/Business)

**Color Palette:**

| Role | Hex |
|------|-----|
| Background | `#F8F7FC` |
| Sidebar | `#F3F0FA` |
| Card BG | `#FFFFFF` |
| Primary/Accent | `#7C3AED` (purple) |
| Secondary | `#A78BFA` (light purple) |
| Tertiary | `#C4B5FD` (lilac) |
| Text Primary | `#1F2937` |
| Text Muted | `#6B7280` |

**Key Patterns:**
- **Monochromatic palette** — all chart colors are shades of one hue (purple)
- **Icon circles** — icons inside soft tinted circles (`background:rgba(124,58,237,0.1); border-radius:50%`)
- **Donut charts** — for categorical breakdowns (Inquiry Breakdown, Income per Quarter)
- **Stacked bar chart** — shows composition over time (Income Source per Month)
- **Date range pills** — `border:1px solid #E5E7EB; border-radius:8px; padding:6px 14px`

**New techniques:**
- Monochromatic = professional look, easy to generate (just vary lightness of one hue)
- Multiple chart types on one page: donut + bar + stacked bar + line

---

### Design B — Olive Green Financial Dashboard

**Color Palette:**

| Role | Hex |
|------|-----|
| Background | `#FAFAF5` |
| Card BG | `#FFFFFF` |
| Accent Primary | `#84A059` (olive green) |
| Accent Dark | `#3D5A1E` (dark olive) |
| Accent Light | `#C5D8A8` (light sage) |
| Text Primary | `#1A1A1A` |
| Text Muted | `#6B7280` |
| Negative | `#DC2626` |

**Key Patterns:**
- **Greeting header** — "Good Morning, [Name]!" + "Today is [DayOfWeek], [Date]" — personal touch
- **KPI strip (not cards)** — multiple KPIs in a single card separated by vertical dividers (`border-left:1px solid #E5E7EB`)
- **Three-dot menu (···)** on cards — implies interactivity (can be decorative in PBI)
- **Growth rate + arrow** — `↑22%` in green = positive, `↓5%` in red = negative
- **Merged stats in chart area** — "Highest monthly revenue: $5,800 (+18%)" inside the chart card itself
- **Donut chart with right-side legend** — legend items positioned beside the chart, not below

**New technique: KPI Strip (single card with dividers)**
```html
<div style='display:flex; gap:0;'>
  <div style='flex:1; padding:16px; border-right:1px solid #E5E7EB;'>
    <div style='font-size:12px; color:#6B7280;'>Net Profit</div>
    <div style='font-size:24px; font-weight:700; color:#3D5A1E;'>$14,840</div>
    <div style='font-size:11px; color:#84A059;'>Growth rate ↑22%</div>
  </div>
  <div style='flex:1; padding:16px;'>
    <!-- next KPI -->
  </div>
</div>
```

---

### Design C — Navy Financial KPI Dashboard

**Color Palette:**

| Role | Hex |
|------|-----|
| Header BG | `#1E2A5E` (dark navy) |
| Background | `#F5F5F0` (warm off-white) |
| Card BG | `#FFFFFF` |
| Accent | `#4A6FA5` (steel blue) |
| Chart Colors | `#7B9AC7` (light blue), `#2D4A7A` (dark blue) |
| Table Header | `#1E2A5E` |
| Table Alt Row | `#F0F4FA` |

**Key Patterns:**
- **Illustrated header** — decorative character illustrations in the title bar (unique branding)
- **Category tab labels** — colored pill labels above each chart ("Revenue Distribution" in a rounded pill)
- **Full data table** — alternating row colors below charts, with negative values in red
- **Three-chart row** — pie + line + bar side-by-side

**New technique: Data table with alternating rows (HTML)**
```html
<table style='width:100%; border-collapse:collapse; font-size:12px;'>
  <tr style='background:#1E2A5E; color:white;'>
    <th style='padding:8px; text-align:left;'>Month</th>
    <th>Revenue</th><th>Expenses</th>
  </tr>
  <tr style='background:#F0F4FA;'>
    <td style='padding:8px; font-weight:600; color:#1E2A5E;'>January</td>
    <td>$20,000</td><td>$15,000</td>
  </tr>
  <tr style='background:#FFFFFF;'>
    <td style='padding:8px; font-weight:600; color:#1E2A5E;'>February</td>
    <td>$22,000</td><td>$16,000</td>
  </tr>
</table>
```

---

### Design D — Sage Green KPI Tracker

**Color Palette:**

| Role | Hex |
|------|-----|
| Background | `#E8EDDF` (sage cream) |
| Card BG | `#F5F5EE` (warm white) |
| Card Border | `#D4D9C7` (sage border) |
| Accent Primary | `#606C38` (forest green) |
| Accent Light | `#A3B18A` (light olive) |
| Progress Bar BG | `#D4D9C7` |
| Alert Red | `#BC4749` |
| Check Green | `#606C38` |
| Text Primary | `#283618` |

**Key Patterns:**
- **Semi-circular gauges** — half-donut charts for KPIs (New Leads, SQL Rate, Demo Conv, Sales Cycle)
  - Percentage + trend arrow inside the gauge
  - Big number below the gauge arc
- **Checklist cards** — ✅ items (Weekly Target) and ❌ items (Blockers) with status icons
- **Progress bars with labels** — Team 1: 77% with label + bar + percentage
- **Period badge** — "Q1 2026" in a rounded pill at top-left
- **Horizontal bar chart** — Primary Metric comparison (Revenue, Pipeline, Win Rate, Team Quota)

**New technique: Semi-circular gauge (SVG)**
```html
<svg viewBox='0 0 120 70' style='width:100%;'>
  <!-- Background arc -->
  <path d='M 10 65 A 50 50 0 0 1 110 65' fill='none' stroke='#D4D9C7' stroke-width='10' stroke-linecap='round'/>
  <!-- Filled arc (percentage) -->
  <path d='M 10 65 A 50 50 0 0 1 85 20' fill='none' stroke='#606C38' stroke-width='10' stroke-linecap='round'/>
  <!-- Center text -->
  <text x='60' y='55' text-anchor='middle' font-size='14' font-weight='700' fill='#283618'>68%</text>
  <text x='60' y='67' text-anchor='middle' font-size='8' fill='#6B7280'>▲ 15%</text>
</svg>
```

**New technique: Progress bar with label (HTML)**
```html
<div style='display:flex; align-items:center; gap:8px; margin:4px 0;'>
  <span style='width:60px; font-size:11px; color:#283618;'>Team 1</span>
  <span style='font-size:10px; color:#606C38;'>▲</span>
  <span style='font-size:11px; color:#283618;'>77%</span>
  <div style='flex:1; background:#D4D9C7; border-radius:4px; height:8px;'>
    <div style='width:77%; height:100%; background:#606C38; border-radius:4px;'></div>
  </div>
</div>
```

---

### Design E — Navy Gantt Chart

**Color Palette:**

| Role | Hex |
|------|-----|
| Background | `#F5F0E8` (warm cream) |
| Header BG | `#1E2A5E` (dark navy) |
| Bar Color | `#2D3A6E` (navy) |
| Grid Lines | `#E0D8F0` (light lavender) |
| Grid Alt Column | `#E8E0F5` (lavender tint) |
| Text Primary | `#1E2A5E` |
| Decorative | `#4A5AA8` (medium blue) |

**Key Patterns:**
- **Gantt/Timeline layout** — tasks as horizontal bars spanning time periods
- **Grouped task categories** — bold section headers (Planning, Design, Development, Testing)
- **Alternating column shading** — light/dark purple columns for months
- **Decorative icons** — star/snowflake motifs for branding

> [!IMPORTANT]
> Gantt charts are very hard to do with standard PBI visuals. Best approach: **Deneb (Vega)** with a custom bar mark, or **HTML Content** with CSS grid/flexbox.

---

### Master Design Token Library (All Dashboards Combined)

**Reusable Color Palettes by Theme:**

| Theme | BG | Card | Accent | Dark | Light |
|-------|-----|------|--------|------|-------|
| Purple CRM | `#F8F7FC` | `#FFF` | `#7C3AED` | `#4C1D95` | `#C4B5FD` |
| Olive Finance | `#FAFAF5` | `#FFF` | `#84A059` | `#3D5A1E` | `#C5D8A8` |
| Navy Corporate | `#F5F5F0` | `#FFF` | `#4A6FA5` | `#1E2A5E` | `#7B9AC7` |
| Sage Tracker | `#E8EDDF` | `#F5F5EE` | `#606C38` | `#283618` | `#A3B18A` |
| Health Warm | `#F0F4FA` | `#FFF` | `#F4A261` | `#2D3436` | `#FFDAB9` |
| Blue Tech | `#F7F9FB` | `#FFF` | `#3B82F6` | `#1F2937` | `#93C5FD` |
| Dark SnowUI | `#0F0F1A` | `#12121F` | `#8B5CF6` | `#0A0A14` | `#6366F1` |

**New Reusable Components (from all dashboards):**

| Component | Best Tool | Complexity |
|-----------|-----------|------------|
| KPI card with icon | HTML+CSS | Low |
| KPI strip (dividers) | HTML+CSS | Low |
| Semi-circular gauge | HTML+CSS (SVG) | Medium |
| Progress bar row | HTML+CSS | Low |
| Status badge pill | HTML+CSS | Low |
| Checklist (✅/❌) | HTML+CSS | Low |
| Data table (alt rows) | HTML+CSS | Medium |
| Donut chart | Standard PBI / Deneb | Low-Medium |
| Bar/Line/Area chart | Standard PBI | Low |
| Stacked bar chart | Standard PBI | Low |
| Gantt chart | Deneb (Vega) | High |
| Greeting header | HTML+CSS (textbox) | Low |

---

## 27. Layout Wireframe Patterns (from Templates)

> [!TIP]
> These wireframes focus on **structural layout** — grid arrangements, sidebar patterns, and KPI card styling. Use these as blueprints when arranging visuals on a Power BI page.

### Layout F — Vibrant Multi-Color KPIs (Purple Sidebar)

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#C5B9F2` (lavender) |
| Content BG | `#FFFFFF` |
| Sidebar | `#6C3FC5` (deep purple) |
| KPI 1 | `#6B8CF5` (cornflower blue) |
| KPI 2 | `#9B72E8` (medium purple) |
| KPI 3 | `#F27FAE` (pink) |
| KPI 4 | `#F5B731` (golden yellow) |

**Key Patterns:**
- **Each KPI card a different vibrant color** — creates a playful, energetic feel
- **Sidebar with icon navigation** — icons only, compact width (~50px)
- **Filter icon (🔽) + collapse (≪)** in the top-right
- **Title in bold uppercase** — "REALIZADO VS. META"

---

### Layout G — Teal/Green Sidebar with Card Grid

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#D8E8E4` (mint/teal gradient background) |
| Content BG | `#F5F7F6` (off-white) |
| Sidebar | `#3BB08F` (teal green) |
| Card BG | `#FFFFFF` |
| Icon Accent | `#3BB08F` |
| Text | `#3BB08F` (sidebar), `#6B7280` (content) |

**Key Patterns:**
- **Sidebar with text labels** — icons + PAGE1/PAGE2/PAGE3 labels
- **3 KPI cards across top** — each with a small icon in the top-left corner
- **2×2 grid below** — for larger chart cards
- **Hamburger menu (≡)** in top-right
- **Generous padding** — cards have large gaps between them

**Grid Layout (PBI Position Mapping):**
```
┌─────────┬───────────┬───────────┬───────────┐
│ SIDEBAR │  KPI 1    │  KPI 2    │  KPI 3    │  y:30, h:90
│ (50px)  ├───────────┴───────────┼───────────┤
│         │  Chart 1 (wide)       │ Chart 2   │  y:140, h:160
│         ├───────────┬───────────┼───────────┤
│         │  Chart 3              │ Chart 4   │  y:320, h:200
└─────────┴───────────┴───────────┴───────────┘
```

---

### Layout H — Dark Mode with Gradient KPI Cards

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#1A1F2E` (very dark charcoal-blue) |
| Card BG | `#232A3A` (dark card) |
| Card Border | `#2E3648` (subtle dark border) |
| KPI Gradient 1 | `linear-gradient(135deg, #2563EB, #1A1F2E)` (blue fade) |
| KPI Gradient 2 | `linear-gradient(135deg, #EA580C, #1A1F2E)` (orange fade) |
| KPI Gradient 3 | `linear-gradient(135deg, #6B7280, #1A1F2E)` (silver fade) |
| Sidebar Icons | `#4B5563` (muted gray) |
| Active Icon | `#3B82F6` (bright blue) |

**Key Patterns:**
- **Gradient KPI cards** — each card has a diagonal gradient fading from a color to the background
- **3×3 equal grid** — uniform card sizes across the page
- **Collapsible sidebar** — `>>` icon to expand, icon-only when collapsed
- **Cards blend into background** — very subtle border, almost invisible separation

**CSS for gradient KPI card:**
```css
background: linear-gradient(135deg, rgba(37,99,235,0.6) 0%, rgba(37,99,235,0) 60%);
border: 1px solid rgba(255,255,255,0.05);
border-radius: 16px;
```

---

### Layout I — Deep Navy/Purple Dark Mode

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#0F1129` (deep navy) |
| Card BG | `#1A1D3A` (dark purple-navy) |
| Card Border | `#252850` (muted purple border) |
| KPI Gradient 1 | `linear-gradient(135deg, #7C3AED, #1A1D3A)` (purple fade) |
| KPI Gradient 2 | `linear-gradient(135deg, #4B5563, #1A1D3A)` (gray fade) |
| Right Panel | `#141630` (darkest navy) |
| Sidebar | `#0D0F24` (near-black) |

**Key Patterns:**
- **Tall right panel** — spans full height, darker than main content area (for filters, details, or KPI summary)
- **3 KPI cards + right panel** — top row has 3 small gradient cards + tall right panel
- **Monochromatic dark** — all purple/navy shades, no bright accent cards
- **Glass-like borders** — `rgba(255,255,255,0.03)` borders on cards

**CSS for deep navy card:**
```css
background: #1A1D3A;
border: 1px solid rgba(255,255,255,0.03);
border-radius: 16px;
box-shadow: 0 4px 24px rgba(0,0,0,0.3);
```

---

### Layout J — Two-Panel (Light + Dark Navy Sidebar)

**Color Palette:**

| Role | Hex |
|------|-----|
| Content BG | `#E8ECF5` (light lavender) |
| Card BG | `#FFFFFF` |
| Right Panel | `#1E2A5E` (dark navy) |
| KPI Gradient 1 | `linear-gradient(135deg, #7C3AED, #1A1D3A)` (purple) |
| KPI Gradient 2 | `linear-gradient(135deg, #EA580C, #1A1D3A)` (orange) |
| Sidebar | `#2D3A6E` (medium navy) |

**Key Patterns:**
- **Split layout: ~70% light / ~30% dark** — light content area with a dark navy right panel
- **KPI cards with gradient** — same gradient technique but on a light background
- **Fewer KPIs (2)** — when right panel takes significant space, reduce KPI count
- **Clean card separation** — white cards on lavender background, subtle shadows

---

### Page Layout Templates Summary

| Layout | Style | Grid | Sidebar | Right Panel | Best For |
|--------|-------|------|---------|-------------|----------|
| F | Vibrant multi-color | 4 KPI + content | Purple (icon-only) | No | Playful/KPI-heavy |
| G | Clean teal | 3 KPI + 2×2 | Teal (icon+text) | No | Standard dashboard |
| H | Dark gradient | 3×3 grid | Dark (collapsible) | No | Modern dark theme |
| I | Deep navy | 3 KPI + 2+1 | Navy (collapsible) | Yes (tall) | Executive view |
| J | Light+dark split | 2 KPI + 2+1 | Navy (collapsible) | Yes (navy) | Mixed theme |

### Collapsible Sidebar Pattern (PBI Implementation)

In Power BI, the sidebar is typically:
1. An **HTML Content visual** with icon SVGs (for the collapsed state)
2. A **bookmark** to toggle between collapsed (icon-only) and expanded (icon+text) states
3. Position: `x:0, y:0, height:720, width:50` (collapsed) or `width:160` (expanded)
4. High `z` value to layer above other visuals

---

## 28. Advanced Layout Patterns — Part 2

### Layout K — Dark Purple with Gold Accent Panel

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#2A2344` (dark purple) |
| Top Nav BG | `#1E1A38` (darker purple) |
| Card BG | `#352E50` (medium purple) |
| Card Border | `#433B60` (muted purple) |
| KPI 1 | `linear-gradient(135deg, #6B8CF5, #352E50)` (blue-purple) |
| KPI 2 | `linear-gradient(135deg, #9B72E8, #352E50)` (purple) |
| KPI 3 | `linear-gradient(135deg, #C08B8B, #352E50)` (mauve) |
| KPI 4 | `linear-gradient(135deg, #8B7660, #352E50)` (brown) |
| Accent Panel | `#D4A853` (gold/amber) |
| Nav Icons | `#6BB8C4` (teal, active) |

**Key Patterns:**
- **Top navigation bar** — horizontal bar with hamburger + centered icons (home, chart, settings)
- **KPI cards with colored circle indicators** — small colored dot on the right side of each card
- **Gold accent panel** — tall right panel in warm gold for highlighting featured content or KPIs
- **No sidebar** — navigation moved to top bar instead

**New technique: Top navigation bar (vs sidebar)**
```
┌──────────────────────────────────────────┐
│  ≡     🏠  📈  ⚙️                        │  h: 30px, dark bar
├────────┬────────┬────────┬────────┬──────┤
│ KPI 1  │ KPI 2  │ KPI 3  │ KPI 4  │      │  h: 80px
├────────┴────────┼────────┴────────┤ GOLD │
│  Chart 1        │  Chart 2        │ PANEL│  h: 200px
├────────┬────────┼────────┬────────┤      │
│ Chart 3│ Chart 4│ Chart 5│ Chart 6│      │  h: 200px
└────────┴────────┴────────┴────────┴──────┘
```

---

### Layout L — Ice Blue Minimal (5 KPIs)

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#EDF4FA` (ice blue) |
| Card BG | `#FFFFFF` |
| Card Border | `#D6E6F2` (light blue border) |
| Sidebar BG | `#EDF4FA` (matches page) |
| Icon Accent | `#5CB8C8` (teal) |
| Text | `#6B7280` |

**Key Patterns:**
- **5 KPI cards across top** — more KPIs than the typical 3-4 layout
- **Ultra-minimal styling** — barely visible borders, no shadows
- **Icon-only sidebar** with 7 icons (hamburger, home, chart, settings, globe, LinkedIn, etc.)
- **Social media icons in sidebar** — useful for linking to external profiles
- **3×3 grid for charts** — very spacious with generous gaps

---

### Layout M — People Analytics (Teal Gradient, Multi-Page)

> [!IMPORTANT]
> This is a **multi-page system** — same sidebar/branding across pages with different content. Very common in real enterprise dashboards.

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#C5DED6` (mint/sage gradient) |
| Content BG | `#FFFFFF` (white card container) |
| Header/Analysis | `#2A8C87` (teal) |
| Sidebar | `#2A8C87` → `#1F6E6A` (teal gradient) |
| Active Nav | `#FFFFFF` (white bg on active) |
| Inactive Nav | transparent |
| KPI Icon BG | `#FFE0E6` (pink), `#FFF0D4` (amber), `#E0F0FF` (blue) |
| Text Primary | `#1A3A3A` (dark teal) |
| Text Subtitle | `#2A8C87` (teal) |
| Section Title | `#1A3A3A` bold uppercase |

**Key Patterns:**
- **Two-column layout** — left column for KPI cards, right section for analysis charts
- **"ANALISAR" filter bar** — dedicated slicer/filter section with rounded container and icon
- **Category column headers** — bold uppercase labels above each chart column (POR GÊNERO, POR FAIXA ETÁRIA)
- **Character illustrations** — decorative people illustrations in sidebar/corners (branding)
- **Multi-page sidebar navigation** — "Overview" and "Frequência" with active state (white bg)
- **Colored icon circles** — each KPI has a distinct pastel circle background

**Page variants in same system:**

| Page | Title | KPI Count | Analysis Columns | Bottom Charts |
|------|-------|-----------|-----------------|---------------|
| Overview | OVERVIEW | 3 | 3 (POR, GÊNERO, FAIXA ETÁRIA) | % TURNOVER + Timeline |
| Frequência | FREQUÊNCIA | 2 | 4 (ESCOLARIDADE, GÊNERO, FAIXA ETÁRIA, ETINIA) | 2× % HORAS EXTRAS |

**New technique: Multi-page design system**
- Keep sidebar, branding, and color scheme **identical** across pages
- Change only the content area + page title
- Active page gets white background in sidebar, inactive is transparent
- Each page can have different KPI count and chart layout

**CSS for teal gradient header section:**
```css
background: linear-gradient(135deg, #2A8C87, #1F6E6A);
border-radius: 20px;
padding: 24px;
color: white;
```

**CSS for filter bar:**
```css
background: #FFFFFF;
border-radius: 30px;
padding: 8px 20px;
display: flex;
align-items: center;
gap: 8px;
box-shadow: 0 2px 8px rgba(0,0,0,0.08);
```

---

### Layout N — Contratos SETIM (Card-Shaped Filters)

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#C5DED6` (mint/sage) |
| Content BG | `#FFFFFF` |
| Header Section | `#2A8C87` (teal) |
| Sidebar | `#2A8C87` (teal, thin strip) |
| Filter Cards | `#FFFFFF` (white, stacked) |
| Filter Card Border | `#E5E7EB` (light gray) |
| Text | `#1A3A3A` (dark teal) |

**Key Patterns:**
- **Card-shaped filter buttons** — 6 white rounded cards stacked vertically in left column (acting as slicers/filters)
- **Large teal header area** — takes ~40% of top space for hero KPI or featured visual
- **"EXECUÇÃO MENSAL" section** — bottom white area with tab/button label
- **Minimal sidebar** — very thin teal strip on far left

**New technique: Stacked card filters**
```
┌────────┬──────────────────────────────┐
│ Title  │                              │
│        │     TEAL HEADER AREA         │  h: 250px
├────────┤    (hero KPI / feature)      │
│ Card 1 │                              │
├────────┼──────────────────────────────┤
│ Card 2 │                              │
├────────┤  EXECUÇÃO MENSAL             │  h: 250px
│ Card 3 │  (main content / table)      │
├────────┤                              │
│ Card 4 │                              │
├────────┤                              │
│ Card 5 │                              │
├────────┴──────────────────────────────┘
```

In PBI, each "filter card" would be a **standard slicer** or **button with bookmark** — positioned as individual visuals with uniform size and spacing.

---

### Updated Layout Templates Summary

| Layout | Style | Grid | Navigation | Accent | Best For |
|--------|-------|------|------------|--------|----------|
| K | Dark purple + gold | 4 KPI + 2×3 + gold panel | Top bar (icons) | Gold right panel | Executive dark |
| L | Ice blue minimal | 5 KPI + 3×2 | Sidebar (7 icons) | Teal icons | Clean analytics |
| M | Teal People Analytics | 3 KPI left + 3 charts right | Sidebar (pages) | Teal gradient | HR/enterprise multi-page |
| N | Teal SETIM | 6 filter cards + hero + content | Thin sidebar | Teal header | Gov/contract tracking |

### New Component Library (from this batch)

| Component | HTML/CSS Pattern | Notes |
|-----------|-----------------|-------|
| Top nav bar | `display:flex; height:30px; bg:#1E1A38` | Alternative to sidebar |
| KPI with color dot | `circle: w:16px h:16px border-radius:50%` | Status indicator on card |
| Gold/accent tall panel | Full-height colored panel on right | Feature spotlight |
| Stacked card filters | Uniform white cards, 100% width, stacked | Alternative to slicers |
| "ANALISAR" filter bar | Rounded pill container with icon | Filter/slicer grouping |
| Multi-page nav | Active=white bg, Inactive=transparent | Sidebar page switching |
| Character illustrations | Positioned at corners/sidebar | Branding/personality |

---

### Layout O — Dark Charcoal with Teal Accent + Top Nav

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#1E2530` (dark charcoal) |
| Card BG | `#283040` (slightly lighter charcoal) |
| Card Border | `#334050` (subtle border) |
| KPI Strip BG | `#283040` (same as card) |
| KPI Icons | `#5CB8C8` (teal) |
| Right Panel | `#4A8A8C` (muted teal) |
| Top Nav | `#1E2530` (matches page) |
| Social Icons | `#5CB8C8` (globe, LinkedIn) |

**Key Patterns:**
- **5 KPI icons in horizontal strip** — single row with small icon-only KPI indicators
- **Top nav with social icons on right** — globe 🌐 + LinkedIn icons at far right
- **Teal right accent panel** — tall, spans both chart rows
- **2 wide + 2 wide grid** — two chart cards per row, evenly split

---

### Layout P — Teal Sidebar with Mixed Gradient KPIs

**Color Palette:**

| Role | Hex |
|------|-----|
| Page BG | `#D8EAE5` (mint green) |
| Content BG | `#E8ECF5` (lavender) |
| Card BG | `#FFFFFF` |
| Sidebar | `#004D4D` (very dark teal) |
| Right Panel | `#004D4D` (dark teal, ~30% width) |
| KPI 1 | `linear-gradient(135deg, #006D5B, #003D3D)` (dark teal) |
| KPI 2 | `linear-gradient(135deg, #B84820, #4A1A0A)` (rust orange) |
| KPI 3 | `linear-gradient(135deg, #00897B, #004D4D)` (bright teal) |

**Key Patterns:**
- **Mixed gradient KPI colors** — teal + orange + teal creates variety without being chaotic
- **Collapsible dark sidebar** — `>>` icon to expand
- **Dark right panel** — same color as sidebar, creates visual "bookend" framing
- **Content sandwiched** — light lavender content between dark sidebar and dark right panel

**CSS for rust/orange gradient:**
```css
background: linear-gradient(135deg, #B84820 0%, #4A1A0A 100%);
border-radius: 12px;
```

---

### Layout Q — Navy Header with Lens Flare Glow

**Color Palette:**

| Role | Hex |
|------|-----|
| Header BG | `#0D1B3E` (deep navy) |
| Header Glow | `radial-gradient(ellipse at 50% 0%, rgba(100,140,255,0.15), transparent 70%)` |
| Page BG | `#E8ECF0` (light silver-blue) |
| Card BG | `#FFFFFF` |
| Card Top Accent | `#2A4080` (dark blue) |
| KPI Pill BG | `#1A2D5A` (navy) |
| Footer | `#D8DCE4` (light gray) |

**Key Patterns:**
- **No sidebar** — full-width layout, navigation in header only
- **Lens flare/glow effect** — subtle radial gradient centered at top of header creates a cinematic glow
- **KPI pills in header** — 2 small rounded KPI cards + wide stats bar within the dark header
- **3-column equal cards** — three white cards of identical size, each with a blue accent top band
- **Light gray footer strip** — subtle footer area at bottom

**CSS for lens flare glow:**
```css
background: #0D1B3E;
position: relative;
/* Pseudo-element for glow */
background-image: radial-gradient(
  ellipse at 50% 0%,
  rgba(100, 140, 255, 0.15) 0%,
  transparent 70%
);
```

**New technique: Card with colored top accent band**
```css
border-radius: 12px;
overflow: hidden;
/* Blue band at top */
border-top: 4px solid #2A4080;
/* Or use a pseudo-element for thicker band */
```

---

### Complete Layout Catalog (A-Q Summary)

| ID | Name | Theme | Navigation | Unique Feature |
|----|------|-------|------------|----------------|
| A | Purple CRM | Light mono-purple | Left sidebar | Monochromatic palette |
| B | Olive Finance | Light olive-green | None | KPI strip with dividers |
| C | Navy Financial | Light + navy header | None | Data table + alternating rows |
| D | Sage Tracker | Light sage-green | None | Semi-circular SVG gauges |
| E | Navy Gantt | Light + navy | None | Gantt timeline chart |
| F | Vibrant Multi-Color | Lavender + vibrant | Purple sidebar | Each KPI a different color |
| G | Teal Grid | Mint/teal | Teal sidebar (text) | 3 KPI + 2×2 grid |
| H | Dark Gradient | Dark charcoal | Dark collapsible | Gradient fade KPI cards |
| I | Deep Navy | Deep navy/purple | Navy collapsible | Tall right panel + glass borders |
| J | Light+Dark Split | Lavender + navy | Navy collapsible | 70/30 light-dark split |
| K | Dark Purple Gold | Dark purple | Top nav bar | Gold accent panel |
| L | Ice Blue | Ice blue minimal | 7-icon sidebar | 5 KPIs, ultra-minimal |
| M | People Analytics | Teal gradient | Multi-page sidebar | Enterprise multi-page system |
| N | SETIM Contracts | Mint + teal | Thin teal strip | Card-shaped filter buttons |
| O | Dark Charcoal Teal | Dark charcoal | Top nav + social | Teal right panel + social icons |
| P | Teal Mixed Gradients | Mint layered | Dark teal collapsible | Orange+teal gradient mix |
| Q | Navy Lens Flare | Navy + silver | Header only | Lens flare glow + 3-col cards |

---

## 29. Rules of Engagement: Visual Technology Strategy

> [!IMPORTANT]
> The golden rule for building premium Power BI dashboards: **Use each technology where it shines. Don't force one tool for everything.** 
> Use the following rubric to decide which technology to use for a given component.

### 🏢 HTML Content Visual (HTML + CSS)
**Best for:** Layout, Structure, Text, and Micro-Interaction

- ✅ **Use for**: 
  - KPI Cards (especially with gradients or complex layouts)
  - Custom Headers & Titles
  - Filter Drawers & Sidebars (paired with Bookmarks)
  - Layout Panels (e.g., placing a dark background panel behind charts)
  - Simple inline SVG graphics (like the semi-circular gauges) that can be generated with string concatenation.
- ❌ **Do NOT use for**: 
  - Interactive data charts (bar, line, scatter) — you lose cross-filtering and tooltips.
  - Complex visualizations — generating complex SVG paths purely via DAX string concatenation is unmaintainable.
- 💡 **Superpower**: Full CSS support (`@keyframes` animations, hover effects, flexbox layouts, gradients, borders, shadows).

### 📊 Standard Power BI Visuals
**Best for:** Standard Analytics & Interactive Drill-down

- ✅ **Use for**: 
  - Line Charts, Bar Charts, Column Charts, Scatter Plots, Matrices
  - Slicers (native slicers are required for cross-filtering out-of-the-box)
  - Any time the user MUST cross-filter other visuals by clicking a data point.
- ❌ **Do NOT use for**: 
  - KPI Cards (they lack CSS styling capabilities and look "boxy")
  - Highly customized aesthetic layouts.
- 💡 **Superpower**: Zero maintenance, maximum performance, native interactivity, built-in tooltips.

### 🎨 Deneb (Vega-Lite)
**Best for:** Unorthodox Data Viz & High-Density Insights

- ✅ **Use for**: 
  - Custom chart types (Sankey, Beeswarm, Joyplots, Org Trees, Gantt charts)
  - High-density visual tables (like sparklines inside tables)
  - When you need absolute pixel-perfect control over every axis, tick mark, and data label in a chart.
- ❌ **Do NOT use for**: 
  - Simple bar/line charts (use standard visuals — they load faster and handle cross-filtering easier).
  - KPI Cards (HTML is much easier to write and maintain via DAX than a JSON spec).
  - Anything that needs CSS transitions or `@keyframes` (Deneb does not support CSS).
- 💡 **Superpower**: Grammar of graphics allows building any static data visualization imaginable from scratch.

### 🚀 Deneb (Vega)
**Best for:** Animated Data Storytelling

- ✅ **Use for**: 
  - Complex animated sequences (Bar chart races, simulation particles, timer-based data progression).
- ❌ **Do NOT use for**: 
  - Anything else. Vega syntax is 3-5x more verbose and complex than Vega-Lite. Only pay this complexity cost if animation is an absolute hard requirement.
- 💡 **Superpower**: Full event streaming and timer loops natively.

### The Hybrid Dashboard Workflow

1. **Base Layer**: Standard PBI Background or simple HTML rectangular panels for structure.
2. **Navigation/Framing**: HTML Content visuals for Sidebars, Filter Drawers, and Headers with CSS hover effects.
3. **Primary KPIs**: HTML Content visual measures returning HTML strings for beautifully styled gradient cards.
4. **Primary Analysis**: Standard PBI bar/line charts placed inside transparent areas for maximum interactivity.
5. **Specialty Viz (Optional)**: 1 or 2 Deneb (Vega-Lite) charts reserved strictly for custom plots (like a Gantt or Bullet chart).
6. **Interaction**: Use PBI Bookmarks over HTML visuals to toggle states (like opening a drawer).

---

## Section 34: Data Storytelling & Visual Narrative (Governança BI)
**Origin:** Extracted from the user's "Governança BI" dashboard (`Projeto para aprendizado`) page and visual JSON topologies.

The dashboard uses a highly structured narrative to convey the overall health and maturity of an IT organization (in this case, a Tribunal). It breaks the story into 4 distinct pillars (pages), each answering a specific question about IT Governance:

### 1. The Bedrock: System Uptime (Page: PJe 1° e 2° Grau)
*   **The Question:** "Are the core machines running?"
*   **The Story:** This acts as the baseline. It uses a custom Gauge Dial (`dg5...`) and a Combo Chart (`lineClusteredColumnComboChart`) to plot the current system availability strictly against an SLA target line (90%). It relies heavily on dynamic DAX bounds (`targetstart`, `targetend`, `mediastart`) to definitively tell the user if the systems are currently healthy. 

### 2. Strategic Benchmarking (Page: iGovTIC)
*   **The Question:** "How are we doing compared to everyone else?"
*   **The Story:** The narrative shifts from raw operational metrics to strategic standing. Utilizing a Line Chart (`lineChart`) and a Combo Chart, it juxtaposes the Tribunal's own iGovTIC evaluation score (`VALOR`) against the national average of other courts (`MÉDIAS ESTADUAIS`). Reference threshold lines explicitly map the score to maturity bands—*Satisfatório (40)*, *Aprimorado (70)*, and *Excelência (90)*—while tracking the state ranking over time.

### 3. The Human Element (Page: Service Desk)
*   **The Question:** "Are our users actually happy?"
*   **The Story:** Having established that systems run and strategy is sound, the narrative focuses on the end-user. A Clustered Column Chart (`clusteredColumnChart`) displays Service Desk survey responses over time. The storytelling here leans heavily on cognitive color mapping: exact survey strings (Excelente, Muito Bom, Bom, Razoável, Ruim) are hardcoded in the visual JSON to display as a color gradient from bright green (`#00C800`) to pure red (`#FF0000`).

### 4. Efficient Execution (Page: Capacitações / Budget)
*   **The Question:** "Are we actually executing our plans?"
*   **The Story:** The final pillar evaluates internal efficiency. A Combo Chart plots planned actions (`PREVISTO`) versus what was successfully carried out (`REALIZADO`) over the years. To ensure the story is instantly understandable, dynamic labels using the DAX measure `% Executado` are placed prominently over the bars, immediately highlighting any execution gaps.---

## Section 33: DAX Logical Patterns for Advanced KPIS (Governança BI Layout)
**Origin:** Extracted from the user's "Governança BI" dashboard (`Projeto para aprendizado`) semantic model `.tmdl` files.

The user utilizes several common DAX patterns to calculate their metrics. When generating models for dashboards, these are the proven formulas to use:

### 1. Context-Clearing Percentages (ALLEXCEPT)
To calculate a percentage of a total while ignoring *some* slicers but respecting others, the user uses `ALLEXCEPT` to establish the denominator context. This is visible in the `'Percentual de Respostas'` measure:
```dax
VAR TotalGeralNoPeriodo =
    CALCULATE(
        [Total de Respostas]/100,
        ALLEXCEPT(
            '5 Satisfação Service Desk',
            '5 Satisfação Service Desk'[Data da Resposta], 
            'dCalendario'[Ano],            
            '5 Satisfação Service Desk'[Pergunta]        
        )
    )
RETURN
    IF(TotalGeralNoPeriodo = 0, BLANK(), DIVIDE(RespostasNoPeriodo, TotalGeralNoPeriodo))
```

### 2. Time-Based Availability Calculations
The dashboard calculates a "System Availability %" by dividing the summed unavailable minutes by the *total possible minutes in the filtered context*. It checks how many days are active in the `dCalendario` filter context:
```dax
VAR MinutosIndisponiveisNoContexto = [Total Minutos Indisponíveis]
VAR DiasNoContexto = COUNTROWS('dCalendario')
VAR TotalMinutosNoContexto = DiasNoContexto * 1440 -- (1440 minutes in a day)
VAR TaxaIndisponibilidade = DIVIDE( MinutosIndisponiveisNoContexto, TotalMinutosNoContexto )
```

### 3. Safe Division and Blanks
Across all metrics (like `% Execução` budget), the user employs the `DIVIDE` function with a safe alternate result (like `0` or `BLANK()`) and uses `IF(ISBLANK())` to ensure charts remain clean when data is missing, avoiding `NaN` or Infinity errors.---

## Section 32: Dynamic Titles, Textboxes (Markdowns), and Slicers (Governança BI Layout)
**Origin:** Extracted from the user's "Governança BI" dashboard (`Projeto para aprendizado`) layout.

### Dynamic DAX Titles in PBIR
To create a dynamic title that changes based on slicer selection, the user creates a DAX measure evaluating to text (e.g., `"Disponibilidade PJe do Ano " & SELECTEDVALUE('dCalendario'[Ano])`). 
In the `visual.json` file, instead of a static `Literal` string, the title property is bound to the measure using the `Measure` expression object:
```json
"visualContainerObjects": {
  "title": [
    {
      "properties": {
        "text": {
          "expr": {
            "Measure": {
              "Expression": {
                "SourceRef": { "Entity": "1 Disponibilidade de Sistemas" }
              },
              "Property": "Título Gráfico PJe"
            }
          }
        }
      }
    }
  ]
}
```

### Textboxes (Markdowns)
Standard Power BI textboxes have `visualType: "textbox"`. The text and its rich formatting are stored inside `objects.general`:
```json
"objects": {
  "general": [
    {
      "properties": {
        "paragraphs": [
          {
            "textRuns": [
              {
                "value": "Pergunta",
                "textStyle": {
                  "fontSize": "12pt",
                  "color": "#ffffff"
                }
              }
            ],
            "horizontalTextAlignment": "center"
          }
        ]
      }
    }
  ]
}
```

### Dropdown Slicer Configuration
Slicers (`visualType: "slicer"`) enforce their display mode (like Dropdown) via the `objects.data` property:
```json
"objects": {
  "data": [
    {
      "properties": {
        "mode": {
          "expr": { "Literal": { "Value": "'Dropdown'" } }
        }
      }
    }
  ]
}
```
Styling for slicer items (font size, color, background) is applied in `objects.items`, and the header in `objects.header`.

---

## 29. Modern Web Dashboard Design — Princípios e Implementação no PBIR

> [!IMPORTANT]
> Esta seção documenta os princípios de design de dashboards modernos (inspirados em shadcn/ui, Tremor, Vercel, Linear, Stripe) **e como implementar cada regra nos arquivos JSON do formato PBIP/PBIR**.
>
> Fontes: Nielsen Norman Group, Stephen Few (Information Dashboard Design), Cole Nussbaumer Knaflic (Storytelling with Data), Edward Tufte, Microsoft Learn, shadcn/ui, Tremor, Cloudscape Design System.

---

### 29.1 As 10 Regras Fundamentais de Design de Dashboard

#### Regra 1 — Hierarquia visual: posição importa
**Princípio**: O elemento mais importante deve estar no canto superior esquerdo. Usuários leem em Z (topo-esquerda → topo-direita → baixo-esquerda → baixo-direita).

**Implementação no PBIR**: Controlar a posição pelos campos `x`, `y` no `position` do `visual.json`.
```json
// KPI mais importante: canto superior esquerdo
"position": { "x": 24, "y": 96, "width": 292, "height": 100 }

// Gráficos de tendência: meio da página
"position": { "x": 24, "y": 212, "width": 860, "height": 340 }

// Tabela de detalhes: parte inferior
"position": { "x": 24, "y": 568, "width": 1232, "height": 128 }
```

**Ordem recomendada para licitações (1280×720):**
```
y:  0–80  → Cabeçalho / título / slicers
y: 80–200 → KPI cards (4–5 métricas principais)
y:200–560 → Gráficos principais (linha, barras, scatter)
y:560–720 → Tabela de detalhe
```

---

#### Regra 2 — Máximo de visuais por página
**Princípio**: Microsoft recomenda **máximo 8–10 visuais** por página. Mais que isso reduz o tamanho de cada visual, comprometendo a legibilidade.

**Verificação**: Contar `visual.json` na pasta `visuals/` de cada página:
```bash
ls pages/00_visao_geral/visuals/ | wc -l
```

**O que NÃO conta como "visual" para o limite:**
- Textboxes de título/subtítulo
- Shapes decorativas
- Slicers de filtro (são controles, não visualizações)

---

#### Regra 3 — Paleta semântica: máximo 5–6 cores com significado
**Princípio**: Cores sem significado são ruído. O cérebro humano distingue com clareza no máximo 7 categorias visuais distintas (Miller's Law). Cada cor deve ter um papel fixo e consistente.

**Paleta semântica recomendada para o projeto (shadcn/Tailwind):**

| Papel | Cor | Hex | Uso |
|-------|-----|-----|-----|
| Principal | Blue | `#3B82F6` | Barras primárias, linhas de tendência |
| Positivo | Emerald | `#10B981` | Crescimento YoY, metas atingidas |
| Negativo | Rose | `#F43F5E` | Queda YoY, alertas |
| Atenção | Amber | `#F59E0B` | Aviso, variação neutra |
| Secundário | Indigo | `#6366F1` | Segunda série, linha de comparação |
| Neutro | Zinc | `#71717A` | Labels secundários, eixos |

**Implementação no PBIR — colorir série de um gráfico:**
```json
// Em visual.json → objects → dataPoint
"dataPoint": [
  {
    "properties": {
      "fill": {
        "solid": {
          "color": { "expr": { "Literal": { "Value": "'#3B82F6'" } } }
        }
      }
    }
  }
]
```

**Colorir uma categoria específica (ex: linha negativa em vermelho):**
```json
"dataPoint": [
  {
    "properties": {
      "fill": {
        "solid": {
          "color": { "expr": { "Literal": { "Value": "'#F43F5E'" } } }
        }
      }
    },
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
            "Right": { "Literal": { "Value": "'ValorParaColorir'" } }
          }
        }
      }]
    }
  }
]
```

---

#### Regra 4 — Anatomia do KPI card moderno (padrão shadcn/Tremor)
**Princípio**: Todo KPI card deve responder: "O que estou vendo? É bom ou ruim? Está melhorando ou piorando?"

**5 elementos obrigatórios:**
1. **Label** — o que está sendo medido (12px, gray-500, uppercase ou regular)
2. **Valor principal** — o número em destaque (32–40px, bold)
3. **Delta vs período anterior** — `+12,3%` com seta ↑↓ e cor semântica (verde/vermelho)
4. **Período de referência** — "Jan–Dez 2024" (10px, muted)
5. **Contexto** — meta, benchmark, ou comparação

**Implementação via card nativo PBI** (limitações: sem delta inline, sem sparkline):
```json
// visual.json para card simples
{
  "visualType": "card",
  "query": {
    "queryState": {
      "Values": {
        "projections": [{
          "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Medidas" } }, "Property": "Valor Total" } },
          "queryRef": "_Medidas.Valor Total"
        }]
      }
    }
  },
  "objects": {
    "labels": [{
      "properties": {
        "fontSize": { "expr": { "Literal": { "Value": "36D" } } },
        "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#09090B'" } } } } }
      }
    }],
    "categoryLabels": [{
      "properties": {
        "fontSize": { "expr": { "Literal": { "Value": "11D" } } },
        "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#71717A'" } } } } }
      }
    }]
  }
}
```

**Implementação via HTML Content visual** (completo — delta + ícone + sparkline):
```dax
measure KpiCardCompleto =
    VAR _valor = [Valor Total]
    VAR _anterior = [Valor Ano Anterior]
    VAR _delta = DIVIDE(_valor - _anterior, _anterior, 0)
    VAR _cor = IF(_delta >= 0, "#10B981", "#F43F5E")
    VAR _seta = IF(_delta >= 0, "↑", "↓")
    RETURN
    "<div style='font-family:Inter,Segoe UI,sans-serif; background:#FFFFFF; border:1px solid #E4E4E7; border-radius:12px; padding:min(20px,3vw); width:100%; height:100vh; box-sizing:border-box; display:flex; flex-direction:column; justify-content:space-between;'>" &
    "<span style='font-size:clamp(10px,2vw,12px); color:#71717A; text-transform:uppercase; letter-spacing:0.05em;'>Valor Total</span>" &
    "<div style='font-size:clamp(24px,5vw,36px); font-weight:700; color:#09090B; line-height:1;'>" & FORMAT(_valor, "R$ #,##0.0,,\" Bi\"") & "</div>" &
    "<div style='display:flex; align-items:center; gap:6px;'>" &
    "<span style='font-size:clamp(10px,2vw,13px); font-weight:600; color:" & _cor & ";'>" & _seta & " " & FORMAT(ABS(_delta), "0,0%") & "</span>" &
    "<span style='font-size:clamp(9px,1.5vw,11px); color:#71717A;'>vs ano anterior</span>" &
    "</div>" &
    "</div>"
```

---

#### Regra 5 — Typography hierarchy: 3 níveis distintos
**Princípio**: A diferença de tamanho entre níveis deve ser percebível (mínimo 4pt de diferença). Não usar mais de 2 pesos (regular + bold).

| Nível | Uso | Tamanho | Peso | Cor |
|-------|-----|---------|------|-----|
| Metric | Valor do KPI | 32–40pt | 700 | `#09090B` |
| Title | Título do visual | 13–14pt | 600 | `#09090B` |
| Label | Labels secundários, eixos | 10–11pt | 400 | `#71717A` |

**Implementação no PBIR — título do visual:**
```json
"visualContainerObjects": {
  "title": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "text": { "expr": { "Literal": { "Value": "'Título do visual'" } } },
      "fontSize": { "expr": { "Literal": { "Value": "13D" } } },
      "fontColor": { "solid": { "color": { "expr": { "Literal": { "Value": "'#09090B'" } } } } },
      "alignment": { "expr": { "Literal": { "Value": "'left'" } } }
    }
  }]
}
```

**Implementação no PBIR — label do eixo (categoryAxis):**
```json
"categoryAxis": [{
  "properties": {
    "fontSize": { "expr": { "Literal": { "Value": "10D" } } },
    "labelColor": {
      "solid": {
        "color": { "expr": { "Literal": { "Value": "'#71717A'" } } }
      }
    }
  }
}]
```

---

#### Regra 6 — Card container styling (borda, sombra, background)
**Princípio** (shadcn/Tailwind): Cards modernos usam borda sutil `1px solid` + `border-radius 8–12px` + background branco sobre fundo levemente cinza. Sombra só em hover, nunca permanente.

**Implementação no PBIR — container do visual:**
```json
"visualContainerObjects": {
  "background": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "color": {
        "solid": {
          "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } }
        }
      },
      "transparency": { "expr": { "Literal": { "Value": "0D" } } }
    }
  }],
  "border": [{
    "properties": {
      "show": { "expr": { "Literal": { "Value": "true" } } },
      "color": {
        "solid": {
          "color": { "expr": { "Literal": { "Value": "'#E4E4E7'" } } }
        }
      },
      "radius": { "expr": { "Literal": { "Value": "12D" } } }
    }
  }],
  "title": [{ "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } }]
}
```

**Página com fundo levemente cinza (padrão shadcn):**
```json
// Em page.json → objects → background
"background": [{
  "properties": {
    "color": {
      "solid": {
        "color": { "expr": { "Literal": { "Value": "'#FAFAFA'" } } }
      }
    }
  }
}]
```

---

#### Regra 7 — Data-ink ratio: remover elementos não-informativos
**Princípio** (Tufte): Maximize a proporção de pixels que comunicam dados. Remova grade desnecessária, bordas decorativas, títulos de eixo óbvios, legendas redundantes.

**O que remover e como no PBIR:**

```json
// Remover gridlines do eixo Y (values)
"valueAxis": [{
  "properties": {
    "gridlineShow": { "expr": { "Literal": { "Value": "false" } } }
  }
}]

// Remover título de eixo desnecessário
"categoryAxis": [{
  "properties": {
    "showAxisTitle": { "expr": { "Literal": { "Value": "false" } } }
  }
}]

// Remover legenda quando série única
"legend": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "false" } } }
  }
}]

// Ocultar ícones do header (hover buttons)
"visualHeader": [{
  "properties": {
    "show": { "expr": { "Literal": { "Value": "false" } } }
  }
}]
```

---

#### Regra 8 — Seleção de gráfico certa para cada pergunta
**Princípio** (Few / Knaflic): Cada tipo de pergunta tem um gráfico ideal.

| Pergunta analítica | Gráfico ideal | visualType no PBIR |
|---|---|---|
| Comparação entre categorias | Barras horizontais | `clusteredBarChart` |
| Evolução ao longo do tempo | Linha | `lineChart` |
| Proporção do total | Barras empilhadas 100% | `hundredPercentStackedColumnChart` |
| Distribuição (parte do todo) | Treemap | `treemap` |
| Correlação entre 2 variáveis | Scatter | `scatterChart` |
| Top N + concentração acumulada | Combo barras + linha | `lineClusteredColumnComboChart` |
| KPI único | Card | `card` ou `cardVisual` |
| Detalhe tabular | Tabela | `tableEx` |

> [!WARNING]
> **Evitar**: Pie charts com mais de 5 categorias, gráficos 3D, gauges decorativos (círculos com ponteiro). O PBI tem estes visuals mas eles violam princípios perceptuais básicos.

---

#### Regra 9 — Ordenação intencional dos dados
**Princípio**: Dados devem ser ordenados pelo valor (decrescente para rankings, crescente para tempo). Ordem alfabética só faz sentido em lookup tables.

**Impacto no PBIR**: A ordenação padrão não pode ser definida no JSON — precisa ser feita no Desktop. Porém, a estrutura da query influencia:

```json
// Para garantir que um eixo temporal use a ordem correta,
// mapear a coluna de data e não o texto formatado
// ❌ Errado — texto "Jan/2024" ordena alfabeticamente
"field": { "Column": { "Expression": { "SourceRef": { "Entity": "Calendario" } }, "Property": "MesAno" } }

// ✅ Certo — usar MesAnoNumero no eixo e MesAno como label
// (configurar sortByColumn no TMDL: MesAno → sortByColumn: MesAnoNumero)
```

---

#### Regra 10 — Slicers: controles, não decoração
**Princípio**: Slicers devem estar visivelmente separados dos dados (zona de controle no topo ou lateral). Usar estilo "Tile" para opções discretas (ano, trimestre). Usar "Dropdown" para listas longas.

**Tile slicer (botões) — objetos necessários:**
```json
"objects": {
  "data": [{
    "properties": {
      "mode": { "expr": { "Literal": { "Value": "'Tile'" } } }
    }
  }],
  "general": [{
    "properties": {
      "orientation": { "expr": { "Literal": { "Value": "1D" } } }
    }
  }],
  "items": [{
    "properties": {
      "fontSize": { "expr": { "Literal": { "Value": "12D" } } },
      "fontColor": {
        "solid": { "color": { "expr": { "Literal": { "Value": "'#09090B'" } } } }
      },
      "background": {
        "solid": { "color": { "expr": { "Literal": { "Value": "'#F4F4F5'" } } } }
      }
    }
  }]
}
```

**Sync entre páginas (sempre usar para filtros globais):**
```json
"syncGroup": {
  "groupName": "slicerAno",
  "fieldChanges": true,
  "filterChanges": true
}
```

---

### 29.2 Padrões de Layout Moderno — Grid 8px

**Princípio**: Design systems modernos (Tailwind, shadcn) usam grid de **8px** como unidade base. Todos os valores de position, padding e gap devem ser múltiplos de 8.

**Mapeamento para PBIR (página 1280×720):**

| Elemento | x | y | width | height | Notas |
|---|---|---|---|---|---|
| Margem lateral | 24 | — | — | — | 3 × 8px |
| Header / título | 24 | 16 | 960 | 56 | |
| Slicers (área) | 24 | 16 | 1232 | 56 | |
| KPI cards (5) | 24 + (i×248) | 88 | 240 | 96 | gap 8px |
| KPI cards (4) | 24 + (i×312) | 88 | 304 | 96 | gap 8px |
| Gráfico principal | 24 | 200 | 860 | 344 | |
| Gráfico lateral | 900 | 200 | 356 | 344 | |
| Tabela inferior | 24 | 560 | 1232 | 144 | |
| Gap entre cards | 8 | — | — | — | 1 × 8px |
| Gap entre seções | 16 | — | — | — | 2 × 8px |

---

### 29.3 Diagnóstico do Dashboard Atual — Violações e Correções

Análise baseada nas screenshots do Databrick Gov dashboard em comparação com as regras acima:

| # | Violação | Regra | Impacto | Correção no PBIR |
|---|---|---|---|---|
| 1 | Pareto com eixo X em ordem alfabética | Regra 9 (ordenação) | Alto | Filtro Top N + ordenar por Valor Total no Desktop |
| 2 | Linha do pareto constante (~96%) | Regra 4 (KPI correto) | Alto | Criar medida `% Pareto Acumulado` (DAX cumulativo) |
| 3 | Scatter com ponto único (sem Top N) | Regra 2 (visuals úteis) | Alto | Filtro Top N = 50 no Desktop |
| 4 | Tabela Top 20 sem dados (sem Top N) | Regra 2 (visuals úteis) | Alto | Filtro Top N = 20 no Desktop |
| 5 | Treemap com 25 cores distintas | Regra 3 (paleta max 7) | Médio | Agrupar categorias menores em "Outros" |
| 6 | Slicer de Ano em modo lista (legenda confusa) | Regra 10 (slicer Tile) | Médio | Mudar para modo Tile no Desktop ou via JSON |
| 7 | KPI cards sem delta vs período anterior | Regra 4 (anatomia KPI) | Médio | Adicionar medidas delta e usar HTML card |
| 8 | Cards sem borda/radius (visual antigo) | Regra 6 (card styling) | Baixo | Adicionar border + radius no visualContainerObjects |
| 9 | Títulos de eixo redundantes | Regra 7 (data-ink ratio) | Baixo | `showAxisTitle: false` nos objetos do gráfico |

---

### 29.4 Template: Visual Moderno Completo (KPI + Borda + Sem Título de Eixo)

Exemplo de `visual.json` seguindo todas as regras modernas para um card de KPI:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.6.0/schema.json",
  "name": "kpi_valor_total_moderno",
  "position": { "x": 24, "y": 88, "z": 4000, "height": 96, "width": 240, "tabOrder": 4000 },
  "visual": {
    "visualType": "card",
    "query": {
      "queryState": {
        "Values": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": { "SourceRef": { "Entity": "_Medidas" } },
                "Property": "Valor Total Formatado"
              }
            },
            "queryRef": "_Medidas.Valor Total Formatado",
            "nativeQueryRef": "Valor Total Formatado"
          }]
        }
      }
    },
    "objects": {
      "labels": [{
        "properties": {
          "fontSize": { "expr": { "Literal": { "Value": "28D" } } },
          "color": {
            "solid": { "color": { "expr": { "Literal": { "Value": "'#09090B'" } } } }
          }
        }
      }],
      "categoryLabels": [{
        "properties": {
          "show": { "expr": { "Literal": { "Value": "true" } } },
          "fontSize": { "expr": { "Literal": { "Value": "11D" } } },
          "color": {
            "solid": { "color": { "expr": { "Literal": { "Value": "'#71717A'" } } } }
          }
        }
      }]
    },
    "visualContainerObjects": {
      "background": [{
        "properties": {
          "show": { "expr": { "Literal": { "Value": "true" } } },
          "color": {
            "solid": { "color": { "expr": { "Literal": { "Value": "'#FFFFFF'" } } } }
          },
          "transparency": { "expr": { "Literal": { "Value": "0D" } } }
        }
      }],
      "border": [{
        "properties": {
          "show": { "expr": { "Literal": { "Value": "true" } } },
          "color": {
            "solid": { "color": { "expr": { "Literal": { "Value": "'#E4E4E7'" } } } }
          },
          "radius": { "expr": { "Literal": { "Value": "12D" } } }
        }
      }],
      "title": [{
        "properties": {
          "show": { "expr": { "Literal": { "Value": "true" } } },
          "text": { "expr": { "Literal": { "Value": "'Valor Total'" } } },
          "fontSize": { "expr": { "Literal": { "Value": "11D" } } },
          "fontColor": {
            "solid": { "color": { "expr": { "Literal": { "Value": "'#71717A'" } } } }
          },
          "alignment": { "expr": { "Literal": { "Value": "'left'" } } }
        }
      }]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

### 29.5 Medida DAX — % Pareto Acumulado (correto)

A medida de concentração usada no `combo_pareto` deve ser **cumulativa por posição** no ranking, não um percentual fixo:

```dax
% Pareto Acumulado =
VAR ValorAtual = [Valor Total]
VAR TotalGeral = CALCULATE([Valor Total], ALL(licitacoes_2019_2024[nome]))
VAR FornecedoresComMaiorValor =
    FILTER(
        ALL(licitacoes_2019_2024[nome]),
        CALCULATE([Valor Total], ALL(licitacoes_2019_2024[nome])) >= ValorAtual
    )
VAR ValorAcumulado =
    CALCULATE([Valor Total], FornecedoresComMaiorValor)
RETURN
    DIVIDE(ValorAcumulado, TotalGeral)
```

Adicionar esta medida ao `_Medidas.tmdl` e trocar o binding do `Y2` no `combo_pareto/visual.json`:
```json
// Substituir em combo_pareto → Y2 projections
{
  "field": {
    "Measure": {
      "Expression": { "SourceRef": { "Entity": "_Medidas" } },
      "Property": "% Pareto Acumulado"
    }
  },
  "queryRef": "_Medidas.% Pareto Acumulado",
  "nativeQueryRef": "% Pareto Acumulado"
}
```

---

### 29.6 Checklist de Design Moderno — PBIR

Usar antes de finalizar qualquer página:

**Layout e hierarquia:**
- [ ] Elemento mais importante está no canto superior esquerdo (menor x, menor y)
- [ ] Máximo de 8 visuais informativos por página (não contar slicers e textboxes)
- [ ] Posições são múltiplos de 8px
- [ ] Seções visualmente separadas (grupo KPIs / grupo gráficos / grupo tabelas)

**Cores e tipografia:**
- [ ] Paleta usa no máximo 5–6 cores com papéis definidos
- [ ] Positivo = emerald `#10B981`, negativo = rose `#F43F5E`, principal = blue `#3B82F6`
- [ ] Título do visual: 13pt, `#09090B`, left-aligned
- [ ] Labels secundários: 10–11pt, `#71717A`
- [ ] Valor do KPI: mínimo 28pt, bold, `#09090B`

**Cards:**
- [ ] Background branco `#FFFFFF` com borda `#E4E4E7` e border-radius 12px
- [ ] Fundo da página em `#FAFAFA` (contraste sutil com os cards)
- [ ] KPI cards incluem label + valor + referência de período

**Gráficos:**
- [ ] Gridlines desnecessárias removidas (`gridlineShow: false`)
- [ ] Títulos de eixo removidos quando óbvios (`showAxisTitle: false`)
- [ ] Legendas removidas em séries únicas
- [ ] Ordenação por valor (não alfabética) — configurar no Desktop

**Dados:**
- [ ] Pareto ordena por valor decrescente (Top N aplicado)
- [ ] Linha do pareto usa medida cumulativa (não percentual fixo)
- [ ] Scatter usa Top N para evitar ponto único
- [ ] Tabelas têm Top N para focar no relevante

---

## Seção 41 — Constantes de Layout para LayoutValidator

> Extraídas empiricamente do dashboard Databrick Gov (finalizado, 3 páginas, 49 visuais).
> Base para o modelo matemático de predição de truncamento no DashForge AI.
> Data de coleta: 2026-04-23

### 41.1 Canvas (padrão observado)

```
Largura:  1280px
Altura:    720px
DisplayOption: FitToPage
Background: #FAFAFA
```

### 41.2 Escala de fontes canônica

| Papel no layout     | Tamanho | Unidade | Visual type   |
|---------------------|---------|---------|---------------|
| Título da página    | 20      | pt      | textbox       |
| Subtítulo da página | 11      | pt      | textbox       |
| Label gaveta filtro | 14      | pt      | textbox       |
| Título do visual    | 13      | D (pt)  | containerObj  |
| Subtítulo do visual | 9       | D (pt)  | containerObj  |
| Título do slicer    | 10      | D (pt)  | slicer        |
| Item do slicer      | 8       | D (pt)  | slicer        |
| Título do card (KPI)| 11      | D (pt)  | card          |
| Valor do card (KPI) | 28      | D (pt)  | card          |
| Header de tabela    | 10      | D (pt)  | tableEx       |
| Valores de tabela   | 10 ou 9 | D (pt)  | tableEx       |

### 41.3 Textbox — altura de linha

Fórmula validada com 3 casos reais:

```
line_height_px = n_lines × (font_pt × 2.2 + 4)
```

| Texto                        | font_pt | Altura real (px) | Fórmula → resultado |
|------------------------------|---------|-----------------|---------------------|
| Título página (1 linha, 20pt)| 20      | 47.88           | 1 × (20×2.2+4) = 48 |
| Subtítulo página (1 linha, 11pt)| 11   | 32.81 / 30.15   | 1 × (11×2.2+4) = 28.2 → ~30 |
| Label "FILTROS" (1 linha, 14pt)| 14    | 40.58           | 1 × (14×2.2+4) = 34.8 → ~38 |

> Precisão: ±3px. Suficiente para detectar overflow; não usar para pixel-perfect.

### 41.4 Card (KPI) — decomposição de altura

```
card_height = title_area + value_area + padding_vertical
  title_area      ≈ 28px  (para font 11pt)
  value_area      ≈ font_pt × 1.6px  (para 28pt → ~45px)
  padding_vertical ≈ 17–26px

Observado:
  90.46px = 28 + 45 + ~17   (página 0)
  99.31px = 28 + 45 + ~26   (página 2)
```

Larguras observadas: ~291–292px para 4 KPIs lado a lado em canvas 1280px.

Para predizer se o valor vai truncar no card:
```python
def card_value_fits(card_width, value_str, font_pt=28):
    avg_char_width_px = font_pt * 0.55  # Segoe UI, proporcional
    needed = len(value_str) * avg_char_width_px
    available = card_width - 24  # padding horizontal total estimado
    return needed <= available
```

### 41.5 TableEx — constantes de paginação

Validado com cross-check nos 3 casos reais (ver cálculo abaixo):

```
header_height    ≈ 43px         (linha de header, independente da fonte)
row_height_10pt  ≈ 24px         → 10 × 2.2 + 2 = 24
row_height_9pt   ≈ 22px         → 9 × 2.2 + 2 = 21.8 ≈ 22
row_height_fórmula: row_h = font_pt × 2.2 + 2
column_overhead  ≈ 30px         (bordas + área de scroll horizontal)
```

**Validação cruzada:**

| Tabela              | Altura total | Font | Header | Fórmula rows                    | Resultado |
|---------------------|-------------|------|--------|---------------------------------|-----------|
| tbl_top10_forn      | 186.21px    | 10pt | 43px   | (186.21-43)/24 = 5.97          | ~6 linhas |
| tbl_cat_detalhe     | 237.64px    | 10pt | 43px   | (237.64-43)/24 = 8.10          | ~8 linhas |
| tbl_top20_forn      | 483.25px    | 9pt  | 43px   | (483.25-43)/22 = **20.01**     | ~20 linhas ✓ perfeito |

Fórmula para predição de linhas visíveis:
```python
def table_rows_visible(height, font_pt=10):
    header = 43
    row_h = font_pt * 2.2 + 2
    return int((height - header) / row_h)

def table_cols_overflow(col_widths, visual_width):
    overhead = 30
    return sum(col_widths) > (visual_width - overhead)
```

### 41.6 Slicer dropdown — dimensões padrão

Consistente nas 6 instâncias (2 slicers × 3 páginas):

```
width:  247.55px
height:  90.76px
font título: 10pt
font items:   8pt
border radius: 8px
border color: #E4E4E7
```

### 41.7 Gaveta de filtros (VisualGroup outspacePane)

```
width:  ~285px  (284.55–284.88)
height: ~273px  (272.62–273.09)
posição X: ~976px  (canvas 1280px → fica quase no limite direito)
posição Y:  ~16–26px
border radius: 30px (shape interno)
default: isHidden = true
```

### 41.8 Botões de navegação (imagem com PageNavigation)

```
width:  40px
height: 40px
posição Y: ~26px (alinhado ao topo da página)
posição X arrow-right: ~1216px (quase na borda direita)
posição X arrow-left:  ~1100–1152px (à esquerda do arrow-right)
posição X filtro (funnel): entre arrow-left e arrow-right
```

### 41.9 Container visual padrão (background + border)

Padrão observado em todos os visuais de dados (cards, gráficos, tabelas):

```json
"background": { "show": true, "color": "#FFFFFF", "transparency": 0 },
"border":     { "show": true, "color": "#E4E4E7", "radius": 12 }
```

Gaveta de filtros usa `"radius": 30` no shape subjacente.

### 41.10 Margens de posicionamento dos visuais

Observado consistentemente entre os visuais principais e as bordas do canvas:

```
margin_left:   ~24px  (X inicial dos visuais de conteúdo)
margin_top:    ~96px  (Y inicial abaixo do header: títulos ~16-87px + cards)
gap_entre_visuais: ~0px (visuais tocam uns nos outros, sem gap visível)
```

*Seção 41 adicionada em 2026-04-23 — constantes extraídas do Databrick Gov, base para LayoutValidator do DashForge AI*

---

## Seção 42 — Constantes de Layout: CONTRATAÇÕES - DGT

> Segundo dashboard analisado. Canvas diferente, visual types novos, escala de fontes maior.
> Data de coleta: 2026-04-23

### 42.1 Canvas — segundo padrão observado

```
Página 1 e 3: 1920 × 1080px  (Full HD — alternativa comum ao 1280×720)
Página 2:     1920 × 1280px  (Full HD vertical expandido)
```

O LayoutValidator precisa parametrizar o canvas; não assumir 1280×720 como único padrão.

### 42.2 Fontes não escalam automaticamente com o canvas

O designer escolhe fontes maiores manualmente em canvases maiores. Comparativo:

| Papel                  | 1280×720 (Databrick Gov) | 1920×1080 (DGT) | Fator |
|------------------------|--------------------------|-----------------|-------|
| Valor do card KPI      | 28pt                     | 30–35pt         | ~1.2× |
| Título do card KPI     | 11pt                     | 22–25pt         | ~2.1× |
| Header de tabela       | 10pt                     | 15pt            | 1.5×  |
| Valores de tabela      | 9–10pt                   | 13pt            | 1.4×  |
| Título do slicer       | 10pt                     | 20pt            | 2.0×  |
| Item do slicer         | 8pt                      | 18pt            | 2.25× |
| Label em gráfico       | n/d                      | 12–22pt         | —     |
| Legenda                | n/d                      | 18–26pt         | —     |

**Implicação para o DashForge AI:** o RequirementsAgent precisa saber o canvas alvo antes de decidir as fontes. Não existe "fonte padrão universal" — depende do canvas.

Regra heurística observada: `font_pt_sugerido ≈ font_pt_base_1280 × (canvas_width / 1280) × 0.85`

### 42.3 Card KPI — dimensões no canvas 1920×1080

```
width:  370–421px   (vs 292px no canvas 1280)
height: 122–158px   (vs 90–99px no canvas 1280)
value font:  30–35pt (título + valor maior = card mais alto)
title font:  22–25pt
```

Validação da fórmula com card de 125.78px (title 25pt, value 35pt):
```
title_area  ≈ 25 × 2.2 + 4 = 59px
value_area  ≈ 35 × 1.6     = 56px
padding     ≈ 10px
total       = 125px ≈ 125.78 ✓
```
A fórmula da Seção 41.4 se mantém válida com fontes maiores.

### 42.4 TableEx — header height varia com a fonte

Tabela observada: 1906px × 348.31px, 14 colunas, header font 15pt, values font 13pt.

```
row_h (13pt) = 13 × 2.2 + 2 = 30.6px
header_h (15pt font) ≈ 15 × 2.8 + 2 = 44px
rows_visible = (348.31 - 44) / 30.6 = 9.94 ≈ 10 linhas ✓
```

Revisão da fórmula de header_height (era fixo em 43px):
```
header_h = max(43, font_pt_header × 2.8 + 2)
```
Para 10pt: max(43, 30) = 43px  → igual ao anterior ✓
Para 15pt: max(43, 44) = 44px  → levemente maior ✓

### 42.5 Novos visual types identificados

#### clusteredColumnChart (barras verticais)
```
Dimensões observadas:
  1538.38 × 512.79px  (página 1, 1920 canvas)
  1467.60 × 313.88px  (página 2, 1920 canvas)

Legenda: pode ser Left (consome largura, não altura)
Labels: show=true, fontSize 12–22pt
categoryAxis: fontSize 15–18pt
valueAxis: pode ser show=false (sem eixo Y visível)
```

Diferença crítica de orientação vs clusteredBarChart:
- `clusteredBarChart`: categorias no eixo Y (horizontal) → rótulos à esquerda consomem **largura**
- `clusteredColumnChart`: categorias no eixo X (vertical) → rótulos embaixo podem **rotar** quando há muitas categorias

#### stackedAreaChart
```
Dimensões observadas: 1472 × 361.95px
Legenda: Left
Labels: show=true, fontSize 22pt
categoryAxis: fontSize 16pt, axisType=Categorical
```

#### pageNavigator
```
Dimensões observadas: 808.74 × 59.38px
Button fontSize: 18pt (default), 15pt (selected)
Shape: rectangleRounded, roundEdge=5
```
Não contribui para truncamento de dados — decorativo.

### 42.6 Legenda na posição Left

Quando `legend.position = Left`, a legenda consome **largura** do gráfico, não altura.
Estimativa de largura reservada: `max_series_label_length × avg_char_width + ícone (~20px)`

Para detectar overflow de legenda lateral:
```python
def legend_left_width(series_labels, font_pt=18):
    avg_char_w = font_pt * 0.55
    longest = max(len(s) for s in series_labels)
    return longest * avg_char_w + 20  # 20px para o ícone de cor

def chart_area_width(visual_width, legend_labels, font_pt=18, position='Left'):
    if position in ('Left', 'Right'):
        return visual_width - legend_left_width(legend_labels, font_pt) - 16
    return visual_width  # Top/Bottom não consome largura
```

### 42.7 Shapes maiores que o canvas

O background shape tinha `width=2597.99, height=2876.35` — bem maior que o canvas 1920×1080. O Power BI clipa automaticamente. Não gera erro nem afeta outros visuais.

### 42.8 Slicer — dimensões no canvas 1920

```
Largura: 262–554px (mais variação que no canvas 1280)
Altura:   74–102px
Title fontSize: 20pt
Items fontSize: 18pt
```

*Seção 42 adicionada em 2026-04-23 — extraída do dashboard CONTRATAÇÕES - DGT (3 páginas, canvas 1920×1080/1280)*

---

## Seção 43 — Constantes de Layout: Relatório Pagamentos + ESTRATÉGICO - PROJETOS + Elos Minuta

> Três dashboards reais analisados em paralelo. Foco em: novos canvas sizes, novos visual types, distinção card vs cardVisual.
> Data de coleta: 2026-04-23

### 43.1 Catálogo completo de canvas sizes observados

| Dimensão          | Dashboard de origem               | Uso típico                     |
|-------------------|-----------------------------------|--------------------------------|
| 1280 × 720        | Databrick Gov, Rel. Pagamentos    | Web / apresentação padrão      |
| 1800 × 900        | Elos Minuta (páginas ativas)      | Monitor widescreen             |
| 1920 × 1080       | CONTRATAÇÕES - DGT                | Full HD                        |
| 1920 × 1280       | DGT página 2                      | Full HD vertical expandido     |
| 2200 × 1200       | ESTRATÉGICO - PROJETOS            | Ultra-wide corporativo         |
| 1400 × 1050       | ESTRATÉGICO página 2              | 4:3 expandido                  |
| 320 × 240         | Elos Minuta (tooltip)             | Página de tooltip              |

**Tooltip page**: `DisplayOption: Tooltip` + dimensões 320×240 + `HiddenInViewMode: true`. O Power BI renderiza essa página como popup ao passar o cursor sobre um visual. O LayoutValidator deve reconhecer e ignorar para cálculos de layout normais.

### 43.2 card (clássico) vs cardVisual (moderno) — distinção crítica

São dois visual types distintos com comportamentos e propriedades diferentes:

| Propriedade           | `card` (clássico)         | `cardVisual` (moderno)              |
|-----------------------|---------------------------|-------------------------------------|
| Visual type no JSON   | `"card"`                  | `"cardVisual"`                      |
| Suporte multi-métrica | Não (1 por visual)        | Sim (N colunas em 1 visual)         |
| Layout interno        | Simples: título + valor   | Tiles: cada métrica é um "tile"     |
| accentBar             | Não                       | Sim (barra colorida lateral)        |
| Dimensões típicas     | ~290×90px (1280 canvas)   | Muito variável — de 240×64 a 1704×168 |
| Propriedade de valor  | `labels.fontSize`         | `value.fontSize` / `calloutValue`   |

**cardVisual multi-coluna** (Elos Minuta — 5 métricas):
```
Dimensões: 1704.91 × 168.45px  (canvas 1800)
Colunas:   5 tiles lado a lado
value font: 22D  |  label font: 16D
Largura por tile: 1704.91 / 5 ≈ 341px
```

**cardVisual compacto** (Relatório Pagamentos — 1 métrica):
```
Dimensões: 240 × 64px  (canvas 1280)
value font: 28D
```

**cardVisual detalhe** (ESTRATÉGICO — modo painel):
```
Dimensões: 330 × 238px  |  329 × 252px
value font: 10D  |  label font: 14D
Suporte a accentBar lateral
```

### 43.3 Novos visual types — catálogo completo

| Visual type | Dashboard | Status para LayoutValidator |
|---|---|---|
| `donutChart` | Elos Minuta | Preditível — legenda + labels |
| `pivotTable` | Rel. Pagamentos, Elos Minuta | Parcialmente preditível |
| `actionButton` | Todos os 3 | Decorativo — não trunca dados |
| `azureMap` | Elos Minuta | Opaco — canvas fixo, sem texto |
| `FlowVisual_*` | Elos Minuta, Rel. Pagamentos | Decorativo — só botão |
| `powerBIGanttChart*` | ESTRATÉGICO | Opaco — visual de marketplace |
| `pageNavigator` | Rel. Pagamentos | Decorativo |

#### donutChart
```
Exemplo: 417.73 × 310.16px (canvas 1800)
Legenda: position=Top, fontSize=10D
Labels (callout): fontSize=11D
```
Quando legenda está Top/Bottom, desconta altura:
`plot_height = visual_height - legend_height`
`legend_height ≈ n_series × (font_pt × 2.0 + 4) + 8px`

#### pivotTable
```
Relatório Pagamentos: 1136.67 × 561.67px, columnAdjustment=growToFit
Elos Minuta:           593.13 × 647.71px, columnWidths explícitas (216D, 434D)
values fontSize:  10–12D
headers fontSize: 10–12D
```
Mesmas fórmulas de row_height e header_height do tableEx (Seção 41.5).
Diferença: `growToFit` distribui o espaço igualmente quando sem columnWidths fixas.

#### actionButton — dimensões por papel
```
Botão "fechar" / close (X):     ~58 × 55px, text 'X', font 20D
Botão "histórico" / toggle (H): ~48 × 49px, text 'H', shape oval, font 12D
Botão de navegação (voltar):    ~199 × 40px, font implícita (sem D explícito)
```
Não contribui para truncamento de dados — ignorar no LayoutValidator.

### 43.4 Escala de fontes por canvas (tabela consolidada 5 dashboards)

| Papel                | 1280×720 | 1800×900 | 1920×1080 | 2200×1200 |
|----------------------|----------|----------|-----------|-----------|
| Valor card (KPI)     | 28pt     | 22–25pt  | 30–35pt   | 24–36pt   |
| Título card          | 11pt     | 15pt     | 22–25pt   | 12–16pt   |
| Header tabela        | 10pt     | 12pt     | 15pt      | 10–12pt   |
| Valores tabela       | 9–10pt   | 12pt     | 13pt      | 10pt      |
| Título slicer        | 10pt     | 14pt     | 20pt      | 16pt      |
| Item slicer          | 8pt      | 14pt     | 18pt      | 16pt      |
| Label gráfico        | n/d      | 11–12pt  | 12–22pt   | 18pt      |

**Conclusão:** não há relação linear simples entre canvas size e font size — o designer escolhe. O RequirementsAgent deve perguntar o canvas target e sugerir fontes baseado em benchmark, não em fórmula rígida.

### 43.5 Padrão de menu toggle via visual groups

Observado no Relatório Pagamentos — alternativa ao bookmarks outspacePane do Databrick Gov:

```
VisualGroup "Menu Escondido"
  x=0, y=96, width=79.65, height=624.22
  GroupMode: ScaleMode
  isHidden: false  ← visível por padrão (menu recolhido)

VisualGroup "Menu Exibido"
  x=0, y=0, width=1280, height=721.04
  GroupMode: ScaleMode
  isHidden: true   ← oculto por padrão
```

Dois grupos se alternam via bookmark — mesma lógica do outspacePane mas implementada como grupos sobrepostos em vez de grupo que desliza para fora do canvas.

### 43.6 Conditional formatting em tabelas (tableEx/pivotTable)

Elos Minuta usou row-level conditional formatting via `selector.data.scopeId.Column`:
```
Status_Validacao = 'Divergência'       → background #D64550 (vermelho)
Status_Validacao = 'Dados Conciliados' → background #049464 (verde)
```
Formato idêntico ao da Seção 36.3 (cor por série em lineChart), mas aplicado em `background` de células de tabela. O LayoutValidator não precisa considerar isso — não afeta dimensões.

### 43.7 Tooltip page — identificação e tratamento

```json
// page.json de página tooltip
"displayOption": "Tooltip",
"visibility": "HiddenInViewMode",
// Dimensões padrão:
"width": 320,
"height": 240
```
O LayoutValidator deve detectar `displayOption = "Tooltip"` e pular a página — as fórmulas de layout não se aplicam ao contexto de tooltip.

*Seção 43 adicionada em 2026-04-23 — extraída de: Relatório Pagamentos (5 págs, 1280×720), ESTRATÉGICO - PROJETOS (4 págs, 2200×1200/1400×1050), Elos Minuta (8 págs, 1800×900 + tooltip)*

---

## Seção 49 — Análise de Qualidade: 7 Dashboards

> Análise visual, funcional e de dados. Serve de benchmark para o DashForge AI. Data: 2026-04-23

### 49.1 Scorecard consolidado

| Dashboard                  | Canvas      | Págs | Visual ★ | Interativ. ★ | Dados ★ | Total |
|----------------------------|-------------|------|----------|--------------|---------|-------|
| **Databrick Gov**          | 1280×720    | 3    | ★★★★★   | ★★★★★       | ★★★★☆  | 14/15 |
| **projeto.pbip**           | 1280×720    | 8    | ★★★★★   | ★★★★★       | ★★★☆☆  | 13/15 |
| **Elos Minuta**            | 1800×900    | 8+tt | ★★★★☆   | ★★★☆☆       | ★★★★★  | 12/15 |
| **Relatório Pagamentos**   | 1280×720    | 5    | ★★★☆☆   | ★★★★☆       | ★★★★★  | 12/15 |
| **Governança BI**          | 1710×800    | 4    | ★★★☆☆   | ★★★★☆       | ★★★★☆  | 11/15 |
| **ESTRATÉGICO - PROJETOS** | 2200×1200   | 4    | ★★★☆☆   | ★★★★☆       | ★★★☆☆  | 10/15 |
| **CONTRATAÇÕES - DGT**     | 1920×1080   | 3    | ★★★☆☆   | ★★★☆☆       | ★★☆☆☆  | 8/15  |

---

### 49.2 Qualidade Visual — análise por dimensão

#### Consistência de design

**★★★★★ Databrick Gov** — único com tema totalmente customizado (shadcn-theme.json). Paleta de 10 cores coerente, border-radius 12px uniforme, tipografia em hierarquia clara (20pt título → 13pt visual → 11pt subtítulo → 9pt dados). Cada visual segue o mesmo padrão de container (background branco + borda #E4E4E7).

**★★★★★ projeto.pbip** — coerência por página temática (dark navy, light, sage-green). Cada página tem identidade própria mas linguagem visual unificada. Glass morphism aplicado consistentemente.

**★★★☆☆ CONTRATAÇÕES - DGT** — paleta #1F5673 aplicada, mas fontes inconsistentes entre páginas (títulos 25D em uma página, 22D em outra). Shape de fundo maior que o canvas (2597×2876px) — workaround de design.

**★★☆☆☆ Governança BI** — 25 imagens como elementos de layout (banners, ícones). Shapes como rótulos de indicadores em vez de visuais nativos. Sensação de "colagem" em vez de dashboard nativo.

#### Adequação do tipo de gráfico ao dado

**Acertos observados:**
- Databrick Gov: barras horizontais para ranking (melhor que treemap, decisão confirmada pelo usuário)
- Governança BI: combo chart (coluna + linha) para realizado vs meta — ideal para esse caso
- Elos Minuta: donut para composição de custo mensal — correto
- Elos Minuta: azureMap para distribuição geográfica de usuários — ideal
- ESTRATÉGICO: Gantt para cronograma de projetos — único chart adequado

**Problemas observados:**
- Governança BI: gauge customizado de marketplace — impacto visual alto mas limitações técnicas; medida `Meta` hardcoded como constante DAX
- CONTRATAÇÕES - DGT: stackedAreaChart para % executado/previsto — legenda Left consome muito espaço lateral

#### Densidade de informação por página

**Alta densidade (problema):**
- Relatório Pagamentos: 142 visuais em 5 páginas = 28 visuais/página em média. Página "deposito de visuais" (39 visuais) indica rascunho não removido — ruído no arquivo PBIR.
- CONTRATAÇÕES - DGT: tabela com 14 colunas — ultrapassa a largura confortável de leitura.

**Densidade ideal:**
- Databrick Gov: 16 visuais/página média, clara hierarquia de atenção (KPIs → gráfico → tabela).
- Governança BI: estrutura 1 gráfico grande + 1 gauge + KPI por página — foco.

---

### 49.3 Qualidade Funcional — análise por dimensão

#### Navegação e orientação do usuário

**★★★★★ Melhor prática — Governança BI**
Imagens de navegação com `tooltip` textual ("Clique para navegar para PJe 1° e 2° Grau"). O usuário sabe para onde vai antes de clicar. PageNavigation em vez de bookmarks — mais simples de manter.

**★★★★★ Melhor prática — projeto.pbip**
Barra de navegação persistente no topo (`exec_nav_bar`), shapes como hotspots invisíveis sobre ícones SVG, 3 destinos sempre visíveis. Padrão de SPA (single page application) no Power BI.

**★★☆☆☆ Problema — Elos Minuta**
8 páginas, 7 delas HiddenInViewMode. Sem bookmarks. Sem pageNavigator. Como o usuário navega? Depende do painel lateral nativo do Power BI — não há controle programático da navegação.

#### Controle de filtros

**★★★★★ Melhor prática — Databrick Gov**
- Gaveta Padrão A: VisualGroup com slicers dentro → oculta para fora do canvas
- 2 bookmarks (abrir/fechar) + 1 ClearAllSlicers independente
- SyncGroup entre páginas: mesmo filtro mantido ao navegar
- InvertedSelectionMode no slicer de categoria: "todos exceto X"

**★★★★★ Melhor prática — projeto.pbip**
- htmlContent como UI de gaveta: CSS puro em medida DAX, sem dependência de shape/image
- `SageDrawerBg` + `SageBtnOpen/Close` — gaveta com backdrop blur animado
- Estado de filtro capturado em bookmark com slicer states

**★★☆☆☆ Ausente — Elos Minuta**
Sem ClearAllSlicers, sem gaveta, sem sinal visual de filtro ativo. O usuário pode não saber que está filtrando.

#### Conteúdo dinâmico

**★★★★★ Melhor prática — Elos Minuta**
```dax
Ultima_Atualizacao = "Atualizado em " & FORMAT(NOW()-TIME(3,0,0), "dd/MM/yyyy HH:mm")
Titulo - Painel Executivo = "Controle de Fiscalização - " & [Periodo Selecionado]
```
Timestamp com correção de fuso horário (UTC-3). Título da página reflete filtro ativo. O usuário sempre sabe quando os dados foram atualizados e qual período está vendo.

**★★★★★ Melhor prática — ESTRATÉGICO**
```dax
ExibirHistorico = IF(ISFILTERED(Projetos[Projeto]), 1, 0)
```
Painel de histórico aparece apenas quando um projeto específico é selecionado. Sem isso o dashboard ficaria poluído com dados de todos os projetos simultaneamente.

**★★★★★ Melhor prática — projeto.pbip**
```dax
HtmlKpiViews → cor condicional por valor, animação de progresso, badge de status
```
Cards que mudam de aparência baseado nos dados — não apenas o valor, mas cor de fundo, ícone e animação.

---

### 49.4 Qualidade de Dados — análise por dimensão

#### Proteção contra contextos inválidos

**★★★★★ Melhor prática — Databrick Gov** (padrão mais rigoroso)
```dax
DIVIDE([A], [B])                         -- nunca divisão direta
IF(HASONEVALUE(T[col]), RANKX(...))      -- rank só com contexto único
CALCULATE(..., ALLEXCEPT(...))           -- participação com contexto controlado
```
Toda medida que pode receber contexto múltiplo tem proteção explícita.

**Problema — CONTRATAÇÕES - DGT**
```dax
Razão = SUM([Valor]) / CALCULATE(SUM([Dotação]), [Ano]="2025")
```
Divisão direta sem DIVIDE. Se o denominador for zero, retorna erro em vez de BLANK. Ano hardcoded como "2025" — quebrará em 2026.

#### Validação e qualidade de dados visível ao usuário

**★★★★★ Melhor prática — Relatório Pagamentos**
KPI dedicado para cada tipo de problema detectado:
```dax
Problemas Encontrados = [Qtd Alvará Faltante] + [Qtd Precatório Faltante] +
                        [Qtd Valor com Problema] + [Assinaturas Faltando]
```
Card muda de cor (#00567E azul → #DE6A73 vermelho) quando há problemas. O usuário vê imediatamente que há dados para corrigir, sem precisar ir à tabela.

**★★★★★ Melhor prática — Elos Minuta**
```dax
Status_Validacao = IF(ABS([ValorCalculado] - [ValorReal]) <= 0.01,
                      "✅ Dados Conciliados", "❌ Divergência encontrada")
```
Reconciliação linha por linha com tolerância de 1 centavo. Aplicada como formatação condicional na tabela — linhas problemáticas ficam vermelhas.

**Ausente — ESTRATÉGICO - PROJETOS e Governança BI**
Nenhum indicador de qualidade de dados. O usuário não tem como saber se os dados do SharePoint estão completos ou com problemas.

#### Frescor e rastreabilidade dos dados

**★★★★★ Elos Minuta** — timestamp visível com fuso horário correto
**★★★☆☆ Governança BI** — `Disponibilidade % (Até Hoje)` usa `KEEPFILTERS(Date <= TODAY())` — dados sempre atuais até hoje, mas sem indicador visual de quando foi o último refresh
**★★☆☆☆ demais** — sem qualquer indicador de atualização

---

### 49.5 Melhores práticas a replicar no DashForge AI (por categoria)

#### Visual
| Prática | Fonte | Implementação |
|---|---|---|
| Tema unificado com theme.json | Databrick Gov | Gerar shadcn-theme.json adaptado ao projeto |
| Hierarquia tipográfica clara: 20→13→11→9pt | Databrick Gov | Hardcoded por canvas size |
| 1 chart grande + KPIs + tabela por página | Databrick Gov + Governança BI | Template de página padrão |
| Barras horizontais para ranking | Databrick Gov | clusteredBarChart + sort DESC |
| Combo chart para meta vs realizado | Governança BI | lineClusteredColumnComboChart |

#### Funcional
| Prática | Fonte | Implementação |
|---|---|---|
| Gaveta com syncGroup cross-page | Databrick Gov | Padrão A + syncConfig |
| ClearAllSlicers dedicado (funnel-x) | Databrick Gov + DGT | Imagem fixa em toda página |
| Timestamp de atualização visível | Elos Minuta | Medida `Ultima_Atualizacao` |
| Título de página reflete filtro ativo | Elos Minuta + Governança BI | SELECTEDVALUE ou Periodo Selecionado |
| ExibirHistorico para painel detalhe | ESTRATÉGICO | ISFILTERED + filtro visual |
| Tooltip em botão de navegação | Governança BI | `tooltip.text` na visualLink |

#### Dados
| Prática | Fonte | Implementação |
|---|---|---|
| DIVIDE() em toda divisão | Databrick Gov | Regra de codegen de medidas |
| HASONEVALUE() antes de RANKX | Databrick Gov | Proteção padrão em medidas de rank |
| KPI de problemas detectados | Relatório Pagamentos | Medida = soma de N validadores |
| Cor condicional do card por alerta | Relatório Pagamentos | Formatação condicional com HEX |
| ABS(diff) <= tolerância | Elos Minuta | Para reconciliação de valores monetários |
| Pasta de medidas (displayFolder) | Databrick Gov | 9 pastas padrão geradas sempre |

---

### 49.6 Anti-padrões identificados (nunca replicar)

| Anti-padrão | Observado em | Problema |
|---|---|---|
| Imagens como elementos de layout (25 imagens/pág) | Governança BI | Manutenção impossível, não responsivo |
| Shapes como rótulos textuais | Governança BI | Não lê via acessibilidade, não escala |
| Shape maior que o canvas (2597×2876px) | CONTRATAÇÕES - DGT | Causa confusão no editor |
| Divisão direta sem DIVIDE | CONTRATAÇÕES - DGT | Erro em runtime quando denominador = 0 |
| Ano hardcoded em medida DAX ("2025") | CONTRATAÇÕES - DGT | Quebra ao virar o ano |
| Página "deposito de visuais" em produção | Relatório Pagamentos | Vaza rascunhos para o arquivo PBIR |
| 8 páginas ocultas sem navegação programática | Elos Minuta | Usuário desorientado |
| Gauge de marketplace como KPI principal | Governança BI | Opaco, não escala, dependência de marketplace |
| Sem indicador de frescor de dados | 4 de 7 dashboards | Usuário não sabe se dados são atuais |

*Seções 48–49 adicionadas em 2026-04-23 — análise qualitativa de 7 dashboards reais*

*Última atualização: 2026-04-18 — baseado em análise das screenshots do Databrick Gov + pesquisa Nielsen Norman Group, Tremor, shadcn/ui, Microsoft Learn*

---

