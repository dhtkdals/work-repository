from flask import Flask, render_template, request
from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def scrape_data(text):
    change = quote(text, encoding="utf-8")
    url = "https://fallcent.com/product/search/?keyword=" + change

    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    html_class = soup.find_all(class_="small_product_div")
    result = ' '.join([tit.text.strip() for tit in html_class if tit])
    sign = list(result.split(" "))
    product = ' '.join(sign).split()
    pro = ' '.join(product)
    elements = pro.split('-')
    result_list = [re.split(r'\s*([-\d]+%)\s*', element) for element in elements]

    flat_list = [item for sublist in result_list for item in sublist]
    combined_data = [f"{flat_list[i - 1]} {flat_list[i]} {flat_list[i + 1]}" if '100%' in flat_list[i] else flat_list[i] for i in range(len(flat_list))]
    index_100 = [i for i, item in enumerate(combined_data) if '100%' in item]
    filtered_list = [combined_data[i] for i in range(len(combined_data)) if i not in [x - 1 for x in index_100] and i not in [x + 1 for x in index_100]]

    result_lines = []
    for line in filtered_list:
        if line.startswith(' '):
            result_lines.append(f'(-) {line.strip()}')
        else:
            result_lines.append(line)

    result = '\n'.join(result_lines)

    new_result = []
    i = 0
    while i < len(result):
        if result[i] == '%' and i < len(result) - 1 and result[i + 1] == '\n':
            new_result.append(result[i])
            new_result.append('↓ ')
            i += 1
        else:
            new_result.append(result[i])
        i += 1

    fin_result = ''.join(new_result)
    final = fin_result.split('\n')

    del final[0]

    i=1
    while i < len(final):
        if len(final[i]) < 15:
            final[i-1] += final[i]
            del final[i]
        else:
            i += 1

    result_list = []

    for item in final:
        match = re.search(r'(\d+%)[↓↑]?\s*([-+]?\d[\d,]*)원\s*(.*)', item)
        if match:
            discount = match.group(1).strip()
            price = match.group(2).strip()
            product = match.group(3).strip()
            result_list.append({'Discount': discount, 'Price': price, 'Product': product})

    return result_list

@app.route('/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        text = request.form.get('keyword', '')
        res_list = scrape_data(text)
        print("Received data in Flask:", res_list)  # 디버깅을 위해 데이터 출력
        return render_template('index.html', keyword=text, res_list=res_list)
    else:
        return render_template('index.html', keyword='', res_list=[])

if __name__ == '__main__':
    app.run(debug=True)




