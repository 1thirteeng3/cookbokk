"""Roadmap: order and wave of implementation for every recipe and project.

    python tools/roadmap.py            # regenerate ROADMAP.md and config/roadmap.yml
    python tools/roadmap.py --check    # exit 1 if they are stale or do not cover the catalog

The plan is computed, not typed in, so it stays consistent with the catalog:

1. W0  recipes the pilot project (P1.01) cites.
2. W1  core: all of Part A plus every recipe used by 4+ projects.
3. W2–W10  project-pull: for each project, in domain-priority order, first the recipes it needs
   that are still unwritten, then the project itself. A recipe is written for the first
   project that needs it.
4. W11–W14  coverage: recipes no project needs, by part.

Changing priorities means editing WAVES / PROJECT_ORDER below and running the tool.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, Catalog, dump_yaml, load_catalog, write_if_changed  # noqa: E402

ROADMAP_MD = ROOT / "ROADMAP.md"
ROADMAP_YML = ROOT / "config" / "roadmap.yml"

POINTS = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}  # relative effort of a recipe by level
PROJECT_POINTS = 8  # a project: document + ~8 notebooks (P1.01 as the reference)
PILOT = "P1.01"
CORE_MIN_PROJECTS = 4  # a recipe used by this many projects belongs to the core

# Each project wave: (wave id, title, goal, [project ids in order])
PROJECT_WAVES = [
    ("W2", "Crédito", "Fechar a vertical de crédito e risco de crédito (P1.02–P1.10).", "P1", None),
    (
        "W3",
        "Fraude, PLD/AML e compliance",
        "Fechar a vertical de fraude e conformidade (P2).",
        "P2",
        None,
    ),
    (
        "W4",
        "Mercados e tesouraria",
        "Dados de mercado, portfólio, risco de mercado e sinais de texto (P3).",
        "P3",
        None,
    ),
    (
        "W5",
        "Macroeconomia",
        "Nowcasting, inflação, política monetária e risco sistêmico (P4).",
        "P4",
        None,
    ),
    (
        "W6",
        "Socioeconomia e políticas públicas",
        "Avaliação de impacto, pobreza, microssimulação e mercado de trabalho (P5).",
        "P5",
        None,
    ),
    (
        "W7",
        "Plataformas I: dados e MLOps",
        "Lakehouse com Open Finance e plataforma de MLOps com gestão de risco de modelos (P6.01–P6.02).",
        "P6",
        ("P6.01", "P6.02"),
    ),
    (
        "W8",
        "Plataformas II: LLMOps, DataOps e atendimento",
        "LLMOps regulado, DataOps e agente de atendimento com auditoria (P6.03–P6.05).",
        "P6",
        ("P6.03", "P6.05"),
    ),
    (
        "W9",
        "Plataformas III: IA financeira e auditoria",
        "Dados sintéticos, LLM financeiro em PT-BR, analista com IA e auditoria agêntica (P6.06–P6.09).",
        "P6",
        ("P6.06", "P6.09"),
    ),
    ("W10", "Outros domínios", "Amplitude técnica fora de finanças (P7).", "P7", None),
]
# Coverage waves: (wave id, title, goal, parts)
COVERAGE_WAVES = [
    (
        "W11",
        "Cobertura: dados e ML clássico",
        "Receitas de A–K que nenhum projeto exige.",
        "ABCDGHIJK",
    ),
    ("W12", "Cobertura: deep learning e IA", "Receitas de E e F que nenhum projeto exige.", "EF"),
    ("W13", "Cobertura: auditoria e domínio", "Receitas de M e N que nenhum projeto exige.", "MN"),
    (
        "W14",
        "Cobertura: ciências generativas",
        "Receitas de L (fronteira) que nenhum projeto exige.",
        "L",
    ),
]

GATES = {
    "W0": "As 22 receitas passam no `make check`, cumprem a Definição de Pronto (SPEC §9) e todos os links do P1.01 resolvem. Anotar o tempo real gasto por receita: ele calibra o prazo de todas as ondas seguintes.",
    "W1": "Núcleo `done`. Nenhum projeto das ondas seguintes precisa reescrever uma técnica do núcleo.",
    "default": "Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.",
}


# --------------------------------------------------------------------------------------
# Plan
# --------------------------------------------------------------------------------------


def _num(item_id: str) -> tuple[str, int, int]:
    m = re.match(r"^([A-NP])(\d+)\.(\d+)$", item_id)
    return m.group(1), int(m.group(2)), int(m.group(3))


def resolve_refs(token: str, recipe_ids: list[str]) -> list[str]:
    """Expand one entry of a project's ``recipes`` list: id, section (G1), or range (B1–B5)."""
    token = token.strip()
    if "–" in token:
        a, b = (s.strip() for s in token.split("–"))
        if "." in a:  # L2.04–L2.08
            part, sec, n1 = _num(a)
            n2 = _num(b if "." in b else f"{part}{sec}.{b}")[2]
            return [i for i in recipe_ids if _num(i)[:2] == (part, sec) and n1 <= _num(i)[2] <= n2]
        return [  # B1–B5
            i for i in recipe_ids if _num(i)[0] == a[0] and int(a[1:]) <= _num(i)[1] <= int(b[1:])
        ]
    if token in recipe_ids:
        return [token]
    return [i for i in recipe_ids if i.startswith(token + ".")]


