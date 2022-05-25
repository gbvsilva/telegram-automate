from tools.credentials import Client
from telethon import events

class ScheduledPost():
    def __init__(self, source_channel, target_channels):
        self.source_channel = source_channel
        self.target_channels = target_channels
        self.index = 0
        self.posts = {0: 'Bom dia'}

        @Client.on(events.NewMessage(chats=self.source_channel))
        async def new_message(event):
            print(f'=== Novo Post: ID -> {event.id} ===\n')
            self.posts[event.id] = event

        @Client.on(events.MessageDeleted(chats=self.source_channel))
        async def clear_messages(event):
            print(f'=== Limpando o apanhado de posts ===')
            self.posts = {}
    
    async def send_message(self):
        if len(self.posts) > 0:
            event = self.posts[self.index]
            for channel in self.target_channels:    
                message = await Client.send_message(channel, event.message)
                print(f"Mensagem enviada para {self.target_channels[channel]['name']}: ID -> {message.id}")
