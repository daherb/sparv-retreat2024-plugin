"""Example for a custom annotator."""

from sparv.api import Annotation, Output, annotator, Text

@annotator("Count number of nouns per sentence")
def sentence_nouns(
    token_pos: Annotation = Annotation("<token:pos>"),
    sentence: Annotation = Annotation("<sentence>"),
    out: Output = Output("<sentence>:sbx_retreat2024_plugin.sbx_noun_count.nouncount"),
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
