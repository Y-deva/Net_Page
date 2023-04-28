from random import randint
import sys
from sqlite3 import connect
con = connect('db/blogs.db', check_same_thread=False)
cur = con.cursor()
# print(st)
cl = False


# вывод
def print_field():
	file = open('log.txt', 'w')

	for cell in CELLS:

		# --------------------------------------------------↓ ГРАФИКА ↓-------------------------------------------------
		if cell in snake_body:
			print('' + 'X', end='', file=file)	   # змейка
		elif cell == apple_pos:
			print('' + 'a', end='', file=file)    # яблоко
		elif cell[1] in (0, FIELD_HEIGHT - 1) or cell[0] in (0, FIELD_WIDTH - 1):
			print('' + '#', end='', file=file)    # стены
		# --------------------------------------------------↑ ГРАФИКА ↑-------------------------------------------------

		else:
			print(' ', end='', file=file)

		if cell[0] == FIELD_WIDTH - 1:
			print('', file=file)
	file.close()
	file = open('log.txt').read()
	cur.execute(f'''Update games Set log="{file}"
	WHERE user_id={path}''')


# спавн яблока
def place_apple():
	col = randint(1, FIELD_WIDTH - 2)
	row = randint(1, FIELD_HEIGHT - 2)
	while (col, row) in snake_body:
		col = randint(1, FIELD_WIDTH - 2)
		row = randint(1, FIELD_HEIGHT - 2)
	return col, row


# съесть яблоко
def apple_collision():
	global apple_pos, eaten

	if snake_body[0] == apple_pos:
		apple_pos = place_apple()
		eaten = True


# обновление позиции змейки
def update_snake():
	global eaten
	new_head = snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]
	snake_body.insert(0, new_head)
	if not eaten:
		snake_body.pop(-1)
	eaten = False


# init(autoreset=True)


# -----------------------------------------------------↓ НАСТРОЙКИ ↓----------------------------------------------------
FIELD_WIDTH = 40
FIELD_HEIGHT = 20
CELLS = [(col, row) for row in range(FIELD_HEIGHT) for col in range(FIELD_WIDTH)]
snake_body = [
	(5, FIELD_HEIGHT // 2),
	(4, FIELD_HEIGHT // 2),
	(3, FIELD_HEIGHT // 2)]
DIRECTIONS = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
direction = DIRECTIONS['right']
eaten = False
apple_pos = place_apple()
# -----------------------------------------------------↑ НАСТРОЙКИ ↑----------------------------------------------------


# --------------------------------------------------------↓ ЗМЕЯ ↓------------------------------------------------------
path = sys.argv[1]
txt = cur.execute(f'''Select log2 FROM games
		WHERE user_id={path}''').fetchall()[0][0]
# print(txt)
exec(txt)
# --------------------------------------------------------↑ ЗМЕЯ ↑------------------------------------------------------

# чистое поле
# вывод поля
# update_snake()

# управление
# txt,_ = timedInput('', timeout=0.3)
txt = open('input.txt').readline().strip()
txt = cur.execute(f'''Select input FROM games
	WHERE user_id={path}''').fetchone()[0]
if True:
	if txt== 'w': direction = DIRECTIONS['up']
	elif txt== 'a': direction = DIRECTIONS['left']
	elif txt== 's': direction = DIRECTIONS['down']
	elif txt== 'd': direction = DIRECTIONS['right']
	elif txt== 'q':
		print_field()
		with open('log2.txt', 'w') as file:
			cur.execute(f'''Update games Set log2="{"""snake_body = [
				(5, FIELD_HEIGHT // 2),
				(4, FIELD_HEIGHT // 2),
				(3, FIELD_HEIGHT // 2)]
			DIRECTIONS = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
			direction = DIRECTIONS['right']
			eaten = False
			apple_pos = place_apple()"""}"
						WHERE user_id={path}''')
# 			print(
# '''snake_body = [
# 	(5, FIELD_HEIGHT // 2),
# 	(4, FIELD_HEIGHT // 2),
# 	(3, FIELD_HEIGHT // 2)]
# DIRECTIONS = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
# direction = DIRECTIONS['right']
# eaten = False
# apple_pos = place_apple()''', file=file)
			cl = True
# обновление состояний
update_snake()
apple_collision()
print_field()

# если умер
if snake_body[0][1] in (0, FIELD_HEIGHT - 1) or snake_body[0][0] in (0,FIELD_WIDTH - 1) or snake_body[0] in snake_body[1:]:
	print_field()
	with open('log2.txt', 'w') as file:
		cur.execute(f'''Update games Set log2="{"""snake_body = [
	(5, FIELD_HEIGHT // 2),
	(4, FIELD_HEIGHT // 2),
	(3, FIELD_HEIGHT // 2)]
DIRECTIONS = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
direction = DIRECTIONS['right']
eaten = False
apple_pos = place_apple()"""}"
			WHERE user_id={path}''')
# 		print(
# '''snake_body = [
# 	(5, FIELD_HEIGHT // 2),
# 	(4, FIELD_HEIGHT // 2),
# 	(3, FIELD_HEIGHT // 2)]
# DIRECTIONS = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
# direction = DIRECTIONS['right']
# eaten = False
# apple_pos = place_apple()''', file=file)
		cl = True
		print_field()
	with open('input.txt', 'w') as file:
		cur.execute(f'''Update games Set input='{'d'}'
			WHERE user_id={path}''')
		# print('d', file=file)

if not cl:
	with open('log2.txt', 'w') as file:
		cur.execute(f'''Update games Set log2="{f"""snake_body = {snake_body}
DIRECTIONS = {DIRECTIONS}
direction = {direction}
eaten = {eaten}
apple_pos = {apple_pos}"""}"
					WHERE user_id={path}''')
# 		print(
# f'''snake_body = {snake_body}
# DIRECTIONS = {DIRECTIONS}
# direction = {direction}
# eaten = {eaten}
# apple_pos = {apple_pos}''', file=file)
	txt = cur.execute(f'''Select log2 FROM games
		WHERE user_id={path}''').fetchone()[0]
	exec(txt)
	print_field()
con.commit()
