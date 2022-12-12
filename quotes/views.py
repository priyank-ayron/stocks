from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm
import finnhub


def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker'].upper().strip()
        finnhub_client = finnhub.Client(api_key = "cebcm5qad3if3fbt6do0cebcm5qad3if3fbt6dog")
        try:
            api = finnhub_client.quote(ticker)
            resp = finnhub_client.company_profile2(symbol = ticker)
            api['name'] = resp['name']
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
            ticker = form.cleaned_data['ticker'].upper().strip()
            try:
                finnhub_client = finnhub.Client(api_key = "cebcm5qad3if3fbt6do0cebcm5qad3if3fbt6dog")
                api = finnhub_client.company_profile2(symbol = ticker)
                if len(api)==0:
                    raise Exception("There is some problem with your ticker symbol. Please try again.")
                form.save()
                messages.success(request, "Stock has been added.")
            except Exception as e:
                messages.success(request, "There is some problem with your ticker symbol. Please try again.")
                api = "Error"
            return redirect('add_stock')

    else:
        tickers = Stock.objects.all()
        output = []
        finnhub_client = finnhub.Client(api_key = "cebcm5qad3if3fbt6do0cebcm5qad3if3fbt6dog")
        for ticker in tickers:
            ticker = str(ticker)
            try:
                ticker = ticker.upper().strip()
                api = finnhub_client.quote(ticker)
                resp = finnhub_client.company_profile2(symbol = ticker)
                api['name'] = resp['name']
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
