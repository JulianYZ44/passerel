# gateway_server.py (à héberger en ligne)
import asyncio
from aiohttp import web

tunnel_clients = {}  # id -> websocket

async def tunnel_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    client_id = request.query.get("id")
    if not client_id:
        await ws.close()
        return ws
    tunnel_clients[client_id] = ws
    print(f"[+] Tunnel ouvert: {client_id}")
    async for msg in ws:
        pass
    print(f"[-] Tunnel fermé: {client_id}")
    del tunnel_clients[client_id]
    return ws

async def proxy_handler(request):
    client_id = request.match_info['client_id']
    ws = tunnel_clients.get(client_id)
    if not ws:
        return web.Response(text="Client non connecté", status=503)

    data = {
        "method": request.method,
        "path": request.path_qs,
        "headers": dict(request.headers),
        "body": await request.read()
    }
    await ws.send_json(data)
    msg = await ws.receive_json()
    return web.Response(
        status=msg['status'],
        headers=msg['headers'],
        body=msg['body'].encode()
    )

app = web.Application()
app.router.add_get('/tunnel', tunnel_handler)
app.router.add_route('*', '/{client_id}/{tail:.*}', proxy_handler)

web.run_app(app, port=8080)
