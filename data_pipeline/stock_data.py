import yfinance as yf

stocks = [
    # IT
    "TCS.NS","INFY.NS","WIPRO.NS","HCLTECH.NS","TECHM.NS","LTIM.NS","MPHASIS.NS","PERSISTENT.NS",

    # Banking & Finance
    "HDFCBANK.NS","ICICIBANK.NS","KOTAKBANK.NS","SBIN.NS","AXISBANK.NS",
    "BAJFINANCE.NS","BAJAJFINSV.NS","HDFCLIFE.NS","SBILIFE.NS","ICICIPRULI.NS",

    # Energy & Oil
    "RELIANCE.NS","ONGC.NS","IOC.NS","BPCL.NS","HPCL.NS","GAIL.NS","ADANIGREEN.NS","ADANITRANS.NS",

    # FMCG
    "HINDUNILVR.NS","ITC.NS","NESTLEIND.NS","DABUR.NS","BRITANNIA.NS","MARICO.NS","COLPAL.NS","GODREJCP.NS",

    # Auto
    "MARUTI.NS","TATAMOTORS.NS","M&M.NS","BAJAJ-AUTO.NS","EICHERMOT.NS","HEROMOTOCO.NS","TVSMOTOR.NS",

    # Pharma
    "SUNPHARMA.NS","DRREDDY.NS","CIPLA.NS","DIVISLAB.NS","LUPIN.NS","AUROPHARMA.NS","ALKEM.NS","TORNTPHARM.NS",

    # Metals
    "TATASTEEL.NS","JSWSTEEL.NS","HINDALCO.NS","VEDL.NS","SAIL.NS","NMDC.NS","JINDALSTEL.NS",

    # Cement
    "ULTRACEMCO.NS","SHREECEM.NS","ACC.NS","AMBUJACEM.NS","DALBHARAT.NS","RAMCOCEM.NS",

    # Infrastructure & Capital Goods
    "LT.NS","SIEMENS.NS","ABB.NS","BHEL.NS","CUMMINSIND.NS","HAVELLS.NS","POLYCAB.NS",

    # Retail & Consumer
    "DMART.NS","TRENT.NS","VBL.NS","PAGEIND.NS","ZOMATO.NS","NYKAA.NS",

    # Telecom
    "BHARTIARTL.NS","IDEA.NS",

    # Chemicals
    "PIDILITIND.NS","SRF.NS","DEEPAKNTR.NS","AARTIIND.NS","UPL.NS",

    # Power
    "NTPC.NS","POWERGRID.NS","TATAPOWER.NS","ADANIPOWER.NS",

    # Mid & Small Caps (diversification)
    "IRCTC.NS","COFORGE.NS","INDIAMART.NS","LALPATHLAB.NS","METROPOLIS.NS",
    "ASTRAL.NS","CROMPTON.NS","DIXON.NS","ROUTE.NS","TANLA.NS",

    # PSU & Others
    "HAL.NS","BEL.NS","RVNL.NS","IRFC.NS","CONCOR.NS","NBCC.NS",

    # Extra to reach 150+
    "BANKBARODA.NS","PNB.NS","CANBK.NS","IDFCFIRSTB.NS","FEDERALBNK.NS",
    "BANDHANBNK.NS","INDUSINDBK.NS","YESBANK.NS","RBLBANK.NS",

    "ADANIENT.NS","ADANIPORTS.NS","ATGL.NS","ADANIWILMAR.NS",

    "JSWENERGY.NS","NHPC.NS","SJVN.NS","RECLTD.NS","PFC.NS",

    "UBL.NS","RADICO.NS","MCDOWELL-N.NS",

    "BIOCON.NS","ZYDUSLIFE.NS","GLENMARK.NS",

    "APOLLOHOSP.NS","FORTIS.NS","MAXHEALTH.NS",

    "ESCORTS.NS","ASHOKLEY.NS",

    "SUPREMEIND.NS","KEI.NS","FINOLEXCABLES.NS",

    "GRASIM.NS","BERGEPAINT.NS","ASIANPAINT.NS",

    "HINDZINC.NS","NATIONALUM.NS",

    "LTTS.NS","CYIENT.NS",

    "BOSCHLTD.NS","MOTHERSUMI.NS",

    "IDBI.NS","UCOBANK.NS",

    "CESC.NS","TORNTPOWER.NS",

    "AUBANK.NS","CHOLAFIN.NS"
]

def get_stock_data():
    all_data = []

    for ticker in stocks:
        stock = yf.Ticker(ticker)
        info = stock.info

        data = {
    "stock": info.get("shortName"),
    "symbol": ticker,
    "sector": info.get("sector"),

    "marketCap": info.get("marketCap"),
    "pe": info.get("trailingPE"),

    "revenueGrowth": info.get("revenueGrowth"),
    "returnOnEquity": info.get("returnOnEquity"),

    "debtToEquity": info.get("debtToEquity"),
    "dividendYield": info.get("dividendYield"),

    "beta": info.get("beta")   
}

        all_data.append(data)

    return all_data
if __name__ == "__main__":
    print(get_stock_data())