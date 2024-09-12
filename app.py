from flask import Flask,request,render_template,session
from packages import fetch
import yfinance as yf




TEMPLATES_AUTO_RELOAD = True
app = Flask(__name__)
app.secret_key = '8420208901'

@app.route('/' ,methods=['GET','POST'])
def hello():
    info={}
    if request.method=='POST':
        ticker=request.form['ticker']
        session['ticker']=ticker
        info=fetch.company_info(ticker)
        if 'companyOfficers' in info:
            del info['companyOfficers']
        return render_template('result.html',info=info)
    return render_template('home.html')


@app.route('/fundamental')
def funAnal():
    info={}
    ticker = session.get('ticker')
    if ticker:
        info=fetch.company_info(ticker)
        if 'companyOfficers' in info:
            del info['companyOfficers']
        return render_template('result.html',info=info)
    return render_template('home.html')


@app.route('/technical')
def techAnal():
    ticker = session.get('ticker')  # Retrieve the ticker from the session
    if ticker:
        plt_image=fetch.plot_closed_data(ticker)
        plt_dr_image=fetch.plot_daily_return(ticker)
        plt_dr_c=fetch.plt_daily_return_curve(ticker)
        plt_mv=fetch.plot_moving_average(ticker)
        return render_template('tech.html',ticker=ticker,plt_url=plt_image,plt_dailyreturn_image=plt_dr_image,plt_dr_curve=plt_dr_c,plt_mv=plt_mv)
    return render_template('tech.html')


@app.route('/ai',methods=['GET','POST'])
def aiAnal():
    if request.method == 'POST':
        open_value = float(request.form.get('open', 0))
        high = float(request.form.get('high', 0))
        low = float(request.form.get('low', 0))
        volume = float(request.form.get('volume', 0))
        prediction_method = request.form.get('dropdown')

        ticker = session.get('ticker')  # Retrieve the ticker from the session
        if ticker:
            closedPrice = fetch.linearRegressionModel(ticker, open_value, high, low, volume)
            print(closedPrice)
            print(ticker)
            return render_template('predict.html',closedPrice=closedPrice,ticker=ticker,open_value=open_value)
    return render_template('ai.html')

@app.route('/news')
def newsFun():
    ticker=yf.Ticker('NIFTY.NS')
    newsNifty=ticker.news
    return render_template('newspage.html',newsNifty=newsNifty)


@app.route('/about')
def aboutMe():
    return render_template('aboutme.html')


@app.route('/contact')
def contactUs():
    return render_template('contactus.html')