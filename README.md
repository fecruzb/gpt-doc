## 1. Dependencies

- Install **Python 3**
- Install **Pip**


## 2. Install env
- pip install virtualenv

## 3. Create env

```bash
`python3 -m venv env
````

## Activate env

```bash
source env/bin/activate
``` 

```bash
.\env\Scripts\activate # windows
```

## Install dependencies

```
pip install -r requirements.txt
``` 

## Put any files inside docs/ they have these parsers

```
".pdf": PDFParser(),
".docx": DocxParser(),
".pptx": PptxParser(),
".jpg": ImageParser(),
".png": ImageParser(),
".jpeg": ImageParser(),
".mp3": VideoAudioParser(),
".mp4": VideoAudioParser(),
".csv": PandasCSVParser(),
".epub": EpubParser(),
".md": MarkdownParser(),
".mbox": MboxParser(),
```

## Start

```
python3 app.py
```