import json
import time
import requests
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Kafka setup
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'crypto-prices'

# CoinGecko API setup
COINGECKO_URL = 'https://api.coingecko.com/api/v3/coins/markets'
PARAMS = {
    'vs_currency': 'usd',
    'ids': (
        'bitcoin,ethereum,solana,cardano,ripple,dogecoin,polkadot,'
        'binancecoin,avalanche,chainlink,polygon,cosmos,uniswap,'
        'litecoin,stellar,vechain,shiba-inu,tron,tezos,neo'
    ),
    'order': 'market_cap_desc',
    'per_page': 20,
    'page': 1,
    'sparkline': 'false',
    'price_change_percentage': '24h'
}

desired_keys = [
    "id", "symbol", "current_price", "market_cap",
    "total_volume", "high_24h", "low_24h", "last_updated"
]

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retries=5,
    linger_ms=10
)

print("🚀 Crypto Kafka Producer started")

try:
    while True:
        try:
            response = requests.get(COINGECKO_URL, params=PARAMS, timeout=10)
            response.raise_for_status()

            data = response.json()
            filtered_data = [
                {key: coin.get(key) for key in desired_keys}
                for coin in data
            ]

            payload = {
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "data": filtered_data
            }

            producer.send(KAFKA_TOPIC, value=payload)
            print(f"📤 Sent {len(filtered_data)} records")

        except (requests.RequestException, KafkaError) as e:
            print(f"⚠️ Warning: {e}")

        time.sleep(30)

except KeyboardInterrupt:
    print("\n🛑 Producer stopped manually")

finally:
    producer.flush()
    producer.close()
