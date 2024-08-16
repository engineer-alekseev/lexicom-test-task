##  Lexicom test task
### Part 1
### Инструкция по сборке
```bash
git clone <link to clone> <directory to clone to>
cd <directory to clone to>/part_one/contacts_api
make dev
```
Далее swagger API будет доступен на адресе http://127.0.0.1:8000/docs#


### Part 2

1. Вариант:
Используем для решения регулярное выражение
```sql
EXPLAIN ANALYZE
UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE sn.filename = regexp_replace(fn.filename, '\.[^.]+$', '');
```
2. Если гарантируется, что в названиях файлов точка содержится не более одного раза и только для отделения имени от расширения, то можно воспользоваться более простой функцией разбиения имени по делиметру

```sql
EXPLAIN ANALYZE
UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE fn.filename = sn.filename || '.' || SPLIT_PART(fn.filename, '.', 2);
```

3. Чтобы решение отработало еще эффективнее, можно добавить индексы на обе таблицы
```sql
CREATE INDEX idx_short_names_filename ON short_names (filename);
CREATE INDEX idx_full_names_filename ON full_names (filename);
```