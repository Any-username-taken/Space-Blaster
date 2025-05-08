import time
import random


def wait_for(wait, maxWait):
    ran = random.randint(wait, maxWait)

    txt = [".", "..", "..."]
    pos = 0

    for i in range(ran):
        print(txt[pos], end="")
        time.sleep(random.randint(5, 10)/10)
        print("\b" * 3, end="", flush=True)
        if pos == 2:
            pos = 0
        else:
            pos += 1


def goFishing():
    print("Let's go fishing!")
    while True:
        ans = input("Do you want to cast your line?\n\n>")

        if ans.upper() == "YES":
            minim = random.randint(4, 6)
            maxim = random.randint(9, 20)

            wait_for(minim, maxim)
            print("PRESS ENTER!")
            start = time.time()
            input()
            end = time.time()

            total = end-start

            if total <= 1:
                print("You got a fish!")
            else:
                print("The fish swam away...")
                time.sleep(1)
                print("Don't take too long next time!")

            time.sleep(1)
            print(f"REACTION TIME: {total} seconds!")
            time.sleep(1)


goFishing()
