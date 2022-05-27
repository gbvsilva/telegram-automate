from tools.credentials import Client
import asyncio
import roletas.copy_app
import tnt.copy_app
import tnt_crash.copy_app

# ROLETAS
roleta_milionaria_channel = -1001786393658
rei_das_roletas_vip_channel = -1001603226496
roleta_do_pix_free = -1001627787232
roleta_pix_vip_100 = -1001620654201
roletas_channels = {
    rei_das_roletas_vip_channel: {'name': 'REI DAS ROLETAS', 'rule': 'sem' },
    roleta_do_pix_free: {'name': 'ROLETA DO PIX FREE', 'rule': 'entre_8_14'},
    roleta_pix_vip_100: {'name': 'ROLETA DO PIX VIP 100%', 'rule': 'sem'}
}
roletas_copy_app = roletas.copy_app.CopyApp(roleta_milionaria_channel, roletas_channels)
# TNT
tnt_bot_channel = -1001661699351
pix_blaze_vip_channel = -1001575202712
tnt_channels = {pix_blaze_vip_channel: {'name': 'PIX BLAZE VIP', 'rule': 'sem' }}
tnt_copy_app = tnt.copy_app.CopyApp(tnt_bot_channel, tnt_channels)
# TNT CRASH
tnt_bot_crash_channel = -1001628576537
pix_blaze_24h_channel = -1001430369464
tnt_crash_channels = {pix_blaze_24h_channel: {'name': 'PIX BLAZE 24H', 'rule': 'sem'}}
tnt_crash_copy_app = tnt_crash.copy_app.CopyApp(tnt_bot_crash_channel, tnt_crash_channels)

async def Main():
    while True:
        await asyncio.sleep(1)
        await roletas_copy_app.clear_messages_to_delete()

with Client:
    Client.loop.run_until_complete(Main())
