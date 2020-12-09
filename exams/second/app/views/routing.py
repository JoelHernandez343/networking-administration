from database import models, manage


def build_routing(db):
    routes = [
        {"name": "Inicio", "route": "/"},
        {"name": "Topología", "route": "/topology"},
        {"name": "Routers", "route": "/routers"},
        {"name": "Acerca de", "route": "/about"},
    ]

    routers = []
    for router in manage.router.get_all(db):
        r = {
            "ip": router["ip_max"],
            "hostname": router["hostname"],
            "route": f"/routers/{router['ip_max']}",
        }

        interfaces = []
        for interface in router["interfaces"]:
            i = {
                "name": interface["name"],
                "route": f"{r['route']}/{interface['name']}",
            }
            interfaces.append(i)

        r["interfaces"] = interfaces

        routers.append(r)

    routes[2]["routers"] = routers

    return routes
