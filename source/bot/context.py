class Context:
    @staticmethod
    def get_username(ctx=None, user=None):
        if ctx:
            return ctx.message.author.name
        elif user:
            return user.name

    @staticmethod
    def get_nickname(ctx=None, user=None):
        if ctx:
            return ctx.message.author.nick
        elif user:
            return user.nick

    @staticmethod
    def get_nick_or_name(ctx=None, user=None):
        if ctx:
            return Context.get_username(ctx) or Context.get_nickname(ctx)
        elif user:
            return Context.get_username(user=user) or Context.get_nickname(user=user)

    @staticmethod
    def get_emoji_name(reaction):
        s = str(reaction.emoji)
        return s[2:s.rfind(':')]