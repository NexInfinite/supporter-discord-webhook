import flask
import json
import requests
from flask import Flask
app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    webhook_id = flask.request.args.get("webhook_id")
    webhook_auth = flask.request.args.get("webhook_auth")

    color = flask.request.args.get("color")
    if color is None:
        color = 222934

    data = json.loads(flask.request.data.decode())
    try:
        if data["action"] == "created":
            sponsorship = data["sponsorship"]
            tier_description = sponsorship["tier"]["description"]
            username = sponsorship["sponsor"]["login"]
            price_in_dollars = int(sponsorship["tier"]["monthly_price_in_cents"])/100
            supporter_url_html = sponsorship["sponsor"]["html_url"]
            supporter_icon = sponsorship["sponsor"]["avatar_url"]
            webhook_send_json = {
              "embeds": [
                {
                  "description": f"{tier_description}",
                  "color": color,
                  "author": {
                    "name": f"{username} just sponsored for ${price_in_dollars}",
                    "url": f"{supporter_url_html}",
                    "icon_url": f"{supporter_icon}"
                  },
                  "footer": {
                    "text": "Thank you for supporting me, it really helps out"
                  }
                }
              ]
            }
            requests.post(f"https://discord.com/api/webhooks/{webhook_id}/{webhook_auth}", json=webhook_send_json)
            return "Run!"
    except IndexError as e:
        return e


if __name__ == "__main__":
    app.run(host="localhost", port="7182")
