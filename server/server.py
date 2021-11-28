import json
from functools import partial

from aiohttp import web
import aiofiles
import aiohttp_cors

from good import Good


routes = web.RouteTableDef()
rus_json_dumps = partial(json.dumps, ensure_ascii=False)


@routes.get('/goods')
async def good_list(request):
    limit = request.rel_url.query.get('limit', '')
    limit = int(limit) if limit.isdigit() else 0

    page = request.rel_url.query.get('page', '')
    page = int(page) if page.isdigit() else 1
    offset = limit * (page - 1)

    search_string = request.rel_url.query.get('search')

    result = await Good.get_list(search_string, limit, offset)
    count = await Good.get_count(search_string)
    return web.json_response({'result': result, 'count': count}, dumps=rus_json_dumps)


@routes.get(r'/goods/{id:\d+}')
async def good_read(request):
    good_id = int(request.match_info.get('id'))
    try:
        good = await Good.by_id(good_id)
    except IndexError:
        raise web.HTTPBadRequest(text=f'Товара с идентификатором {good_id} нет в БД')
    return web.json_response(good.to_json(), dumps=rus_json_dumps)


@routes.post('/goods')
async def good_create(request):
    good = Good()
    good.update(await request.json())
    return web.json_response({'id': await good.save()}, dumps=rus_json_dumps)


@routes.post(r'/goods/{id:\d+}')
async def good_update(request):
    good_id = int(request.match_info.get('id'))
    try:
        good = await Good.by_id(good_id)
    except IndexError:
        raise web.HTTPBadRequest(text=f'Товара с идентификатором {good_id} нет в БД')
    good.update(await request.json())
    await good.save()
    return web.json_response(good.to_json(), dumps=rus_json_dumps)


@routes.delete(r'/goods/{id:\d+}')
async def good_delete(request):
    good_id = int(request.match_info.get('id'))
    try:
        good = await Good.by_id(good_id)
    except IndexError:
        raise web.HTTPBadRequest(text=f'Товара с идентификатором {good_id} нет в БД')
    await good.delete()
    return web.json_response({'id': good_id}, dumps=rus_json_dumps)


@routes.get('/')
async def index(request):
    async with aiofiles.open('index.html', encoding='utf-8') as f:
        return web.Response(body=await f.read(), content_type='text/html')


if __name__ == '__main__':
    app = web.Application()

    routes.static('/script', 'static/script')
    routes.static('/css', 'static/css')
    app.add_routes(routes)

    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")})
    for route in app.router.routes():
        cors.add(route)

    web.run_app(app, host='127.0.0.1', port=8080)
