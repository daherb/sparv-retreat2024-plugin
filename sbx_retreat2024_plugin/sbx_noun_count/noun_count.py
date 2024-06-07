"""Example for a custom annotator."""

from sparv.api import Annotation, Output, annotator, Text

@annotator("Count number of nouns per sentence")
def sentence_nouns(
    token_pos: Annotation = Annotation("<token:pos>"),
    sentence: Annotation = Annotation("<sentence>"),
    out: Output = Output("<sentence>:sbx_retreat2024_plugin.noun_count_sent"),
):
    """Annotate sentences with number of nouns per sentence."""
    sentences, _orphans = sentence.get_children(token_pos)  # Ignore the orphans 😢
    pos_list = list(token_pos.read())  # Convert iterator to a list to access the tokens by index
    output = []  # Resulting annotation values, one per sentence

    # Count the nouns per sentence
    count = 0
    for s in sentences:
        for w in s:
            print(pos_list[w])
            # Do something with pos_list[w] here
            if pos_list[w] == "NN":
                count += 1
        output.append(str(count))  # Append count to result
    out.write(output)

@annotator("Count number of nouns per text")
def text_nouns(
    text: Annotation = Annotation("<text>"),
    sentence_noun_counts: Annotation = Annotation("<sentence>:sbx_retreat2024_plugin.noun_count_sent"),
    out: Output = Output("<text>:sbx_retreat2024_plugin.noun_count_text"),
):
    """Annotate texts with number of nouns in all sentences."""
    output = []  # Resulting annotation values, one per sentence
    counts_list = list(sentence_noun_counts.read())
    texts, _orphans = text.get_children(sentence_noun_counts)
    for t in texts:
        count = 0
        for c in t:
            count += int(counts_list[c])
        output.append(str(count))
    out.write(output)
