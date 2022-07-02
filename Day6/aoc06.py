# Advent of Code Day 6 - Lanternfish 


def simplePopulationCalc(fishList,days):
    for day in range(days):
        for f in range(len(fishList)):
            if fishList[f] == 0:
                fishList.append(8)
                fishList[f] = 6
            else:
                fishList[f] -= 1
    return len(fishList) 

def cleverPopulationCalc(ageList,days):
    for _ in range(days):
        ageList[7] += ageList[0]
        ageList.append(ageList.pop(0))
    return sum(ageList)



if __name__ == "__main__":

    lanternFish = []
    filename = input("Enter the file containing the vent data: ")
    with open(filename) as file_object:
        for line in file_object:
            lanternFish = file_object.readlines()
    # to get this input to work, again there had to be a blank leading line, why?

    lanternFish = lanternFish[0].split(",")
    lanternFish = [int(fish) for fish in lanternFish]

    days = 256    
    #print(f"Number of fish after {days} days is {simplePopulationCalc(lanternFish,days)}")

    # Count the number of fish by age, then total fish is sum across all ages
    fishAges = [0,0,0,0,0,0,0,0,0]
    for fish in lanternFish:
        fishAges[fish] += 1

    print(f"Function returns {cleverPopulationCalc(fishAges,days)}")