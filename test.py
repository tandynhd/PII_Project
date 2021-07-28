from datetime import datetime

now = datetime.now()
current_time = now.strftime("dmy%d%m%y-hms%H%M%S")
print(current_time)
("C:/Users/Tandin Dorji/Desktop/{0}".format(current_time))