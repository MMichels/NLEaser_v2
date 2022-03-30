from wordcloud import WordCloud
from nltk import download
from nltk.corpus import stopwords


download("stopwords")


def generate_wordcloud(sentences, language) -> WordCloud:
    """
    Gera um objeto "wordcloud" ja preenchido

    :param sentences: lista de sentenças para gerar o wordcloud
    :param language: idioma das sentenças
    :return: WordCloud gerado a partir das sentenças
    """
    stop_wds = stopwords.words(language)
    text = ' '.join(sentences)
    wcloud = WordCloud(stopwords=stop_wds, collocations=True,
                       margin=4, max_words=75,
                       width=1968, height=1080, background_color="white", colormap="Set1")
    wcloud.generate_from_text(text)
    return wcloud
