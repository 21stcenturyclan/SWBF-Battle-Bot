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
            return Context.get_nickname(ctx) or Context.get_username(ctx)
        elif user:
            return Context.get_nickname(user=user) or Context.get_username(user=user)

    @staticmethod
    def get_user_roles(ctx=None, user=None):
        if ctx:
            return [role.name for role in ctx.message.author.roles]
        elif user:
            return [role.name for role in user.roles]

    @staticmethod
    def get_emoji_name(reaction):
        s = str(reaction.emoji)
        return s[2:s.rfind(':')]