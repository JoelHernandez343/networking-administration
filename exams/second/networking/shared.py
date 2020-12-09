from networking.graph import Graph

username = "admin"
password = "admin"

topology = Graph()
visited = []

hostname = ""
pending = []


def log(message):
    print(f"[{hostname}] {message}")