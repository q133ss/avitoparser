from bs4 import BeautifulSoup
import requests
import unidecode
import transliterate
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

class ParserApp(App):
    def build(self):
        #Менеджер окон
        self.sm = ScreenManager()
        
        #Первое окно
        main_screen = Screen(name='main')
        
        #Виджеты окна
        bl = BoxLayout(orientation='vertical')
        self.query = TextInput(hint_text='Запрос')
        bl.add_widget(self.query)
        self.city = TextInput(hint_text='Город')
        bl.add_widget(self.city)
        self.number = TextInput(hint_text='Кол-во объявлений')
        bl.add_widget(self.number)
        bl.add_widget(Button(text='Начать!', on_press=(self.parse)))
        
        #Добавляем виджеты к окну
        main_screen.add_widget(bl)

        #Второе окно
        done_screen = Screen(name='done')

        #Виджеты для второго окна
        done_layout = BoxLayout(orientation='vertical')
        done_layout.add_widget(Label(text='Объявления успешно спаршены! Они находяться в файле ads.csv'))
        done_layout.add_widget(Button(text='Назад', on_press=(self.back)))
        done_screen.add_widget(done_layout)

        #Добавляем окна в менеджер
        self.sm.add_widget(main_screen)
        self.sm.add_widget(done_screen)

        #Задаем изначальное окно
        self.sm.current = 'main'

        return self.sm


    def parse(self, instance):

        errors = [] #Список незаполненных полей

        if(self.query.text != ''):
            self.query.foreground_color = [.44,.44,.44,1]
            self.query.background_color = [1,1,1,1]
        else:
            self.query.background_color = [1,0,0,1]
            self.query.foreground_color = [1,1,1,1]
            errors.append('query')

        if(self.city.text != ''):
            self.city.foreground_color = [.44,.44,.44,1]
            self.city.background_color = [1,1,1,1]
        else:
            self.city.background_color = [1,0,0,1]
            self.city.foreground_color = [1,1,1,1]
            errors.append('city')

        if(self.number.text != ''):
            self.number.foreground_color = [.44,.44,.44,1]
            self.number.background_color = [1,1,1,1]
        else:
            self.number.background_color = [1,0,0,1]
            self.number.foreground_color = [1,1,1,1]
            errors.append('number')

        #Если все поля заполнены
        if(len(errors) == 0):
            url = 'https://www.avito.ru/'+transliterate.translit(self.city.text, reversed=True).lower()+'?q='+self.query.text
            request = requests.get(url)
            bs = BeautifulSoup(request.text, "html.parser")
            data = []

            for i in range(int(self.number.text)):
                link = bs.find_all('a', class_="iva-item-title-_qCwt")[i].get_text()
                price = bs.find_all('span', class_="price-text-E1Y7h")[i].get_text()
                price = unidecode.unidecode(price)
                description = bs.find_all('div', class_="iva-item-description-S2pXQ")[i].get_text()


                data.append([link, price, description])

            #открываем файл на запись
            with open('ads.csv', 'w', encoding='utf-8') as ouf:
            #перебираем элементы списка d
                for i in data:
                    #преобразуем элемент списка в строку
                    i=str(i)
                    #очищаем строку от ненужных символов
                    i=i.replace("\'", "")
                    i=i.replace("[", "")
                    i=i.replace("]", "")
                    #записываем строку в файл
                    ouf.write(i + '\n')

            #Меняем окно
            self.sm.transition.direction = "left"
            self.sm.current = "done"

    #Метод, который возвращает нас назад
    def back(self, instance):
        self.sm.transition.direction = "right"
        self.sm.current = 'main'



if __name__ == '__main__':
    ParserApp().run()