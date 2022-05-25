from tools.credentials import Client
from telethon import events
from rules import Rule
import asyncio

class CopyApp():

    def __init__(self, source_channel, target_channels):
        self.source_channel = source_channel
        self.target_channels = target_channels

        # Messages to delete
        self.messages_to_delete = {}
        self.ids_to_delete_pool = {}
        # Setting rules
        for channel in self.target_channels:
            rule_name = self.target_channels[channel]['rule']
            self.target_channels[channel]['rule'] = Rule(rule_name)
            self.messages_to_delete[channel] = {}
            self.ids_to_delete_pool[channel] = []
        

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
                        self.messages_to_delete[channel][event.id] = message.id

        @Client.on(events.MessageDeleted(chats=[self.source_channel]))
        async def delete_messages(event):
            print(f'=== Excluindo mensagens IDs -> {event.deleted_ids} ===')
            for channel in self.messages_to_delete:
                for message_id in event.deleted_ids:
                    if message_id in self.messages_to_delete[channel]: 
                        await Client.delete_messages(channel, self.messages_to_delete[channel][message_id])
                        del self.messages_to_delete[channel][message_id]
                    # Tratando sincronização com mensagens ainda não inseridas
                    else:
                        self.ids_to_delete_pool[channel].append(message_id)
            
            
            await asyncio.sleep(30)
            # Clearing IDs not inserted in previous call
            for channel in self.ids_to_delete_pool:
                if len(self.ids_to_delete_pool[channel]) > 0:
                    for message_id in self.ids_to_delete_pool[channel]:
                        if message_id in self.messages_to_delete[channel]:
                            await Client.delete_messages(channel, self.messages_to_delete[channel][message_id])
                            del self.messages_to_delete[channel][message_id]
                            self.ids_to_delete_pool[channel].remove(message_id)
            
