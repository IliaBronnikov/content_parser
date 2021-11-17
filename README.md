# Парсер контента сайтов / режим для чтения
Программу, по переданному URL парсит веб-страницу, выделяет полезный контент и возвращает его в виде текста с шириной строки N символов.

## Возможности
- Работа в режиме скрипта, параметры передаются через опции командной строки, результат выводится в консоль и/или сохраняется в файл;
- Работа в режиме web, параметры передаются через query-параметры GET запроса, а результат возращается в формате .txt.

## Входные параметры
- URL страницы;
- ширина строки текста на выходе;
- сохранять ссылки на картинки в тексте или нет;
- сохранять результат в файл или нет (для режима скрипта).

## Входные параметры
Полезный контент со страницы в виде читаемого текста.

## Запуск проекта
- В режиме web: docker-compose up -d  
- В режиме терминала: docker exec parser python -m parser http://google.com 80