def pilot_citations(cat: Catalog, recipe_ids: list[str]) -> set[str]:
    """Recipes cited by the pilot: its metadata list plus links in its documents."""
    pilot = next(i for i in cat.all_items() if i.id == PILOT)
    cited: set[str] = set()
    for token in pilot.meta.get("recipes", []):
        cited.update(resolve_refs(token, recipe_ids))
    for lang in ("pt", "en"):
        doc = pilot.doc(lang)
        if doc.exists():
            cited.update(
                re.findall(
                    r"recipes/[^/\s)]+/[^/\s)]+/([A-N]\d+\.\d{2})-", doc.read_text(encoding="utf-8")
                )
            )
    return cited & set(recipe_ids)


def build_plan(cat: Catalog) -> dict:
    recipes = {i.id: i for i in cat.all_items() if i.kind == "recipe"}
    projects = {i.id: i for i in cat.all_items() if i.kind == "project"}
    rids = sorted(recipes, key=_num)

    used_by: dict[str, set[str]] = {r: set() for r in rids}
    for pid, p in projects.items():
        for token in p.meta.get("recipes", []):
            for r in resolve_refs(token, rids):
                used_by[r].add(pid)

    scheduled: set[str] = set()
    rows: list[dict] = []
    waves: list[dict] = []

    def add(wave: str, item_id: str, why: str) -> None:
        item = recipes.get(item_id) or projects[item_id]
        level = item.meta.get("level")
        rows.append(
            {
                "seq": len(rows) + 1,
                "id": item_id,
                "kind": item.kind,
                "wave": wave,
                "level": level or "—",
                "points": POINTS[level] if item.kind == "recipe" else PROJECT_POINTS,
                "title": item.meta["title"]["pt"],
                "why": why,
            }
        )
        scheduled.add(item_id)

    def recipe_order(ids) -> list[str]:
        return sorted(
            ids, key=lambda i: (_num(i)[:2], POINTS[recipes[i].meta["level"]], _num(i)[2])
        )

    # W0: what the pilot cites
    waves.append(
        {
            "id": "W0",
            "title": "Piloto fechado",
            "goal": f"Escrever as receitas que o {PILOT} já cita, para os links do piloto levarem a conteúdo.",
        }
    )
    for r in recipe_order(pilot_citations(cat, rids)):
        add("W0", r, f"citada por {PILOT}")
    add("W0", PILOT, "piloto (já concluído)")

    # W1: core
    waves.append(
        {
            "id": "W1",
            "title": "Núcleo transversal",
            "goal": f"Parte A inteira e toda receita usada por {CORE_MIN_PROJECTS}+ projetos.",
        }
    )
    core = [
        r
        for r in rids
        if r not in scheduled and (r[0] == "A" or len(used_by[r]) >= CORE_MIN_PROJECTS)
    ]
    for r in recipe_order(core):
        add(
            "W1",
            r,
            "fundação (Parte A)" if r[0] == "A" else f"usada por {len(used_by[r])} projetos",
        )

    # W2–W9: project pull
    for wid, title, goal, group, span in PROJECT_WAVES:
        waves.append({"id": wid, "title": title, "goal": goal})
        for pid in sorted(projects, key=_num):
            if projects[pid].meta["group"] != group or pid in scheduled:
                continue
            if span and not (span[0] <= pid <= span[1]):
                continue
            for r in recipe_order(r for r in rids if pid in used_by[r] and r not in scheduled):
                add(wid, r, f"puxada por {pid}")
            add(wid, pid, "projeto integrador")

    # W10–W13: coverage
    for wid, title, goal, parts in COVERAGE_WAVES:
        waves.append({"id": wid, "title": title, "goal": goal})
        for r in recipe_order(r for r in rids if r[0] in parts and r not in scheduled):
            add(wid, r, "cobertura (nenhum projeto exige)")

    return {"rows": rows, "waves": waves, "catalog": set(recipes) | set(projects)}


