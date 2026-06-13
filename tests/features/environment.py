import threading

from backend.server import create_server, context_store


def before_all(context):
    context.server = create_server(port=0)
    context.port = context.server.server_address[1]
    thread = threading.Thread(target=context.server.serve_forever, daemon=True)
    thread.start()


def before_scenario(context, scenario):
    # Reset shared context store between scenarios for isolation
    context_store._data.clear()


def after_all(context):
    context.server.shutdown()
    context.server.server_close()
