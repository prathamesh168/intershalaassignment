# from crypt import methods
# from urllib import request
from flask import Flask,redirect,url_for,render_template,request
import bs4
from bs4 import BeautifulSoup as bs
import requests
# { % ... % } for statements
# { { } } expressions to print output
# { # .... # } this is for internal comment

###  creates WSGI app
app = Flask(__name__)
#decorator url
@app.route('/')
def welcome():
    return "HELLO"

@app.route('/maths/<int:marks>')
def maths(marks):
    if marks<50:
        result = "fail"
    else:
        result="pass1"
    return redirect(url_for(result,score=marks))

@app.route('/pass1/<int:score>')
def pass1(score):
    return ("you are passed and your marks are " + str(score))

@app.route('/fail/<int:score>')
def fail(score):
    return ("you are failed and your marks are" + str(score))


@app.route('/submit')
def submit():
    return render_template('index.html')

@app.route('/result',methods=['POST','GET'])
def result():
    if(request.method == 'POST'):
        search_q = request.form['product name'].split()
        search_q = '+'.join(search_q)
        link = "https://www.flipkart.com/search?q="+search_q
        page = requests.get(link)
        g=  bs(page.content,'html.parser')
        if g.find('div',class_="_4rR01T").text != None or g.find('div',class_="_30jeq3").text != None or g.find('div',class_="_3I9_wc _27UcVY").text != None:
            name = g.find('div',class_="_4rR01T").text
            dis_price = g.find('div',class_="_30jeq3").text
            mrp_price = g.find('div',class_="_3I9_wc _27UcVY").text
            # print(dis_price)
        else:
            dis_price = "Product is not avialable on flipkart or check spelling"
        link1 = "https://www.amazon.in/s?k="+search_q
        
        HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36',
                                'Accept-Language': 'en-US, en;q=0.5'})
        
        webpage = requests.get(link1, headers=HEADERS)
        soup = bs(webpage.content, "lxml")
        if soup.find('span',class_="a-size-medium a-color-base a-text-normal").text or soup.find('span',class_="a-price").text != None or soup.find('span',class_="a-price a-text-price").text != None:
            name1 = soup.find('span',class_="a-size-medium a-color-base a-text-normal").text
            dis_price1 = soup.find('span',class_="a-price").text.split('₹')[1]
            mrp_price1 = soup.find('span',class_="a-price a-text-price").text.split('₹')[1]
        else:
            dis_price1= "Product is not avialable on amazon or check spelling "    
    return(render_template('results.html',amazon = dis_price1,flipkart=dis_price))


if __name__ == '__main__':
    app.run(debug=True)