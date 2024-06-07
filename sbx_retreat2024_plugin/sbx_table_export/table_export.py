"""Example for a custom exporter."""

from sparv.api import Annotation, Export, Config, exporter
from typing import Optional

@exporter("Export annotations in a tabular format", config = [
    Config("sbx_retreat2024_plugin.table_export.lemma",
           description="Annotation in DEPREL field of CoNLL-U output")]
        )
def table_exporter(
    words: Annotation = Annotation("<token:word>"),
    lemmas: Optional[Annotation] = Annotation("[sbx_retreat2024_plugin.table_export.lemma]"),
        # Annotation("<token>:stanza.baseform"),
    sentence: Annotation = Annotation("<sentence>"),
    out : Export = Export("sbx_retreat2024_plugin.table_export/{file}.txt")):
    lines = []
    sent_id = 1
    sentences, _orphans = sentence.get_children(words)  # Ignore the orphans 😢
    words_list = list(words.read())
    has_lemmas = False
    if lemmas is not None:
        has_lemmas = True
        lemmas_list = list(lemmas.read())
    for s in sentences:
        lines.append("# sentence " + str(sent_id))
        sent_id += 1
        for t in s:
            line = words_list[t]
            if has_lemmas:
                line += "\t" + lemmas_list[t]
            lines.append(line)
    # Write result to file
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return
