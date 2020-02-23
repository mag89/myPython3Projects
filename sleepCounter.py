from datetime import datetime, timedelta


def user_input():
    input_r_hours, input_r_minutes = None, None
    while not isinstance(input_r_hours, int) or input_r_hours < 0 or input_r_hours > 23:
        try:
            input_r_hours = int(input("часов(00-24): "))
        except ValueError:
            print("Это должно быть целое число от 00 до 24!")

    while not isinstance(input_r_minutes, int) or input_r_minutes < 0 or input_r_minutes > 59:
        try:
            input_r_minutes = int(input("минут(00-59): "))
        except ValueError:
            print("Это должно быть целое число от 00 до 59!")
    return input_r_hours, input_r_minutes


now = datetime.now()
print("Во сколько вы хотите встать завтра?")
user_ring = user_input()
ring = datetime(now.year, now.month, now.day + 1, user_ring[0], user_ring[1])

t = timedelta(hours=1, minutes=30)
delta = ring - now

print("Ваш будильник на завтра - {}.\n".format(ring.time()))
for i in range(1, delta//t + 1):
    sleep_time = ring - i * t
    if i * t >= timedelta(hours=6, minutes=00):
        print("Чтобы поспать {} - ложитесь в {}".format(i * t, sleep_time))
        print("До {} осталось {}\n".format(sleep_time.time(), sleep_time - now))
