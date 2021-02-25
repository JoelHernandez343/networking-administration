from networking.graph import Graph

username = "admin"
password = "admin"

topology = Graph()
visited = []

hostname = ""
pending = []
lan = 0


def log(message):
    print(f"[{hostname}] {message}")
