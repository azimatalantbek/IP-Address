from flask import Flask, render_template, request, jsonify
import ping3
import re

app = Flask(__name__)


def is_valid_ip(ip: str) -> bool:
    """Validate if the given IP address is in a correct format."""
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return ip_pattern.match(ip) is not None


def ping_ip(ip: str) -> bool:
    """Ping the given IP address and return True if reachable, False otherwise."""
    try:
        response = ping3.ping(ip, timeout=1)
        return response is not None
    except ping3.ping3.PingError:
        return False


@app.route("/")
def index():
    """Render the index page."""
    return render_template("index.html")


@app.route("/check_ips", methods=["POST"])
def check_ips():
    """Check the status of multiple IP addresses."""
    ip_addresses = request.form.get("ip_addresses", "").split()
    valid_ips = [ip for ip in ip_addresses if is_valid_ip(ip)]

    result = {}
    for ip in valid_ips:
        status = "works" if ping_ip(ip) else "doesn't work"
        result[ip] = status

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
