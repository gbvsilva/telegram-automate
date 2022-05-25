from tools.credentials import Client

async def print_dialogs():
    # You can print all the dialogs/conversations that you are part of:
    async for dialog in Client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

async def print_one_dialog(name):
    async for dialog in Client.iter_dialogs():
        if name in dialog.name:
            print(dialog.name, 'has ID', dialog.id)