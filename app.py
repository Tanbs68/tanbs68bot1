from flask import Flask, request
from binance.client import Client
import os

app = Flask(__name__)

# 从环境变量读取币安 API 密钥
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
client = Client(api_key, api_secret)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json  # 接收 TradingView 的信号
        if not data or 'action' not in data:
            app.logger.error("Invalid data received: %s", data)
            return "Invalid data", 400

        if data['action'] == 'buy':
            order = client.create_order(
                symbol='BTCUSDT',
                side='BUY',
                type='MARKET',
                quantity=0.001  # 买入 0.001 BTC，可根据需要调整
            )
            app.logger.info("Buy order executed: %s", order)
        elif data['action'] == 'sell':
            order = client.create_order(
                symbol='BTCUSDT',
                side='SELL',
                type='MARKET',
                quantity=0.001  # 卖出 0.001 BTC
            )
            app.logger.info("Sell order executed: %s", order)
        return "Success", 200
    except Exception as e:
        app.logger.error("Error processing webhook: %s", str(e))
        return f"Error: {str(e)}", 500