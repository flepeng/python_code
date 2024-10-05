import random
import test.get_web_url
columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

batch = 1000

for j in range(17, 0, -1):
    num = 0
    for i in range(batch):
        choice_set = set()
        while len(choice_set) < j:
            choice = random.choice(columns)
            choice_set.add(choice)
        # print(choice_set)
        if 1 in choice_set or 2 in choice_set or 3 in choice_set:
            num += 1
    print(num / batch)

ret = getattr(test.get_web_url, "soup")
print(ret)
