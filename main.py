import time

running = True
seconds = 10
end = 0

while running:
    print(seconds)
    time.sleep(1)
    seconds = seconds - 1
    if seconds < end:
        running = False
print("Done!!!")