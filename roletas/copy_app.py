import asyncio
from tools.credentials import Client
from telethon import events
from rules import Rule


class CopyApp():

    def __init__(self, source_channel, target_channels):
        self.source_channel = source_channel
        self.target_channels = target_channels

        # Messages to delete
        self.msgs_to_delete_list = {}
        # Setting rules
        for channel in self.target_channels:
            rule_name = self.target_channels[channel]['rule']
            self.target_channels[channel]['rule'] = Rule(rule_name)
            self.msgs_to_delete_list[channel] = []
        # Text Filters
        self.msg_to_delete_filters = ['ANALISANDO', 'Fazer gale']
        self.msg_to_maintain_filters = ['WIN', 'RED', 'ANÁLISE CONFIRMADA']
        self.msg_filters = self.msg_to_delete_filters + self.msg_to_maintain_filters

        @Client.on(events.NewMessage(chats=self.source_channel))
        async def new_message(event):
            print(f'=== Roletas Nova Mensagem ID -> {event.id} ===\n'+event.raw_text)
            if bool([text for text in self.msg_filters if text in event.raw_text]):
                for channel in self.target_channels:
                    ok = await self.target_channels[channel]['rule'].execute()
                    if ok:
                        message = await Client.send_message(channel, event.raw_text)
                        print(f"Mensagem enviada para {self.target_channels[channel]['name']} ID -> {message.id}")
                        if bool([text for text in self.msg_to_delete_filters if text in event.raw_text]):
                            self.msgs_to_delete_list[channel].append(message.id)
        
        # This method is not 100% reliable. Then, all messages with 'ANALISANDO' and 'Fazer gale' will be always cleared
        @Client.on(events.MessageDeleted(chats=[self.source_channel]))
        async def insert_into_del_list(event):
            print(f'=== Inserindo nas filas mensagens a serem excluídas IDs -> {event.deleted_ids} ===')
            for channel in self.target_channels:
                for message_id in event.deleted_ids:
                    if message_id not in self.msgs_to_delete_list[channel]:
                        self.msgs_to_delete_list[channel].append(message_id)
            

    async def clear_messages_to_delete(self):   
        # Clearing IDs in the list to delete
        await asyncio.sleep(60)
        print('=== Limpando cache de mensagens ===')
        for channel in self.target_channels:
            for message_id in self.msgs_to_delete_list[channel]:
                await Client.delete_messages(channel, message_id)
                self.msgs_to_delete_list[channel].remove(message_id)
