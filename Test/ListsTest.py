myList = [1,2,3,4,5,6,7,8,9]
print myList
popped = myList.pop()
print("The popped value is: " + str(popped))
print("The list after pop operation: ")
for ele in myList:
    print ele
    
pushed = 999
myList.append(pushed)

print("The pushed value is: " + str(pushed))
print("The list after append (push) operation: ")
for ele in myList:
    print ele
    
"""
Double Lists
"""
print('\n\nTesting list of lists!..........')
nameList = ['Art', 'Oli','dorthy']
ageList = [32,21,25]
guestList = [nameList, ageList]
print('Guest List:')
for guest in guestList:
    print guest[1]


print('\n\nTesting list of appended !..........')
nameList = ['Art', 'Oli','dorthy']
ageList = [32,21,25]
Hyp =[]
Score = []
for currentModel in range(0,4):
    H = []
    S = []
    for i in range(0,3):
        H.append(nameList[i])
        S.append(ageList[i])
    Hyp.append(H)
    Score.append(S)
print('Name List:')
print Score