def check_coverage(plan: dict) -> list[str]:
    ids = [r["id"] for r in plan["rows"]]
    problems = []
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        problems.append(f"itens repetidos: {sorted(dup)}")
    missing = plan["catalog"] - set(ids)
    if missing:
        problems.append(f"itens fora do roadmap: {sorted(missing)}")
    extra = set(ids) - plan["catalog"]
    if extra:
        problems.append(f"itens que não existem no catálogo: {sorted(extra)}")
    return problems


# --------------------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------------------


def _esc(text: str) -> str:
    return text.replace("|", "\\|")


def render_yaml(plan: dict) -> str:
    data = {
        "waves": [
            {
                "id": w["id"],
                "title": w["title"],
                "items": [r["id"] for r in plan["rows"] if r["wave"] == w["id"]],
            }
            for w in plan["waves"]
        ]
    }
    header = "# Gerado por tools/roadmap.py. Não edite: altere as regras no script e rode `make roadmap`.\n"
    return dump_yaml(data, header)


def render_md(plan: dict) -> str:
    rows, waves = plan["rows"], plan["waves"]
    total_pts = sum(r["points"] for r in rows)
    n_rec = sum(r["kind"] == "recipe" for r in rows)
    n_prj = len(rows) - n_rec
    out: list[str] = []
    w = out.append

    w("# Roadmap de implementação\n")
    w(
        "> Gerado por `tools/roadmap.py` a partir do catálogo. Não edite à mão: mude as regras no script e rode `make roadmap`.\n"
    )
    w(
        f"Este roteiro ordena **todos os {len(rows)} itens** do cookbook ({n_rec} receitas e {n_prj} projetos integradores) em {len(waves)} ondas, com número de ordem único de 1 a {len(rows)}.\n"
    )

    w("## 1. Como a ordem foi decidida\n")
    w(
        f"1. **Quem já é citado vem primeiro.** O projeto-piloto ({PILOT}) aponta para 22 receitas que ainda não existem. Escrevê-las fecha o piloto e dá resultados reais para citar."
    )
    w(
        f"2. **Fundações antes de aplicações.** A Parte A e toda receita usada por {CORE_MIN_PROJECTS} ou mais projetos formam o núcleo, para que nenhum projeto reescreva uma técnica básica."
    )
    w(
        "3. **Projetos puxam as receitas de que precisam.** Do crédito ao socioeconômico, cada projeto integrador espera as receitas que ele cita e só então é escrito. Uma receita é escrita para o primeiro projeto que a usa. Assim, cada onda termina com um playbook completo e utilizável."
    )
    w(
        "4. **Finanças, economia e socioeconomia primeiro**, como definido no índice: P1 a P6 antes de P7 (outros domínios)."
    )
    w("5. **O que nenhum projeto exige entra por último**, agrupado por parte (cobertura).")
    w("6. **Dentro de cada grupo**, a ordem é por parte e seção, do nível L1 ao L4.\n")

    w("## 2. Resumo das ondas\n")
    w("| Onda | Foco | Receitas | Projetos | Pontos | Acumulado |")
    w("|---|---|---:|---:|---:|---:|")
    done = 0
    for wv in waves:
        wr = [r for r in rows if r["wave"] == wv["id"]]
        done += len(wr)
        rec = sum(r["kind"] == "recipe" for r in wr)
        w(
            f"| [{wv['id']}](#{wv['id'].lower()}-{_slug(wv['title'])}) | {wv['title']} | {rec} | {len(wr) - rec} | {sum(r['points'] for r in wr)} | {done}/{len(rows)} ({100 * done // len(rows)}%) |"
        )
    w(f"| **Total** | | **{n_rec}** | **{n_prj}** | **{total_pts}** | |\n")
    w(
        f"**Pontos** medem esforço relativo, não horas: receita L1 = 1, L2 = 2, L3 = 3, L4 = 4; projeto integrador = {PROJECT_POINTS}. O P1.01 serve de referência para o projeto.\n"
    )

    w("## 3. Ritmo e prazo\n")
    w(
        "O prazo depende do ritmo, e ele só é conhecido depois da onda 0. Por isso a tabela abaixo é um cenário, não uma previsão: **meça os pontos concluídos por mês na W0 e substitua o ritmo.**\n"
    )
    w(
        f"| Ritmo (pontos/mês) | Prazo total | Prazo até o fim da {PROJECT_WAVES[-1][0]} (todos os projetos) |"
    )
    w("|---:|---:|---:|")
    coverage_ids = {c[0] for c in COVERAGE_WAVES}
    pts_projects = sum(r["points"] for r in rows if r["wave"] not in coverage_ids)
    for rate in (20, 40, 80):
        w(
            f"| {rate} (≈ {rate / 3:.0f} receitas L3) | {_months(total_pts / rate)} | {_months(pts_projects / rate)} |"
        )
    w("")
    w(
        f"Como referência de escala, {total_pts} pontos são uma obra de muitos meses mesmo no ritmo mais alto. Se isso for demais, as duas saídas honestas são cortar escopo (parar após a {PROJECT_WAVES[-1][0]} e tratar as ondas de cobertura como opcionais) ou reduzir a profundidade das receitas de L1 e L2. Essa escolha é sua e vale decidir depois de medir o ritmo.\n"
    )

    w("## 4. Regras do roadmap\n")
    w(
        "- **Fim de onda:** nada da onda seguinte começa em definitivo antes do critério de saída da atual. Pode-se adiantar rascunhos."
    )
    w(
        "- **Replanejar a cada onda:** ao fechar uma onda, medir o ritmo real, rever prioridades e rodar `make roadmap`."
    )
    w(
        "- **Mudança de prioridade:** edite `PROJECT_WAVES` ou `COVERAGE_WAVES` em `tools/roadmap.py`. O `--check` garante que nenhum item some ou se repete."
    )
    w(
        "- **Revisões periódicas** (SPEC §12) continuam valendo para o que já está pronto e competem por tempo com a escrita nova.\n"
    )

    w("## 5. Ondas\n")
    for wv in waves:
        wr = [r for r in rows if r["wave"] == wv["id"]]
        rec = sum(r["kind"] == "recipe" for r in wr)
        w(f"### {wv['id']} · {wv['title']}\n")
        w(
            f"{wv['goal']} **{_plural(rec, 'receita')} e {_plural(len(wr) - rec, 'projeto')}, {sum(r['points'] for r in wr)} pontos.**\n"
        )
        w(f"**Critério de saída:** {GATES.get(wv['id'], GATES['default'])}\n")
        w("| Ordem | ID | Nível | Título | Motivo |")
        w("|---:|---|---|---|---|")
        for r in wr:
            w(f"| {r['seq']} | {r['id']} | {r['level']} | {_esc(r['title'])} | {r['why']} |")
        w("")

    w("## 6. Como regenerar\n")
    w(
        "```bash\nmake roadmap     # reescreve ROADMAP.md e config/roadmap.yml\nmake check       # inclui `roadmap.py --check`\n```"
    )
    return "\n".join(out).rstrip() + "\n"


