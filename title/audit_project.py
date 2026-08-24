from __future__ import annotations

import collections
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CORE_TEXTS = (
    "intro.tex",
    "chapter_1.tex",
    "chapter_2.tex",
    "chapter_3.tex",
    "chapter_4.tex",
    "conclusions.tex",
    "abstract_uk.tex",
)
FORMULA_TEXTS = ("chapter_2.tex", "chapter_3.tex", "chapter_4.tex")
AUTHOR_KEYS = {
    "denysiuk2023steganalysis",
    "denysiuk2024behavior",
    "denysiuk2024implantscorporate",
    "denysiuk2024botnets",
    "denysiuk2024decoysystem",
    "denysiuk2024systemdecoys",
    "denysiuk2024intrusions",
    "denysiuk2025parallel",
    "denysiuk2025commands",
    "denysiuk2026multimediahidden",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def tex_plain(text: str) -> str:
    text = re.sub(r"(?m)%.*$", " ", text)
    text = re.sub(r"\\(?:begin|end)\{[^}]+\}", " ", text)
    text = re.sub(r"\\(?:chapter|section|subsection)\*?\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:textbf|textit|emph|foreignterm)\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:addcontentsline|label|cite\w*|ref|eqref|pageref)\{[^}]*\}", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = text.replace("~", " ").replace("{", " ").replace("}", " ").replace("$", " ")
    return re.sub(r"\s+", " ", text).strip()


def line_hits(text: str, pattern: re.Pattern[str]) -> list[str]:
    return [
        f"{number}: {line.strip()}"
        for number, line in enumerate(text.splitlines(), 1)
        if pattern.search(line)
    ]


def parse_equations(text: str) -> list[dict[str, object]]:
    equations: list[dict[str, object]] = []
    pattern = re.compile(r"\\begin\{equation\}(.*?)\\end\{equation\}", re.S)
    for match in pattern.finditer(text):
        start_line = text.count("\n", 0, match.start()) + 1
        body = match.group(1)
        labels = re.findall(r"\\label\{([^}]+)\}", body)
        significant = []
        for raw in body.splitlines():
            clean = re.sub(r"%.*$", "", raw).strip()
            clean = re.sub(r"\\label\{[^}]+\}", "", clean).strip()
            clean = re.sub(r"\\(?:begin|end)\{gathered\}", "", clean).strip()
            if clean:
                significant.append(clean)
        last = significant[-1] if significant else ""
        tail = text[match.end() :]
        next_line = ""
        for raw in tail.splitlines():
            clean = re.sub(r"%.*$", "", raw).strip()
            if clean:
                next_line = clean
                break
        prefix = text[: match.start()].rstrip()
        previous = prefix.splitlines()[-1].strip() if prefix else ""
        equations.append(
            {
                "line": start_line,
                "labels": labels,
                "last": last,
                "next": next_line,
                "previous": previous,
            }
        )
    return equations


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    stats: list[str] = []

    manuscript_paths = sorted(ROOT.glob("*.tex"))
    manuscript_text = "\n".join(read(path) for path in manuscript_paths)
    figure_inputs = sorted(set(re.findall(r"\\input\{(figures_tex/[^}]+)\}", manuscript_text)))
    tex_paths = manuscript_paths + [
        (ROOT / target) if Path(target).suffix else (ROOT / target).with_suffix(".tex")
        for target in figure_inputs
    ]
    texts = {path.relative_to(ROOT).as_posix(): read(path) for path in tex_paths}
    corpus = "\n".join(texts.values())

    required = {
        "title.tex",
        "abstract_uk.tex",
        "abstract_en.tex",
        "publications.tex",
        "abbreviations.tex",
        "intro.tex",
        "chapter_1.tex",
        "chapter_2.tex",
        "chapter_3.tex",
        "chapter_4.tex",
        "conclusions.tex",
        "references.tex",
        "appendices.tex",
        "references.bib",
    }
    missing_required = sorted(name for name in required if not (ROOT / name).exists())
    if missing_required:
        failures.append("Відсутні обов’язкові файли: " + ", ".join(missing_required))

    main_text = texts.get("main.tex", "")
    main_inputs = re.findall(r"\\input\{([^}]+)\}", main_text)
    required_order = [
        "title",
        "abstract_uk",
        "abstract_en",
        "publications",
        "abbreviations",
        "intro",
        "chapter_1",
        "chapter_2",
        "chapter_3",
        "chapter_4",
        "conclusions",
        "references",
        "appendices",
    ]
    filtered = [item for item in main_inputs if item != "preamble"]
    if filtered != required_order:
        failures.append(f"Порушено порядок структурних частин у main.tex: {filtered}")

    missing_inputs: list[str] = []
    for source_name, text in texts.items():
        source = ROOT / source_name
        for target in re.findall(r"\\input\{([^}]+)\}", text):
            candidate = source.parent / target
            if not candidate.exists() and not candidate.with_suffix(".tex").exists():
                missing_inputs.append(f"{source_name}: {target}")
    if missing_inputs:
        failures.append("Відсутні цілі input: " + "; ".join(missing_inputs))

    labels = re.findall(r"\\label\{([^}]+)\}", corpus)
    refs = re.findall(r"\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}", corpus)
    duplicate_labels = sorted(key for key, count in collections.Counter(labels).items() if count > 1)
    missing_refs = sorted(set(refs) - set(labels))
    if duplicate_labels:
        failures.append("Дубльовані мітки: " + ", ".join(duplicate_labels))
    if missing_refs:
        failures.append("Нерозв’язані текстові посилання: " + ", ".join(missing_refs))

    bib_text = read(ROOT / "references.bib")
    bib_keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib_text)
    duplicate_bib = sorted(key for key, count in collections.Counter(bib_keys).items() if count > 1)
    cite_keys: list[str] = []
    for group in re.findall(r"\\cite\w*\{([^}]+)\}", corpus):
        cite_keys.extend(key.strip() for key in group.split(",") if key.strip())
    unknown_cites = sorted(set(cite_keys) - set(bib_keys))
    unused_bib = sorted(set(bib_keys) - set(cite_keys))
    missing_author_cites = sorted(AUTHOR_KEYS - set(cite_keys))
    missing_author_bib = sorted(AUTHOR_KEYS - set(bib_keys))
    if duplicate_bib:
        failures.append("Дубльовані бібліографічні ключі: " + ", ".join(duplicate_bib))
    if unknown_cites:
        failures.append("Невідомі ключі цитування: " + ", ".join(unknown_cites))
    if unused_bib:
        failures.append("Не процитовані джерела у references.bib: " + ", ".join(unused_bib))
    if missing_author_cites or missing_author_bib:
        failures.append(
            "Публікації здобувача не повністю пов’язані зі списком джерел: "
            f"не процитовано {missing_author_cites}; немає у bib {missing_author_bib}"
        )

    own_chapter_citation = re.compile(r"\\footnote\s*\{", re.I)
    for name in FORMULA_TEXTS:
        hits = line_hits(texts[name], own_chapter_citation)
        if hits:
            failures.append(
                f"Бібліографічні посилання або примітки у власному розділі {name}: "
                + " | ".join(hits)
            )

    forbidden_math = re.compile(
        r"\\mathcal|\\mathbb|\\mathfrak|\\vartheta|x\s*\^\s*\\star|"
        r"\\begin\{(?:aligned|cases|array|split)\}"
    )
    for name in FORMULA_TEXTS:
        hits = line_hits(texts[name], forbidden_math)
        if hits:
            failures.append(f"Заборонене математичне оформлення у {name}: " + " | ".join(hits))
        for equation in parse_equations(texts[name]):
            label = ",".join(equation["labels"]) or "без мітки"
            if not str(equation["last"]).endswith(","):
                failures.append(
                    f"{name}:{equation['line']} ({label}) — формула не завершується комою"
                )
            if not re.match(r"(?:\\noindent\s*)?де\s", str(equation["next"]), re.I):
                failures.append(
                    f"{name}:{equation['line']} ({label}) — пояснення не починається з «де »"
                )
            previous = str(equation["previous"])
            if not previous.endswith(":"):
                failures.append(
                    f"{name}:{equation['line']} ({label}) — вступне речення не завершується двокрапкою"
                )
            if equation["labels"] and not any(
                f"\\eqref{{{item}}}" in previous for item in equation["labels"]
            ):
                failures.append(
                    f"{name}:{equation['line']} ({label}) — вступне речення не називає номер формули"
                )

    placeholder_pattern = re.compile(
        r"TODO|FIXME|ПОТРІБНЕ ДЖЕРЕЛО|ВКАЗАТИ ЗНАЧЕННЯ|\\manualcheck",
        re.I,
    )
    for name, text in texts.items():
        if name == "preamble.tex":
            text = re.sub(r"\\newcommand\{\\manualcheck\}.*", "", text)
        hits = line_hits(text, placeholder_pattern)
        if hits:
            failures.append(f"Службові маркери у {name}: " + " | ".join(hits))

    hyphenated_web = re.compile(r"веб-(?:ресурс|систем|сервер)", re.I)
    terminology = re.compile(
        r"\b(?:контент\w*|плагін\w*|валідн\w*|модифікац\w*|метадан\w*|"
        r"інтерфейс\w*|конвертац\w*)",
        re.I,
    )
    misleading_physical_file = re.compile(r"\bфізичн\w*\s+(?:MP4[- ]*)?файл\w*", re.I)
    for name in CORE_TEXTS:
        for number, line in enumerate(texts[name].splitlines(), 1):
            if hyphenated_web.search(line):
                failures.append(f"{name}:{number} — нормативну форму вебресурс/вебсистема/вебсервер написано з дефісом")
            if terminology.search(line):
                failures.append(f"{name}:{number} — термін не відповідає SKILL v1.3: {line.strip()}")
            if misleading_physical_file.search(line):
                warnings.append(
                    f"{name}:{number} — контекстно перевірити словосполучення «фізичний файл»: {line.strip()}"
                )

    for name in ("abstract_uk.tex", "abstract_en.tex"):
        plain = tex_plain(texts[name])
        length = len(plain)
        if not 8000 <= length <= 12000:
            failures.append(f"{name}: обсяг анотації {length} знаків, очікується 8000–12000")
        keyword_match = re.search(r"(?:Ключові слова|Keywords):\}\s*([^\n]+)", texts[name], re.I)
        if not keyword_match:
            failures.append(f"{name}: не знайдено рядок ключових слів")
        else:
            keywords = [item.strip().rstrip(".") for item in keyword_match.group(1).split(",")]
            if not 5 <= len(keywords) <= 15:
                failures.append(f"{name}: {len(keywords)} ключових слів, очікується 5–15")
        stats.append(f"{name}: {length} знаків")

    tikz_paths = sorted(path for path in tex_paths if path.parent == ROOT / "figures_tex")
    drawio_paths = sorted((ROOT / "figures_drawio" / f"{path.stem}.drawio") for path in tikz_paths)
    drawio_stems = {path.stem for path in drawio_paths}
    tikz_stems = {path.stem for path in tikz_paths}
    if drawio_stems != tikz_stems:
        failures.append(
            f"Неповні пари рисунків: без Drawio {sorted(tikz_stems-drawio_stems)}; "
            f"без TikZ {sorted(drawio_stems-tikz_stems)}"
        )
    for path in drawio_paths:
        try:
            tree = ET.parse(path)
        except Exception as exc:
            failures.append(f"Некоректний XML {path.name}: {exc}")
            continue
        text = read(path)
        if "rounded=1" in text:
            failures.append(f"{path.name}: наявні заокруглені блоки")
        vertices = tree.findall(".//mxCell[@vertex='1']")
        content_blocks = [
            cell
            for cell in vertices
            if not cell.attrib.get("style", "").startswith("text;")
            and "shape=line" not in cell.attrib.get("style", "")
        ]
        if len(content_blocks) > 12:
            failures.append(f"{path.name}: {len(content_blocks)} змістових блоків, дозволено не більше 12")
        for cell in vertices:
            size = re.search(r"fontSize=(\d+(?:\.\d+)?)", cell.attrib.get("style", ""))
            if size and float(size.group(1)) < 9:
                failures.append(f"{path.name}: шрифт {size.group(1)} pt менший за 9 pt")
    for path in tikz_paths:
        text = read(path)
        if re.search(r"\\(?:scriptsize|tiny)\b", text):
            failures.append(f"{path.name}: використано надто дрібний шрифт")
        if forbidden_math.search(text):
            failures.append(f"{path.name}: наявне заборонене математичне оформлення")
        legacy_state = re.findall(r"\b(?:S_T|R_A)\b", text)
        if legacy_state:
            failures.append(
                f"{path.name}: застарілі позначення стану/запису {sorted(set(legacy_state))}"
            )

    publication_items = len(re.findall(r"\\item\b", read(ROOT / "publication_entries.tex")))
    if publication_items != 10:
        failures.append(f"У publication_entries.tex виявлено {publication_items} позицій замість 10")

    chapter_stats = []
    for name in ("intro.tex", "chapter_1.tex", "chapter_2.tex", "chapter_3.tex", "chapter_4.tex", "conclusions.tex"):
        text = texts[name]
        chapter_stats.append(
            (
                name,
                len(re.findall(r"[A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+(?:[-’'][A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+)*", tex_plain(text))),
                len(re.findall(r"\\begin\{equation\}", text)),
                len(re.findall(r"\\begin\{(?:table|longtable)\}", text)),
                len(re.findall(r"\\input\{figures_tex/", text)),
            )
        )
    stats.extend(
        [
            f"джерела/цитування: {len(bib_keys)}/{len(cite_keys)}",
            f"мітки/посилання: {len(labels)}/{len(refs)}",
            f"рисунки Drawio/TikZ: {len(drawio_paths)}/{len(tikz_paths)}",
            "файл | слів | формул | таблиць | рисунків",
        ]
    )
    stats.extend(f"{name} | {words} | {equations} | {tables} | {figures}" for name, words, equations, tables, figures in chapter_stats)

    report = [
        "# Звіт перевірки дисертаційного проєкту",
        "",
        "## Підсумок",
        "",
        f"- Критичні невідповідності: {len(failures)}.",
        f"- Контекстні попередження: {len(warnings)}.",
        "",
        "## Статистика",
        "",
    ]
    report.extend(f"- {item}" for item in stats)
    if failures:
        report.extend(["", "## Критичні невідповідності", ""])
        report.extend(f"- {item}" for item in failures)
    if warnings:
        report.extend(["", "## Контекстні попередження", ""])
        report.extend(f"- {item}" for item in warnings)
    (ROOT / "qa_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Критичні невідповідності: {len(failures)}")
    print(f"Контекстні попередження: {len(warnings)}")
    for item in failures[:30]:
        print("FAIL:", item)
    if len(failures) > 30:
        print(f"... ще {len(failures) - 30}; повний перелік у qa_report.md")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
