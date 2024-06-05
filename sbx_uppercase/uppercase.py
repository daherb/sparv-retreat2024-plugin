"""Example for a custom annotator."""

from sparv.api import Annotation, Output, annotator, Text


@annotator("Convert every word to uppercase")
def uppercase(
    word: Annotation = Annotation("<token:word>"),
    out: Output = Output("<token>:sbx_uppercase.upper"),
    # some_config_variable: str = Config("sbx_uppercase.some_setting")
):
    """Convert to uppercase."""
    out.write([val.upper() for val in word.read()])


#@annotator("Convert every word of a sentence to uppercase")
#def uppercase_sent(
#    word: Annotation = Annotation("<token:word>"),
#    sentence: Annotation = Annotation("<sentence>"),
#    out: Output = Output("<sentence>:sbx_uppercase.upper_sent"),
#    # some_config_variable: str = Config("sbx_uppercase.some_setting")
#):
#    """Convert to uppercase."""
#    words = list(word.read())
#    output = []
#    sentences, _ = sentence.get_children(word)
#    for s in sentences:
#        output.append(" ".join([words[i] for i in s]).upper())
#    out.write(output)


@annotator("Convert every word of a sentence to uppercase")
def uppercase_sent(
    text: Text = Text(),
#    text: Annotation = Annotation("<text>"),
    sentence: Annotation = Annotation("<sentence>"),
    out: Output = Output("<sentence>:sbx_uppercase.upper_sent"),
    # some_config_variable: str = Config("sbx_uppercase.some_setting")
):
    """Convert to uppercase."""
    complete_text=list(text.read())
    sentence_bounds = list(sentence.read())
    output = []
    print(complete_text)
    for ((begin,), (end,)) in sentence_bounds:
        output.append(''.join(complete_text[begin:end]).upper())
    out.write(output)
    
@annotator("Count number of nouns per sentence")
def sentence_nouns(
    token_pos: Annotation = Annotation("<token:pos>"),
    sentence: Annotation = Annotation("<sentence>"),
    out: Output = Output("<sentence>:sbx_uppercase.nouncount"),
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
