# name = input()
# name2 = input()
# print(f"Привет {name} и {name2}")

# name=input("Введите имя: ")
# age=input("Введите свой возраст: ")
# subject=input("Введите свой любимый предмет в школе: ")
# print(f"Привет, меня зовут {name}. Мне {age} лет, и я очень люблю {subject}.")

# file = open('3 Day/Sample.txt', 'r')-считывание текста из файла
# data = file.read()
# print(data)
# file.close()

# file = open('3 Day/1.txt', 'w')-запись, с удалением старых записей
# file.write("Привет")
# file.close()

# file = open('3 Day/1.txt', 'a')-дозапись, без удаления старых записей
# file.write("1223566\n")
# file.write("Привет\n")
# file.close()

# name=input("Введите своё имя: ")
# surname=input("Введите свою фамилию: ")
# city=input("Введите свой город: ")
# file = open('3 Day/About.txt','w')
# file.write(name + "\n")
# file.write(surname + "\n")
# file.write(city + "\n")
# file.close()
# file = open('3 Day/About.txt', 'r')
# data = file.read()
# print(data)
# file.close()
# file = open('3 Day/About.txt','a')
# file.write("Мне нравится программирование")
# file.close()


# import csv
# with open("3 Day/Example.csv", encoding="utf-8") as r_file:
#     file_reader = csv.reader(r_file, delimiter = ";")
#     for i in file_reader:
#         print(i)

# mas=[1, 4, 5, 6, 7]
# # for i in mas:
# #     print(i, end=" ")
# # for i in range(len(mas)):
# #     print(mas[i], end=" ")
# # print(mas)
# # mas.clear()-очистка массива, удаление всех символов в массиве
# # print(mas)
# mas.append(10)#-добавление нового элемента в конец массива
# mas.remove(5)#-удаление элемента в массиве по его значению

# mas=[]
# for i in range(5, 16):
#     mas.append(i)
# print(mas)


# mas=[4, 10, 15, 23, 47, 17, 2]
# mas.remove(15)
# mas.remove(47)
# mas.append(31)
# for i in mas:
#     print(i, end=" ")

# import json
# with open("4 Day/Example.json", encoding='utf-8') as file:
#     data = json.load(file)
# print(data[0]["class"], data[0]["rating"])

# dict_one={
#     "orange": 100,
#     "apple": 40,
#     "pears": 30
# }
# print(dict_one["orange"])
# dict_one["orange"]=70
# print(dict_one["orange"])
# print(dict_one.values()) #вывод всех значенией
# print(dict_one.keys()) #вывод всех ключей


# dict_one={
#     "Maths": 4,
#     "IT": 5,
#     "Russian": 4
# }
# print(dict_one)
# dict_one["Maths"]=5
# dict_one["English"]=5
# print(dict_one)
