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
        self.text_filters = ['GREEN', 'LOSS', 'ENTRADA CONFIRMADA']

        @Client.on(events.NewMessage(chats=self.source_channel))
        async def new_message(event):
            print(f'=== TNT CRASH Nova Mensagem ID -> {event.id} ===\nTexto: '+event.message.text)
            if bool([text for text in self.text_filters if text in event.message.text]):
                for channel in self.target_channels:
                    ok = await self.target_channels[channel]['rule'].execute()
                    if ok:
                        if 'GREEN' in event.message.text:
                            event.message.text = '🟢🟢🟢 GREEN'
                        elif 'LOSS' in event.message.text:
                            event.message.text = '⚫️⚫️⚫️ LOSS'
                        else:
                            event.message.text = event.message.text.replace('✅', '').replace('💣', '⚠️')
                        message = await Client.send_message(channel, event.message)
                        print(f"Mensagem enviada para {self.target_channels[channel]['name']} ID -> {message.id}")

