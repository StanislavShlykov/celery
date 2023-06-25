from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   a = ['идиот', 'дура', 'мудак']
   text_list = value.split()
   for i in a:
      for j in range(len(text_list)):
         if i in text_list[j]:
            text_list[j] = text_list[j][0] + '*'*(len(text_list[j])-1)
   text = ' '.join(text_list)
   return text