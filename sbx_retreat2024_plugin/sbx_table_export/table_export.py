"""Example for a custom exporter."""

from sparv.api import Annotation, Export, ExportAnnotations, Config, exporter, get_logger
from typing import Optional


logger = get_logger(__name__)

@exporter("Export annotations in a tabular format", config = [
    Config("sbx_retreat2024_plugin.table_export.lemma",
           description="Annotation in DEPREL field of CoNLL-U output")]
        )
def table_exporter(
    words: Annotation = Annotation("<token:word>"),
    annotations : ExportAnnotations =  ExportAnnotations("export.annotations"),
    sentence: Annotation = Annotation("<sentence>"),
    out : Export = Export("sbx_retreat2024_plugin.table_export/{file}.txt")):
    lines = []
    sent_id = 1
    sentences, _orphans = sentence.get_children(words)  # Ignore the orphans 😢
    words_list = list(words.read())
    annotation_lists={a.name: list(a.read()) for (a,_) in annotations}
    for s in sentences:
        line = ["# sentence", str(sent_id)]
        line.extend([annotation_name + ":" + annotation_lists[annotation_name][sent_id-1] for annotation_name in annotation_lists if annotation_name.startswith("segment.sentence:")])
        lines.append(" ".join(line))
        lines.append("segment.token:word\t" + "\t".join([annotation_name for annotation_name in annotation_lists if annotation_name.startswith("segment.token:")]))
        sent_id += 1
        for t in s:
            line = []
            line.append(words_list[t])
            line.extend([annotation_lists[annotation_name][t] for annotation_name in annotation_lists if annotation_name.startswith("segment.token:")])
            lines.append("\t".join(line))
    # Write result to file
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return
