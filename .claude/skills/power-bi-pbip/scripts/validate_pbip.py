#!/usr/bin/env python3
"""Validador estático de projetos Power BI (PBIP = PBIR + TMDL).

Pega, antes de abrir no Power BI Desktop, os erros que mais quebram projetos
editados fora do Desktop: JSON inválido, BOM, cores em hex puro, pastas/nomes
fora do padrão, pages.json dessincronizado, campos de visual apontando para
tabelas/colunas/medidas inexistentes, indentação TMDL com espaços, lineageTag
inválido ou duplicado, palavras-chave TMDL que não existem, refs quebradas em
model.tmdl e relationships.tmdl, e LocalDateTables órfãs.

Uso:
    python validate_pbip.py <pasta com .pbip | pasta .Report | pasta .SemanticModel>

Sai com código 1 se houver ERROS (avisos não falham).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

GUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
NAME_RE = re.compile(r"^[\w-]+$")
# Palavras-chave que parecem válidas mas não existem em TMDL (causam UnknownKeyword)
BAD_TMDL_KEYWORDS = {
    "isDataTable": "não existe em TMDL; marque tabela de datas pelo Desktop (dataCategory: Time na coluna é o que vai no TMDL)",
    "cardinality": "não existe; muitos-para-um é o padrão (omita). Para muitos-para-muitos use 'toCardinality: many'",
    "calculatedTable": "não existe; use 'partition <nome> = calculated' com 'source ='",
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, path: Path | str, msg: str) -> None:
        self.errors.append(f"[ERRO]  {path}: {msg}")

    def warn(self, path: Path | str, msg: str) -> None:
        self.warnings.append(f"[AVISO] {path}: {msg}")


def unquote(name: str) -> str:
    name = name.strip()
    if len(name) >= 2 and name[0] == "'" and name[-1] == "'":
        return name[1:-1].replace("''", "'")
    return name


def split_name(rest: str) -> str:
    """Extrai o nome de um objeto TMDL em 'measure <nome> = ...' ou 'column <nome>'."""
    rest = rest.strip()
    if rest.startswith("'"):
        i = 1
        while i < len(rest):
            if rest[i] == "'":
                if i + 1 < len(rest) and rest[i + 1] == "'":
                    i += 2
                    continue
                return rest[1:i].replace("''", "'")
            i += 1
        return rest.strip("'")
    return re.split(r"\s*=|\s", rest, maxsplit=1)[0]


def read_text(path: Path, rep: Report) -> str | None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        rep.err(path, "arquivo com BOM UTF-8; salve como UTF-8 sem BOM")
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as e:
        rep.err(path, f"não é UTF-8 válido ({e})")
        return None


# ----------------------------------------------------------------------------- TMDL

def parse_model(sm_dir: Path, rep: Report) -> dict[str, dict[str, set[str]]]:
    """Retorna {tabela: {'columns': set, 'measures': set, 'hierarchies': set}} e valida TMDL."""
    definition = sm_dir / "definition"
    tables: dict[str, dict[str, set[str]]] = {}
    lineage: dict[str, Path] = {}
    if not definition.is_dir():
        rep.warn(sm_dir, "sem pasta definition/ (modelo não está em TMDL? talvez model.bim)")
        return tables

    local_date_tables: dict[str, Path] = {}
    for tmdl in sorted(definition.rglob("*.tmdl")):
        text = read_text(tmdl, rep)
        if text is None:
            continue
        current_table: str | None = None
        in_backticks = False
        # Bloco de expressão multilinha sem crases: (profundidade mínima exigida, linha que abriu, já viu conteúdo?)
        expr_block: tuple[int, int, bool] | None = None
        bad_runs: list[list[int]] = []
        bad_run: list[int] | None = None
        for n, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if in_backticks:
                if stripped == "```":
                    in_backticks = False
                continue
            indent = line[: len(line) - len(line.lstrip())]
            depth = len(indent.replace("    ", "\t"))
            if not stripped:
                continue
            if expr_block is not None:
                need, opened, seen = expr_block
                if depth >= need:
                    expr_block = (need, opened, True)
                    continue
                if not seen:
                    rep.err(f"{tmdl}:{n}", f"expressão multilinha aberta na linha {opened} precisa começar com {need} TAB(s) "
                            "(um nível abaixo das propriedades) — ou use o bloco com ```")
                expr_block = None
            if indent.startswith(" "):
                rep.warn(f"{tmdl}:{n}", "indentação começa com espaço; TMDL usa TAB (espaços só são aceitos dentro de expressões)")
            if stripped.startswith("//") and not stripped.startswith("///"):
                rep.err(f"{tmdl}:{n}", "comentário '//' não é suportado em TMDL (só dentro de expressões DAX/M); use '///' para descrição do objeto")
                continue
            if not re.match(r"^(///|[A-Za-z_][\w.]*(\s|:|=|$))", stripped):
                if bad_run and bad_run[1] == n - 1:
                    bad_run[1] = n
                else:
                    bad_run = [n, n]
                    bad_runs.append(bad_run)
                continue
            # Registra objetos ANTES de tratar crases (a declaração pode terminar com ```)
            if depth == 0 and stripped.startswith("table "):
                current_table = split_name(stripped[6:])
                tables[current_table] = {"columns": set(), "measures": set(), "hierarchies": set()}
                if current_table.startswith("LocalDateTable_"):
                    local_date_tables[current_table] = tmdl
            elif depth == 1 and current_table:
                for kind, key in (("column ", "columns"), ("measure ", "measures"), ("hierarchy ", "hierarchies")):
                    if stripped.startswith(kind):
                        tables[current_table][key].add(split_name(stripped[len(kind):]))
            if stripped.endswith("```"):
                in_backticks = True
                continue
            if stripped.endswith("="):
                is_object = bool(re.match(r"^(measure|column|partition|expression|table|calculationItem|function)\b", stripped))
                expr_block = (depth + (2 if is_object else 1), n, False)
            for kw, why in BAD_TMDL_KEYWORDS.items():
                if re.match(rf"^{kw}\b", stripped):
                    rep.err(f"{tmdl}:{n}", f"'{kw}' {why}")
            m = re.match(r"^lineageTag:\s*(\S+)", stripped)
            if m:
                tag = m.group(1)
                if not GUID_RE.match(tag):
                    rep.err(f"{tmdl}:{n}", f"lineageTag '{tag}' não é GUID 8-4-4-4-12 hexadecimal")
                elif tag.lower() in lineage and lineage[tag.lower()] != tmdl:
                    rep.err(f"{tmdl}:{n}", f"lineageTag {tag} duplicado (também em {lineage[tag.lower()]})")
                lineage.setdefault(tag.lower(), tmdl)
        for a, b in bad_runs:
            where = f"{a}" if a == b else f"{a}-{b}"
            rep.err(f"{tmdl}:{where}", "linha(s) fora de expressão que não são objeto nem propriedade — provável DAX/M multilinha "
                    "no nível errado. Sem crases, a expressão inteira vai um nível abaixo das propriedades; ou use o bloco com ```")

    # model.tmdl: refs ↔ arquivos
    model = definition / "model.tmdl"
    if model.exists():
        text = read_text(model, rep) or ""
        refs = {unquote(m.group(1)) for m in re.finditer(r"^ref table (.+)$", text, re.M)}
        for ref in refs - tables.keys():
            rep.err(model, f"'ref table {ref}' sem arquivo tables/{ref}.tmdl correspondente")
        for t in tables.keys() - refs:
            rep.warn(model, f"tabela '{t}' existe em tables/ mas não tem 'ref table' em model.tmdl (o Desktop lê o arquivo mesmo assim)")

    # relationships.tmdl: colunas existem; LocalDateTables têm relacionamento
    rel = definition / "relationships.tmdl"
    targeted: set[str] = set()
    if rel.exists():
        text = read_text(rel, rep) or ""
        for n, line in enumerate(text.splitlines(), 1):
            m = re.match(r"^\s*(fromColumn|toColumn):\s*(.+)$", line)
            if not m:
                continue
            table, col = parse_col_ref(m.group(2))
            if table is None:
                rep.err(f"{rel}:{n}", f"referência de coluna ilegível: {m.group(2)}")
                continue
            if table.startswith("LocalDateTable_"):
                targeted.add(table)
            if table not in tables:
                rep.err(f"{rel}:{n}", f"tabela '{table}' não existe no modelo")
            elif col not in tables[table]["columns"]:
                rep.err(f"{rel}:{n}", f"coluna '{table}'.'{col}' não existe")
    for t, path in local_date_tables.items():
        if t not in targeted:
            rep.err(path, "LocalDateTable órfã (nenhum relacionamento aponta para ela). Apague o ARQUIVO — tirar só o 'ref' não basta")
    return tables


def parse_col_ref(ref: str) -> tuple[str | None, str | None]:
    ref = ref.strip()
    m = re.match(r"^('(?:[^']|'')+'|[^.'\s]+)\.('(?:[^']|'')+'|.+)$", ref)
    if not m:
        return None, None
    return unquote(m.group(1)), unquote(m.group(2))


# ----------------------------------------------------------------------------- PBIR

def iter_field_refs(node, path=""):
    """Gera (tipo, entidade, propriedade) de referências a campos com Entity explícita."""
    if isinstance(node, dict):
        for kind in ("Column", "Measure", "Hierarchy"):
            v = node.get(kind)
            if isinstance(v, dict):
                ent = v.get("Expression", {}).get("SourceRef", {}).get("Entity")
                prop = v.get("Property") if kind != "Hierarchy" else v.get("Hierarchy")
                if ent and prop:
                    yield kind, ent, prop
        for k, v in node.items():
            yield from iter_field_refs(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from iter_field_refs(v, f"{path}[{i}]")


def find_plain_colors(node, path=""):
    """Cores como string '#RRGGBB' direta são ignoradas pelo Desktop."""
    if isinstance(node, dict):
        for k, v in node.items():
            # Exceção: textbox usa CSS puro em textRuns[].textStyle.color
            if k == "color" and isinstance(v, str) and v.strip().startswith("#") and not path.endswith("textStyle"):
                yield f"{path}.{k}"
            else:
                yield from find_plain_colors(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from find_plain_colors(v, f"{path}[{i}]")


def load_json(path: Path, rep: Report):
    text = read_text(path, rep)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        rep.err(path, f"JSON inválido: {e}")
        return None


def validate_report(rp_dir: Path, tables: dict, rep: Report) -> None:
    definition = rp_dir / "definition"
    if not definition.is_dir():
        if (rp_dir / "report.json").exists():
            rep.warn(rp_dir, "relatório em PBIR-Legacy (report.json) — não suporta edição externa. Salve no Desktop com PBIR ativado")
        return

    for jf in sorted(definition.rglob("*.json")):
        data = load_json(jf, rep)
        if data is None:
            continue
        if isinstance(data, dict) and "$schema" not in data:
            rep.warn(jf, "sem '$schema' — o Desktop valida contra ele")
        for p in find_plain_colors(data):
            rep.err(jf, f"cor em hex puro em {p}; use {{\"expr\": {{\"Literal\": {{\"Value\": \"'#RRGGBB'\"}}}}}}")
        if tables:
            for kind, ent, prop in iter_field_refs(data):
                t = tables.get(ent)
                if t is None:
                    rep.err(jf, f"{kind} aponta para tabela inexistente '{ent}'")
                    continue
                key = {"Column": "columns", "Measure": "measures", "Hierarchy": "hierarchies"}[kind]
                if prop not in t[key]:
                    # Coluna referenciada como medida (ou vice-versa) é erro comum
                    other = [k for k in ("columns", "measures") if prop in t[k]]
                    hint = f" (existe como {other[0][:-1]})" if other else ""
                    rep.err(jf, f"{kind} '{ent}'.'{prop}' não existe no modelo{hint}")

    pages_dir = definition / "pages"
    pages_json = pages_dir / "pages.json"
    if not pages_json.exists():
        rep.err(pages_dir, "pages.json ausente")
        return
    meta = load_json(pages_json, rep) or {}
    order = meta.get("pageOrder", [])
    folders = {p.name for p in pages_dir.iterdir() if p.is_dir()}
    for pid in order:
        if pid not in folders:
            rep.err(pages_json, f"pageOrder cita '{pid}' mas a pasta pages/{pid}/ não existe")
    for f in folders - set(order):
        rep.warn(pages_json, f"pasta pages/{f}/ não está em pageOrder (página não aparece)")
    active = meta.get("activePageName")
    if active and active not in order:
        rep.warn(pages_json, f"activePageName '{active}' não está em pageOrder")

    for page in sorted(pages_dir.iterdir()):
        if not page.is_dir():
            continue
        if not NAME_RE.match(page.name):
            rep.err(page, "nome de pasta só pode ter letras, dígitos, _ ou - (senão o Desktop ignora)")
        pj = page / "page.json"
        if not pj.exists():
            rep.err(page, "page.json ausente")
            continue
        pdata = load_json(pj, rep) or {}
        if pdata.get("name") != page.name:
            rep.warn(pj, f"'name' ({pdata.get('name')}) difere do nome da pasta ({page.name})")
        groups: set[str] = set()
        parents: list[tuple[Path, str]] = []
        vdir = page / "visuals"
        for vis in sorted(vdir.iterdir()) if vdir.is_dir() else []:
            if not vis.is_dir():
                continue
            if not NAME_RE.match(vis.name):
                rep.err(vis, "nome de pasta inválido (use letras, dígitos, _ ou -)")
            vj = vis / "visual.json"
            if not vj.exists():
                rep.err(vis, "visual.json ausente")
                continue
            v = load_json(vj, rep) or {}
            if v.get("name") != vis.name:
                rep.warn(vj, f"'name' ({v.get('name')}) difere do nome da pasta ({vis.name})")
            pos = v.get("position")
            if not isinstance(pos, dict) or not all(k in pos for k in ("x", "y", "width", "height")):
                rep.err(vj, "position precisa de x, y, width e height")
            else:
                pw, ph = pdata.get("width"), pdata.get("height")
                if pw and ph and (pos["x"] + pos["width"] > pw + 1 or pos["y"] + pos["height"] > ph + 1):
                    rep.warn(vj, f"visual ultrapassa a página ({pw}x{ph})")
            if "visualGroup" in v:
                groups.add(v.get("name", vis.name))
            if "parentGroupName" in v:
                parents.append((vj, v["parentGroupName"]))
            if "visual" not in v and "visualGroup" not in v:
                rep.err(vj, "precisa de 'visual' ou 'visualGroup'")
        for vj, g in parents:
            if g not in groups:
                rep.err(vj, f"parentGroupName '{g}' não corresponde a nenhum visualGroup da página")


# ----------------------------------------------------------------------------- main

def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1]).resolve()
    rep = Report()
    if root.name.endswith(".Report"):
        reports, models = [root], []
    elif root.name.endswith(".SemanticModel"):
        reports, models = [], [root]
    else:
        reports = sorted(p for p in root.glob("*.Report") if p.is_dir())
        models = sorted(p for p in root.glob("*.SemanticModel") if p.is_dir())

    tables: dict = {}
    for sm in models:
        tables.update(parse_model(sm, rep))
    for rp in reports:
        if not models:
            pbir = rp / "definition.pbir"
            if pbir.exists():
                ref = (load_json(pbir, rep) or {}).get("datasetReference", {}).get("byPath", {}).get("path")
                if ref and (rp / ref).resolve().is_dir():
                    tables.update(parse_model((rp / ref).resolve(), rep))
        validate_report(rp, tables, rep)

    if not reports and not models:
        print(f"Nenhuma pasta .Report ou .SemanticModel encontrada em {root}")
        return 2
    rep.errors = list(dict.fromkeys(rep.errors))
    rep.warnings = list(dict.fromkeys(rep.warnings))
    for line in rep.errors + rep.warnings:
        print(line)
    print(f"\n{len(rep.errors)} erro(s), {len(rep.warnings)} aviso(s) — "
          f"{len(reports)} relatório(s), {len(models)} modelo(s), {len(tables)} tabela(s) lidas")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
