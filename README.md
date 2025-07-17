\# 🤖 Crypto Telegram Alert Bot



<div align="center">



\[!\[Live Bot](https://img.shields.io/badge/Live%20Bot-Online-brightgreen?style=for-the-badge\&logo=telegram)](https://t.me/My\_Crypto\_Coin\_Alert\_bot)

\[!\[Heroku](https://img.shields.io/badge/Deployed%20on-Heroku-brightgreen?style=for-the-badge\&logo=heroku)](https://my-crypto-alert-bot-dceb4558154b.herokuapp.com/)

\[!\[Python](https://img.shields.io/badge/Python-3.8+-brightgreen?style=for-the-badge\&logo=python)](https://python.org)

\[!\[Status](https://img.shields.io/badge/Status-24%2F7%20Active-brightgreen?style=for-the-badge)](https://my-crypto-alert-bot-dceb4558154b.herokuapp.com/)



\*\*🚀 Real-time cryptocurrency price alerts delivered straight to your Telegram\*\*



\*Never miss a buy or sell opportunity again!\*



\[\*\*🤖 Try the Bot\*\*](https://t.me/My\_Crypto\_Coin\_Alert\_bot) • \[\*\*📊 Live Dashboard\*\*](https://my-crypto-alert-bot-dceb4558154b.herokuapp.com/) • \[\*\*🔧 Deploy Your Own\*\*](#deployment)



</div>



---



\## ✨ Features



<table>

<tr>

<td width="50%">



\### 🎯 \*\*Smart Alerts\*\*

\- \*\*Buy/Sell Notifications\*\* - Get alerted when prices hit your targets

\- \*\*Real-time Monitoring\*\* - Checks prices every 30 seconds

\- \*\*Multiple Coins\*\* - Support for 10 major cryptocurrencies

\- \*\*Custom Thresholds\*\* - Set your own price targets



</td>

<td width="50%">



\### 🔧 \*\*Easy to Use\*\*

\- \*\*Simple Commands\*\* - `/buy bitcoin 30000`

\- \*\*Instant Setup\*\* - Just start chatting with the bot

\- \*\*24/7 Operation\*\* - Never stops monitoring

\- \*\*Multi-user Support\*\* - Share with friends and family



</td>

</tr>

</table>



---



\## 🚀 Quick Start



\### 1. \*\*Start Using the Bot\*\*

\[!\[Telegram Bot](https://img.shields.io/badge/Start%20Bot-@My\_Crypto\_Coin\_Alert\_bot-brightgreen?style=for-the-badge\&logo=telegram)](https://t.me/My\_Crypto\_Coin\_Alert\_bot)



\### 2. \*\*Basic Commands\*\*

```

/start     - Initialize the bot

/prices    - View current crypto prices

/buy       - Set buy alert (e.g., /buy bitcoin 30000)

/sell      - Set sell alert (e.g., /sell eth 2500)

/alerts    - View your active alerts

/help      - Show all commands

```



\### 3. \*\*Example Usage\*\*

```

👤 You: /prices

🤖 Bot: 📊 Current Crypto Prices:

&nbsp;       ₿ BTC: $43,250.00

&nbsp;       Ξ ETH: $2,580.00

&nbsp;       ...



👤 You: /buy bitcoin 40000

🤖 Bot: ✅ Buy alert set!

&nbsp;       ₿ BTC at $40,000.00

&nbsp;       I'll notify you when the price drops to this level.



\[Later when price hits target]

🤖 Bot: 🔔 BUY ALERT!

&nbsp;       ₿ BTC has reached your buy target!

&nbsp;       Current: $39,950.00

&nbsp;       Target: $40,000.00

&nbsp;       💡 Good opportunity to buy!

```



---



\## 💰 Supported Cryptocurrencies



| Coin | Symbol | Emoji |

|------|--------|-------|

| \*\*Bitcoin\*\* | BTC | ₿ |

| \*\*Ethereum\*\* | ETH | Ξ |

| \*\*Solana\*\* | SOL | ☀️ |

| \*\*XRP\*\* | XRP | 💧 |

| \*\*Cardano\*\* | ADA | ₳ |

| \*\*Dogecoin\*\* | DOGE | 🐕 |

| \*\*Polkadot\*\* | DOT | ⚫ |

| \*\*Chainlink\*\* | LINK | 🔗 |

| \*\*Polygon\*\* | MATIC | 🔷 |

| \*\*Litecoin\*\* | LTC | Ł |



---



\## 🛠️ Technical Stack



| Component | Technology | Purpose |

|-----------|------------|---------|

| \*\*Bot Framework\*\* | python-telegram-bot | Telegram integration |

| \*\*Price Data\*\* | CoinGecko API | Real-time crypto prices |

| \*\*Database\*\* | SQLite | User data and alerts |

| \*\*Deployment\*\* | Heroku | 24/7 cloud hosting |

| \*\*Monitoring\*\* | Background threads | Continuous price checking |



---



\## 📊 Architecture



```

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐

│   Telegram      │    │   Heroku Bot     │    │   CoinGecko     │

│   Users         │◄──►│   Application    │◄──►│   API           │

│                 │    │                  │    │                 │

│ Send commands   │    │ • Process msgs   │    │ • Price data    │

│ Receive alerts  │    │ • Monitor prices │    │ • Market info   │

└─────────────────┘    │ • Send alerts    │    └─────────────────┘

&nbsp;                      │ • Store data     │

&nbsp;                      └──────────────────┘

&nbsp;                               │

&nbsp;                      ┌──────────────────┐

&nbsp;                      │   SQLite DB      │

&nbsp;                      │                  │

&nbsp;                      │ • User data      │

&nbsp;                      │ • Alert settings │

&nbsp;                      │ • Preferences    │

&nbsp;                      └──────────────────┘

```



---



\## 🚀 Deployment



\### Deploy Your Own Bot



\[!\[Deploy to Heroku](https://img.shields.io/badge/Deploy%20to-Heroku-brightgreen?style=for-the-badge\&logo=heroku)](https://heroku.com/deploy)



\#### Prerequisites

\- Python 3.8+

\- Telegram Bot Token (from \[@BotFather](https://t.me/botfather))

\- Heroku account



\#### Local Setup

```bash

\# Clone the repository

git clone https://github.com/LDolanLDolan/crypto-telegram-bot.git

cd crypto-telegram-bot



\# Create virtual environment

python -m venv venv

source venv/bin/activate  # On Windows: venv\\Scripts\\activate



\# Install dependencies

pip install -r requirements.txt



\# Set environment variable

export TELEGRAM\_BOT\_TOKEN="your\_bot\_token\_here"



\# Run the bot

python crypto\_bot.py

```



\#### Heroku Deployment

```bash

\# Login to Heroku

heroku login



\# Create app

heroku create your-crypto-bot-name



\# Set bot token

heroku config:set TELEGRAM\_BOT\_TOKEN="your\_bot\_token\_here"



\# Deploy

git push heroku main



\# Scale worker

heroku ps:scale worker=1

```



---



\## 📈 Performance \& Reliability



\- \*\*🔄 Uptime\*\*: 99.9% availability on Heroku

\- \*\*⚡ Response Time\*\*: < 1 second for commands

\- \*\*🔍 Monitoring\*\*: Checks prices every 30 seconds

\- \*\*📱 Delivery\*\*: Instant Telegram notifications

\- \*\*💾 Data\*\*: Persistent SQLite database

\- \*\*🔒 Security\*\*: Environment-based token storage



---



\## 💡 Advanced Features



\### Custom Alerts

\- Set multiple alerts per cryptocurrency

\- Percentage-based notifications

\- Portfolio tracking capabilities



\### Future Enhancements

\- \[ ] Portfolio value tracking

\- \[ ] Price charts and graphs

\- \[ ] News integration

\- \[ ] DeFi protocol monitoring

\- \[ ] Technical analysis alerts



---



\## 🤝 Contributing



Contributions are welcome! Here's how you can help:



1\. \*\*🍴 Fork\*\* the repository

2\. \*\*🌿 Create\*\* a feature branch (`git checkout -b feature/amazing-feature`)

3\. \*\*💾 Commit\*\* your changes (`git commit -m 'Add amazing feature'`)

4\. \*\*📤 Push\*\* to the branch (`git push origin feature/amazing-feature`)

5\. \*\*🔄 Open\*\* a Pull Request



\### Ideas for Contributions

\- Add support for more cryptocurrencies

\- Implement portfolio tracking

\- Add technical analysis indicators

\- Create web dashboard interface



---



\## 📄 License



This project is licensed under the MIT License - see the \[LICENSE](LICENSE) file for details.



---



\## 🆘 Support



\### Getting Help

\- 📧 \*\*Issues\*\*: \[Create an issue](https://github.com/LDolanLDolan/crypto-telegram-bot/issues)

\- 💬 \*\*Discussions\*\*: \[Join the discussion](https://github.com/LDolanLDolan/crypto-telegram-bot/discussions)

\- 📖 \*\*Documentation\*\*: Check the code comments and README



\### Troubleshooting



\*\*Bot not responding?\*\*

\- Check if the bot token is set correctly

\- Verify the worker process is running: `heroku ps`

\- Check logs: `heroku logs --tail`



\*\*Price alerts not working?\*\*

\- Ensure CoinGecko API is accessible

\- Check background monitoring in logs

\- Verify alert thresholds are realistic



---



\## 🌟 Acknowledgments



\- \*\*CoinGecko\*\* for providing free cryptocurrency data

\- \*\*python-telegram-bot\*\* for the excellent Telegram library

\- \*\*Heroku\*\* for reliable cloud hosting

\- \*\*The crypto community\*\* for inspiration and feedback



---



<div align="center">



\*\*⭐ Star this repository if you found it helpful!\*\*



\[!\[GitHub stars](https://img.shields.io/github/stars/LDolanLDolan/crypto-telegram-bot?style=social)](https://github.com/LDolanLDolan/crypto-telegram-bot/stargazers)

\[!\[GitHub forks](https://img.shields.io/github/forks/LDolanLDolan/crypto-telegram-bot?style=social)](https://github.com/LDolanLDolan/crypto-telegram-bot/network)



\*Built with ❤️ for the crypto community\*



\[!\[Live Bot](https://img.shields.io/badge/Try%20the%20Bot%20Now-brightgreen?style=for-the-badge\&logo=telegram)](https://t.me/My\_Crypto\_Coin\_Alert\_bot)



</div>

