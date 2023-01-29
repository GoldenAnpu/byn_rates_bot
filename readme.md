<div align="center">
<!-- Title: -->
    <h2>Exchange rates infoBOT</h2>
</div>

### This is an unofficial bot❗

Bot provides official exchange rates for currencies from National Bank of the Republic of Belarus. The information provided here is not directly from NBRB. The author cannot be held responsible for any financial problems that may result from improper use of the information.

<a href="https://t.me/BY_Rates_bot"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/240px-Telegram_logo.svg.png" height="16" alt="Telegram"> Try it here</a>

### How it works
The service operates within the EU, so it is not possible to obtain information directly from the official site as all requests are blocked. Therefore, information is gathered from a site that can be accessed, which in turn retrieves the data directly from the NBRB site. The information is collected once between rate changes during the first request of the period. There is no need to constantly retrieve fresh data as the exchange rate changes occur at a specific time. Additionally, it makes sense to reduce the number of requests to the site to avoid losing access.

### For whom it needs
For people who are outside Belarus but have financial dealings within the country and only need information about exchange rates.

### Technical information
 - Developed using python-telegram-bot
 - Deployed on VPS Linode with Ubuntu 22.10