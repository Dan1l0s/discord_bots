import datetime
import helpers
import os
import disnake

class Logger:
    def __init__(self, state: bool):
        self.state = state

    def error(self, err, guild):
        if not self.state:
            return
        abs_path = self.get_path(guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + " : ERROR : " + str(err) + "\n")
        f.close()

    def skip(self, inter):
        if not self.state:
            return
        abs_path = self.get_path(inter.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : SKIP : Skipped track in VC: {inter.guild.voice_client.channel}\n")
        f.close()

    def enabled(self, bot):
        if not self.state:
            return
        abs_path = self.get_path("general")
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : STARTUP : Bot is logged as {bot.user}\n")
        f.close()

    def logged(self, entry):
        if not self.state:
            return
        abs_path = self.get_path(entry.user.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(datetime.datetime.now().strftime("%H:%M:%S") +
                f" : AUDIT_LOG : {entry.user} did {entry.action} to {entry.target}\n".replace('AuditLogAction.', ''))
        f.close()

    def added(self, guild, track):
        if not self.state:
            return
        abs_path = self.get_path(guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : PLAY : Added {track['title']} to queue with duration of {helpers.get_duration(track)}\n")
        f.close()

    def playing(self, guild, track):
        if not self.state:
            return
        abs_path = self.get_path(guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : PLAY : Playing {track['title']} in VC: {guild.voice_client.channel}\n")
        f.close()

    def radio(self, guild, data):
        if not self.state:
            return
        abs_path = self.get_path(guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : RADIO : Playing {data['name']} in VC: {guild.voice_client.channel}\n")
        f.close()

    def finished(self, inter):
        if not self.state:
            return
        abs_path = self.get_path(inter.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : STOP : Finished playing in VC: {inter.guild.voice_client.channel}\n")
        f.close()

    def switched(self, member, before, after):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} switched VC from {before.channel.name} to {after.channel.name}\n")
        f.close()

    def connected(self, member, after):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} joined VC {after.channel.name}\n")
        f.close()

    def disconnected(self, member, before):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} left VC {before.channel.name}\n")
        f.close()

    def log_voice_state_update(self, member, before: disnake.VoiceState, after: disnake.VoiceState):
        if before.channel and after.channel:
            if before.channel.id != after.channel.id:
                self.logger.switched(member, before, after)
            else:
                if before.deaf != after.deaf:
                    if before.deaf:
                        self.logger.guild_undeafened(member)
                    else:
                        self.logger.guild_deafened(member)
                elif before.mute != after.mute:
                    if before.mute:
                        self.logger.guild_unmuted(member)
                    else:
                        self.logger.guild_muted(member)
                elif before.self_deaf != after.self_deaf:
                    if before.self_deaf:
                        self.logger.undeafened(member)
                    else:
                        self.logger.deafened(member)
                elif before.self_mute != after.self_mute:
                    if before.self_mute:
                        self.logger.unmuted(member)
                    else:
                        self.logger.muted(member)
        elif before.channel:
            self.logger.disconnected(member, before)
        else:
            self.logger.connected(member, after)

    def guild_deafened(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} was deafened by guild admin\n")
        f.close()

    def guild_undeafened(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} was undeafened by guild admin\n")
        f.close()

    def guild_muted(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} was muted by guild admin\n")
        f.close()

    def guild_unmuted(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} was unmuted by guild admin\n")
        f.close()

    def deafened(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} deafened themself\n")
        f.close()

    def undeafened(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} undeafened themself\n")
        f.close()

    def muted(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} muted themself\n")
        f.close()

    def unmuted(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} unmuted themself\n")
        f.close()

    def video_on(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} turned on their camera\n")
        f.close()

    def video_off(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} turned off their camera\n")
        f.close()

    def stream_on(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} went live\n")
        f.close()

    def stream_off(self, member):
        if not self.state:
            return
        abs_path = self.get_path(member.guild.id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : VC : User {member} shutted their stream\n")
        f.close()

    def gpt(self, member, messages, guild_id="gpt"):
        if not self.state:
            return
        abs_path = self.get_path(guild_id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : GPT : User {member} used GPT with the query: `{messages[0]}` and got response `{messages[1]}`\n")
        f.close()

    def gpt_clear(self, member, guild_id="gpt"):
        if not self.state:
            return
        abs_path = self.get_path(guild_id)
        f = open(f'{abs_path}.txt', "a", encoding='utf-8')
        f.write(
            datetime.datetime.now().strftime("%H:%M:%S") + f" : GPT : User {member} cleared their chatGPT history\n")
        f.close()

    def get_path(self, dir_name: str):
        if not self.state:
            return
        if not os.path.exists(f"logs/{dir_name}"):
            os.makedirs(f"logs/{dir_name}")
        file_name = datetime.datetime.now().strftime('%d-%m-%Y')
        script_dir = os.path.dirname(__file__)
        rel_path = f"logs/{dir_name}/{file_name}"
        abs_path = os.path.join(script_dir, rel_path)
        return abs_path
