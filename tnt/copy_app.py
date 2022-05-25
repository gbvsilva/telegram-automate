from tools.credentials import Client
from telethon import events
from rules import Rule

class CopyApp():

    def __init__(self, source_channel, target_channels):
        self.source_channel = source_channel
        self.target_channels = target_channels

        # Setting rules
        for channel in self.target_channels:
            rule_name = self.target_channels[channel]['rule']
            self.target_channels[channel]['rule'] = Rule(rule_name)

        self.text_filters = ['Parcial', 'SINAL CONFIRMADO']

        self.stickers = {
            5148131741549986716: '🟢🟢🟢 GREEN',
            5147702558352998878: '⚪️⚪️⚪️ WHITE',
            5145797680227680975: '🔴🔴🔴 RED'}

        @Client.on(events.NewMessage(chats=self.source_channel))
        async def new_message(event):
            print(f'=== TNT Nova Mensagem ID -> {event.id} ===\nTexto: '+event.message.text)
            if bool([text for text in self.text_filters if text in event.message.text]):
                for channel in self.target_channels:
                    ok = await self.target_channels[channel]['rule'].execute()
                    if ok:
                        new_msg = event.message.text
                        if 'SINAL CONFIRMADO' in new_msg:
                            new_msg = '⚠️ '+new_msg.replace('✅', '').replace('🧨','\n•').\
                                        replace('💣', '\n•')
                        message = await Client.send_message(channel, new_msg)
                        print(f"Mensagem enviada para {self.target_channels[channel]['name']} ID -> {message.id}")
            else:
                try:
                    sticker_id = event.message.sticker.id
                    if sticker_id in self.stickers:
                        print(self.stickers[sticker_id])
                        for channel in self.target_channels:
                            ok = await self.target_channels[channel]['rule'].execute()
                            if ok:
                                message = await Client.send_message(channel, self.stickers[sticker_id])
                                print(f"Mensagem enviada para {self.target_channels[channel]['name']} ID -> {message.id}")
                except:
                    pass

