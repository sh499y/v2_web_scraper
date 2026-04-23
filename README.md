# Scraper Web

Prosty program scraper + open ai do tworzenie profili firm na ppodstawie istniejacych stron interentowych
## Instalacja

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# lub
.venv\Scripts\activate  # Windows

pip install scrapy
```

## Uruchomienie

```bash
# Zapis do pliku
scrapy crawl cytaty_spider -o output.json
scrapy crawl cytaty_spider -o output.csv
```


## Korzystanie z programu
```
scrapy crawl content -a url=https://quotes.toscrape.com/page/2/
```