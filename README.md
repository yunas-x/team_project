### Plan loader

#### Использование

Установка зависимостей:

```
pip install -r plan_loader/requirements.txt
```

Запуск:

```
python plan_loader -m [PLAN_TYPE] -d [DESTINATION_FOLDER_PATH]
```

По умолчанию загружает рабочие планы НИУ ВШЭ на рабочий стол
Возможные значения PLAN_TYPE см. в **plan_loader/enums.py**

### Parser

#### Использование

Установка зависимостей:

```
pip install -r src/requirements.txt
```

На данный момент не реализован вызов с аргументами, поэтому рекомендуется запускать вручную, предварительно настроив **src/\_\_main\_\_.py**

#### Документация

В модуле **src/parsers/\_\_init.py\_\_** реализованы высокоуровневые методы для запуска парсинга и валидации с возможностью вызова в многопроцессном режиме (если в количество процессов передано число больше 1). Обрабатывают все файлы, находящиеся в указанной папке.

В качестве аргумента также используется протокол парсера, определенный в **src/parsers/core/protocols/ParserProtocol.py**. Конкретные реализации протокола см. в следующих модулях:
- **src/parsers/hse/annual/AnnualParser.py** - парсинг рабочего плана НИУ ВШЭ из файла
- **src/parsers/hse/annual/AnnualParserByLink.py** - парсинг рабочего плана НИУ ВШЭ по ссылке
- **src/parsers/hse/basic/BasicParser.py** - парсинг базового плана НИУ ВШЭ из файла
- **src/parsers/hse/basic/BasicParserByLink.py** - парсинг базового плана НИУ ВШЭ по ссылке
- **src/parsers/itmo/ItmoParser.py** - парсинг учебного плана ИТМО из файла

В каждом парсере две части: парсинг текста с титульного листа и парсинг табличной части с дисциплинами. Чтобы извлечь соответствующие данные из pdf в модуле **src/parsers/core/utils/converters.py** реализованы следующие методы:
- **get_pdf_page_text** - получение списка строк с определенного листа (см. Exctracting text https://pypi.org/project/pdfplumber/). Важно правильно подобрать настройки, иначе между словами могут пропадать пробелы или раздельные строки начнут объединяться в одну.
- **convert_pdf_to_data_frame** - получение табличной части в виде pandas dataframe (см. Exctracting tables https://pypi.org/project/pdfplumber/)
- **convert_pdf_to_data_frame_with_row_colors** - получение таблиной части в виде pandas dataframe, но при этом в последнем столбце содержится цвет строки или None если цвета нет (цвет нужен для распознания иерархии дисциплин). В pdfplumber'е нет встроенной возможности получать цвета строк таблицы, поэтому код соотносит положение на листе строки таблицы с положением раскрашенных прямоугольников (rect - базовый элемент pdf файла). !!!Тестировалось только на уч. планах ИТМО!!!

Как конкретно список строк и датафрейм должны обрабатываться зависит от учебного плана. Важно помнить, что иногда учебные планы по какой-то причине имеют отличающуюся структуру или ошибки, из-за этого отдельные части кода могут быть реализованы менее эффективно, чтобы обработать большее количество кейсов