from calendar import c
from tools.credentials import Client
from telethon import events
from rules import Rule


class CopyApp():

    def __init__(self, source_channel, target_channels):
        self.source_channel = source_channel
        self.target_channels = target_channels

        # Messages to delete
        self.msgs_to_delete_ids = {}
        self.msgs_to_delete_list = {}
        # Setting rules
        for channel in self.target_channels:
            rule_name = self.target_channels[channel]['rule']
            self.target_channels[channel]['rule'] = Rule(rule_name)
            self.msgs_to_delete_ids[channel] = {}
            self.msgs_to_delete_list[channel] = []

        @Client.on(events.NewMessage(chats=self.source_channel))
        async def new_message(event):
            print(f'=== Roletas Nova Mensagem ID -> {event.id} ===\n'+event.raw_text)
            if 'ANÁLISE CONFIRMADA' in event.raw_text or 'WIN' in event.raw_text or 'RED' in event.raw_text:
                for channel in self.target_channels:
                    ok = await self.target_channels[channel]['rule'].execute()
                    if ok:
                        message = await Client.send_message(channel, event.raw_text)
                        print(f"Mensagem enviada para {self.target_channels[channel]['name']} ID -> {message.id}")
            elif 'ANALISANDO' in event.raw_text or 'Fazer gale' in event.raw_text:
                for channel in self.target_channels:
                    ok = await self.target_channels[channel]['rule'].execute()
                    if ok:
                        message = await Client.send_message(channel, event.raw_text)
                        print(f"Mensagem enviada para {self.target_channels[channel]['name']} ID -> {message.id}")
                        self.msgs_to_delete_ids[channel][event.id] = message.id

        @Client.on(events.MessageDeleted(chats=[self.source_channel]))
        async def insert_into_del_list(event):
            print(f'=== Inserindo nas filas mensagens a serem excluídas IDs -> {event.deleted_ids} ===')
            for channel in self.target_channels:
                for message_id in event.deleted_ids:
                    self.msgs_to_delete_list[channel].append(message_id)
            

    async def clear_messages_to_delete(self):   
        # Clearing IDs in the list to delete
        for channel in self.target_channels:
            for message_id in self.msgs_to_delete_list[channel]:
                if message_id in self.msgs_to_delete_ids[channel]:
                    await Client.delete_messages(channel, self.msgs_to_delete_ids[channel][message_id])
                    del self.msgs_to_delete_ids[channel][message_id]
                    self.msgs_to_delete_list[channel].remove(message_id)
            
