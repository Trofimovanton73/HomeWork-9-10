from aiogram import types
from create_bot import bot
import model
import random
import asyncio
from create_bot import dp

async def start(message: types.Message):
    player = message.from_user
    model.set_player(player)
    await bot.send_message(message.from_user.id, f'Приветствую тебя {player.first_name}, маленький любитель сладкого!\n'
                'Хотите сыграть в игру про сахарноый диабет"?\n'
                'Для начала я расскажу правила:\n'
                'Я даю тебе 150, вы берете их поочереди,\n'
                'причем, за один раз можно взять не больше 28 конфет.\n'
                'Выигрывает тот, кто последним ходом заберет все конфеты.\n'
                'Начнем!!!')
    await asyncio.sleep(3)                                                
    dp.register_message_handler(player_turn)
    first_turn = random.randint(0,1)
    if first_turn:
        await await_player(player)
    else:
        await enemy_turn(player)

async def player_turn(message: types.Message):
    player = message.from_user
    model.set_player(player)
    if (message.text).isdigit():
        if 0 < int(message.text) < 29:
            total_count = model.get_total_candies()
            player_take = int(message.text)
            total = total_count - player_take
            await bot.send_message(player.id, f'{player.first_name} взял{player_take} конфет,'
                                              f'и на столе осталось {total}')
            if model.check_win(total):
                await bot.send_message(player.id, f'Победил {player.first_name}, ты сделал эту железяку!!!')
                return 
            model.set_total_candies(total)
            await enemy_turn(player)
        else:
            await bot.send_message(player.id, 'А не много ли взял? Послушай жадина, бери не больше 28')
    else:
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name},'
                                                     f'вообще-то конфеты мы считаем в цифрах')
async def enemy_turn(player):
    total_count = model.get_total_candies()
    if total_count < 29:
        enemy_take = total_count
    else:
        # enemy_take = (total_count - 1)%28
        enemy_take = random.randint(1,28)
    total = total_count - enemy_take
    await bot.send_message(player.id, f'Бот взял {enemy_take} конфет,'
                                      f' и на столе осталось {total}')
    if model.check_win(total):
        await bot.send_message(player.id, f'Баста, карапузик!  {player.first_name} ты приграл')
        return 
    model.set_total_candies(total)
    await asyncio.sleep(1)
    await await_player(player)

async def await_player(player):
    max_take = model.get_max_take()    
    await bot.send_message(player.id,
                    f'{player.first_name}, бери конфеты, но не больше {max_take}')


async def set_total_candies(message: types.Message):
    count = int((message.text).split(' ')[1])
    model.set_total_candies(count)
    await bot.send_message(message.from_user.id, f'Максимальное количество конфет изменили на {count}')

                    