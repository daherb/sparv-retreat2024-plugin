"""Example for a custom annotator."""

from sparv.api import Annotation, Output, annotator, Text


@annotator("Convert every word to uppercase")
def uppercase(
    word: Annotation = Annotation("<token:word>"),
    out: Output = Output("<token>:sbx_retreat2024_plugin.sbx_uppercase.upper"),
    # some_config_variable: str = Config("sbx_uppercase.some_setting")
):
    """Convert to uppercase."""
    out.write([val.upper() for val in word.read()])


@annotator("Convert a complete sentence to uppercase using individual tokens")
def uppercase_sent_token(
    word: Annotation = Annotation("<token:word>"),
    sentence: Annotation = Annotation("<sentence>"),
    out: Output = Output("<sentence>:sbx_retreat2024_plugin.sbx_uppercase.upper_sent_token"),
):
    """Convert to uppercase."""
    words = list(word.read())
    output = []
    sentences, _ = sentence.get_children(word)
    for s in sentences:
        output.append(" ".join([words[i] for i in s]).upper())
    out.write(output)


@annotator("Convert a complete sentence to uppercase using the raw text data")
def uppercase_sent_text(
    text: Text = Text(),
    sentence: Annotation = Annotation("<sentence>"),
    out: Output = Output("<sentence>:sbx_retreat2024_plugin.sbx_uppercase.upper_sent_text"),
):
    """Convert to uppercase."""
    complete_text=list(text.read())
    sentence_bounds = list(sentence.read())
    output = []
    print(complete_text)
    for ((begin,), (end,)) in sentence_bounds:
        output.append(''.join(complete_text[begin:end]).upper())
    out.write(output)
