import math
def eyebrow_left_first(value):
    if(value >= 10 and value < 20):
        return 55
    elif (value >= 20 and value < 30):
        return 75
    elif(value >= 30 and value < 40):
        return 100
    elif(value >=40 and value < 50):
        return 150
    elif(value >50):
        return 180
    else:
        return 0

def eyebrow_left_second(value):
    if(value >= 10 and value < 20):
        return 30
    elif (value >= 20 and value < 30):
        return 60
    elif(value >= 30 and value < 40):
        return 90
    elif(value >=40 and value < 50):
        return 120
    elif(value >50):
        return 150
    else:
        return 0

def eyebrow_right_first(value):
    if (value >= 10 and value < 20):
        return 45
    elif (value >= 20 and value < 30):
        return 60
    elif (value >= 30 and value < 40):
        return 75
    elif (value >= 40 and value < 50):
        return 90
    elif (value > 50):
        return 120
    else:
        return 0

def eyebrow_right_second(value):
    if(value >= 10 and value < 20):
        return 45
    elif (value >= 20 and value < 30):
        return 60
    elif(value >= 30 and value < 40):
        return 75
    elif(value >=40 and value < 50):
        return 90
    elif(value >50):
        return 120
    else:
        return 0

def lefteye_ball(value):
    if(value >=60 and value <= 90):
        return 90
    return 20 + int(2.8 * abs(value - 50))

def righteye_ball(value):
    if (value >= 70 and value <= 90):
        return 90
    return 20 + int(2.8 * abs(100 - value))

def lefteye(value):
    if(value > 20):
        return 0
    elif(value < 13):
        return 60
    else:
        return 0 + int(8.5 * (20 - value))

def righteye(value):
    if (value > 20):
        return 60
    elif (value < 13):
        return 0
    else:
        return 60 - int(6 * (20 - value))

def mouth(value):
    if(value < 10):
        return 0;
    elif(value >= 10 and value <20):
        return 1;
    elif(value >= 20 and value <30):
        return 2;
    elif (value > 30 and value <40):
        return 3;
    else:
        return 4;


