import requests


def fetch_leeds_corpus():
    r = requests.get("http://corpus.leeds.ac.uk/frqc/internet-jp-forms.num")
    return r.content


if __name__ == "__main__":
    resp = fetch_leeds_corpus()
    with open("../data/leeds_corpus.txt", "wb") as f:
        f.write(resp)
