from datetime import datetime
a = ['идиот', 'дура', 'мудак']

# a = 'идиот'

b = 'Тут должен быть идиотский контент, а будет абракадабра, для проверки задания: Дурак, ываываываф идиот ыафыаываывфа мудак ываф ываф ывп фывп фвап фвп выа фывп фыва выа ыфвп выа фыв афвыа ывф.'
b = b.split()
for i in a:
    for j in range(len(b)):
        if i in b[j].lower():
            print('yes')
            b[j] = b[j][0]+'...'

# for i in b:
#     if a in i:
#         print(i[0]+'...')
text = ' '.join(b)
print(text)