vals = [True, False]

count1 = 0
count2 = 0
count3 = 0

def implies (x, y):
    return (not x) or y

for A in vals:
    for B in vals:
        for C in vals:
            for D in vals:
                if (not (A and B)) or ((not B) and C):
                    count1 += 1
                if implies((not A) or B, C):
                    count2 += 1
                if (A or (not B)) and implies(not B, not C) and (not implies(D, not A)):
                    count3 += 1

print("Count1: ", count1)
print("Count2: ", count2)
print("Count3: ", count3)