def _slug(text: str) -> str:
    text = text.lower()
    for a, b in (
        ("ç", "c"),
        ("ã", "a"),
        ("á", "a"),
        ("â", "a"),
        ("é", "e"),
        ("ê", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("õ", "o"),
        ("ú", "u"),
    ):
        text = text.replace(a, b)
    # Same rule as Markdown heading anchors: drop punctuation, spaces become hyphens
    text = re.sub(r"[^a-z0-9 -]", "", text)
    return re.sub(r"\s", "-", text.strip())


def _plural(n: int, word: str) -> str:
    return f"{n} {word}{'s' if n != 1 else ''}"


def _months(m: float) -> str:
    if m < 12:
        return f"{m:.0f} meses"
    return f"{m / 12:.1f} anos ({m:.0f} meses)".replace(".", ",")


def build(cat: Catalog) -> dict[Path, str]:
    plan = build_plan(cat)
    problems = check_coverage(plan)
    if problems:
        raise SystemExit("roadmap: " + "; ".join(problems))
    return {ROADMAP_MD: render_md(plan), ROADMAP_YML: render_yaml(plan)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    outputs = build(load_catalog())
    if args.check:
        stale = [
            p.name
            for p, t in outputs.items()
            if not p.exists() or p.read_text(encoding="utf-8") != t
        ]
        if stale:
            print(f"roadmap desatualizado: {', '.join(stale)} (rode `make roadmap`)")
            return 1
        print("roadmap ok")
        return 0
    changed = [p.name for p, t in outputs.items() if write_if_changed(p, t)]
    print(f"roadmap: {len(changed)} arquivo(s) atualizado(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
