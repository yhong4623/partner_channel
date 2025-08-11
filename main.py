import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Discord bot token from environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not TOKEN:
    print("未找到 Discord Bot Token，請檢查環境變數設定")

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.guilds = True          # Enable guild intent
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot ready event
@bot.event
async def on_ready():
    print(f'{bot.user} 已經上線!')
    try:
        # Sync slash commands with Discord
        synced = await bot.tree.sync()
        print(f"同步了 {len(synced)} 個指令")
    except Exception as e:
        print(f"同步指令時發生錯誤: {e}")

# Command to create partner channel
@bot.hybrid_command(name="partner", description="創建合作夥伴頻道")
@commands.has_permissions(manage_channels=True)  # Requires manage channels permission
async def partner(ctx, channelname: str, user: discord.Member):
    try:
        # Get the category channel from environment variable
        category = ctx.guild.get_channel(int(os.getenv('CATEGORY_ID')))
        if not category:
            await ctx.send("找不到指定的分類!", ephemeral=True)
            return
        
        # Verify if the channel is a category
        if not isinstance(category, discord.CategoryChannel):
            await ctx.send("指定的 ID 不是一個分類頻道!", ephemeral=True)
            return
        
        # Create new channel with specified name format
        channel_name = os.getenv('CHANNEL_NAME')
        new_channel = await category.create_text_channel(channel_name)
        
        # Set up channel permissions for the user
        overwrites = discord.PermissionOverwrite()
        overwrites.manage_channels = True      # Allow channel management
        overwrites.send_messages = True        # Allow sending messages
        overwrites.use_external_emojis = True  # Allow using external emojis
        overwrites.attach_files = True         # Allow file attachments
        await new_channel.set_permissions(user, overwrite=overwrites)
        
        await ctx.send(f"已創建頻道 {new_channel.mention} 並設定 {user.mention} 的權限", ephemeral=True)
    
    except discord.Forbidden:
        await ctx.send("機器人沒有足夠的權限執行此操作!", ephemeral=True)
    except Exception as e:
        await ctx.send(f"發生錯誤: {str(e)}", ephemeral=True)

# Command to give user permissions in specific channel
@bot.hybrid_command(name="joinpartner", description="給予使用者特定頻道的權限")
@commands.has_permissions(manage_channels=True)  # Requires manage channels permission
async def joinpartner(ctx, channel: discord.TextChannel, user: discord.Member):
    try:
        # Verify channel is in the correct category
        category = ctx.guild.get_channel(int(os.getenv('CATEGORY_ID')))
        if not category or channel.category_id != category.id:
            await ctx.send("指定的頻道不在合作夥伴分類中!", ephemeral=True)
            return
        
        # Set up channel permissions for the user
        overwrites = discord.PermissionOverwrite()
        overwrites.manage_channels = True      # Allow channel management
        overwrites.send_messages = True        # Allow sending messages
        overwrites.use_external_emojis = True  # Allow using external emojis
        overwrites.attach_files = True         # Allow file attachments
        await channel.set_permissions(user, overwrite=overwrites)
        
        await ctx.send(f"已為 {user.mention} 設定 {channel.mention} 的權限", ephemeral=True)
    
    except discord.Forbidden:
        await ctx.send("機器人沒有足夠的權限執行此操作!", ephemeral=True)
    except Exception as e:
        await ctx.send(f"發生錯誤: {str(e)}", ephemeral=True)

# Error handler for partner command
@partner.error
async def partner_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("您沒有執行此指令的權限!", ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("請提供所需的參數: `!partner <頻道名稱> <用戶>`", ephemeral=True)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("請確認您輸入的用戶是有效的!", ephemeral=True)
    else:
        await ctx.send(f"發生錯誤: {str(error)}", ephemeral=True)

# Error handler for joinpartner command
@joinpartner.error
async def joinpartner_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("您沒有執行此指令的權限!", ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("請提供所需的參數: `!joinpartner <頻道> <用戶>`", ephemeral=True)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("請確認您輸入的頻道和用戶是有效的!", ephemeral=True)
    else:
        await ctx.send(f"發生錯誤: {str(error)}", ephemeral=True)

# Main entry point
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤: 找不到 Discord Bot Token!")
        print("請在 .env 檔案中設定 DISCORD_BOT_TOKEN，或直接在程式碼中設定 TOKEN 變數")