from bs4 import BeautifulSoup
import requests
import unidecode
import transliterate

def main():
    product = input("Ваш запрос: ")
    city = input('Город:')
    count = input("Сколько товаров спарсить?: ")

    url = 'https://www.avito.ru/'+transliterate.translit(city, reversed=True).lower()+'?q='+product

    request = requests.get(url)
    bs = BeautifulSoup(request.text, "html.parser")

    data = []

    # all_links = bs.find_all("a", class_="iva-item-title-_qCwt")

    # iva-item-root-Nj_hb

    # for link in all_links:
    # 	print("https://www.avito.ru"+ link["href"])
    print(url)

    for i in range(int(count)):
    	link = bs.find_all('a', class_="iva-item-title-_qCwt")[i].get_text()
    	price = bs.find_all('span', class_="price-text-E1Y7h")[i].get_text()
    	price = unidecode.unidecode(price)
    	description = bs.find_all('div', class_="iva-item-description-S2pXQ")[i].get_text()


    	data.append([link, price, description])


    #print(data)


    #открываем файл на запись
    with open('products.csv', 'w') as ouf:
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

if(__name__ == "__main__"):
    main()