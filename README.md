# Diplon
My diplom work to get data from ldap
to-do
- [ ] Получить пользователей
  - [ ] Базово получить пользователей
  - [ ] Получить пользователей в красивом виде
  - [ ] Добавить атрибуты пользователей
- [ ] Получить Компьютеры
- [ ] Получить Группы


```lua
s = box.schema.space.create('ald')
s:format({ {name = 'uid', type = 'string'}})
s:create_index('primary', { type = 'tree', parts = {'uid'}})
```