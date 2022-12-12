from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm
import requests
import json


def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_req = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_62f1e6b0a3874cde8a3c9873241088f7".format(ticker))
        try:
            api = json.loads(api_req.content)
        except Exception as e:
            api = "Error"
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': 'Enter a ticker symbol above...'})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added.")
            return redirect('add_stock')
    else:
        tickers = Stock.objects.all()
        output = []
        for ticker in tickers:
            api_req = requests.get(
                "https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_62f1e6b0a3874cde8a3c9873241088f7".format(str(ticker)))
            try:
                api = json.loads(api_req.content)
                output.append(api)
            except Exception as e:
                api = "Error"
        return render(request, 'add_stock.html', {'ticker': tickers, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, 'Stock has been deleted.')
    return redirect(delete_stock)


def delete_stock(request):
    tickers = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': tickers})
