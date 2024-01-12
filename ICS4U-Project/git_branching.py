

num = int(input("Enter an integer greater than 0: "))


for divider in range(1, num+1):
    print(f"divider variable is: {divider}.")
    

    if num % divider == 0:
        #we have a factor!
        print(f"{divider} is factor for {num}.")
        