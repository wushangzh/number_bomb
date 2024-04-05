# -*- coding: utf-8 -*-

import random
import pygame
import threading
import PySimpleGUI as sg
import game_initials


def play_audio():
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(game_initials.SOUND_PATH)
    pygame.mixer.music.play()


audio_thread = threading.Thread(target=play_audio)


class Game:
    def __init__(self):
        self.initials = game_initials.GameInitials()

        self.player_guessed = set()
        self.computer_guessed = set()

        self.guess_range = (0, 100)

        self.game_over = False

        self.window = None

        self.layout = [
            [sg.Text('数字炸弹，启动！炸弹初始范围在0-100！', font=('微软雅黑', 20))],
            [sg.Text('你的猜测：')],
            [sg.InputText(size=(10, 1), key='-PLAYER_GUESS-'),
             sg.Button('确认', key='-OK-')],
            [sg.Text('', size=(50, 2), key='-PLAYER_OUTPUT-')],
            [sg.Text('电脑猜测的数字：'), sg.Text(
                '', size=(10, 1), key='-COMPUTER_GUESS-')],
            [sg.Text('', size=(50, 2), key='-COMPUTER_OUTPUT-')],
            [sg.Button('退出', key='-QUIT-', visible=False)]
        ]

    def set_window(self, window):
        self.window = window

    def computer_guess(self):
        if self.initials.lower_bound == self.initials.upper_bound:
            return self.initials.lower_bound

        else:
            guess = random.randint(self.initials.lower_bound, self.initials.upper_bound)
            return guess

    def process_event(self, event, values):
        if self.game_over:
            if pygame.mixer.music.get_busy():
                return
            else:
                return

        if event == '-OK-':
            player_guess_num = int(values['-PLAYER_GUESS-'])

            if player_guess_num in self.player_guessed or \
                    player_guess_num < self.guess_range[0] or player_guess_num > self.guess_range[1]:
                if player_guess_num in self.player_guessed:
                    sg.popup_error('你已经猜过了这个数字！')
                else:
                    sg.popup_error(f'请输入介于 {self.guess_range[0]} 和 {self.guess_range[1]} 之间的数字！')
                return

            self.player_guessed.add(player_guess_num)

            if player_guess_num == self.initials.target_num:
                audio_thread.start()
                self.window['-PLAYER_OUTPUT-'].update(
                    f'砰————炸弹被你引爆了！炸弹数字为：{self.initials.target_num}')
                self.game_over = True
                self.window['-QUIT-'].update(visible=True)

            elif player_guess_num < self.initials.target_num:
                self.window['-PLAYER_OUTPUT-'].update(
                    f'炸弹没有引爆！')
                self.initials.lower_bound = player_guess_num + 1
                self.guess_range = (player_guess_num + 1, self.guess_range[1])

            else:
                self.window['-PLAYER_OUTPUT-'].update(
                    f'炸弹没有引爆！')
                self.initials.upper_bound = player_guess_num - 1
                self.guess_range = (self.guess_range[0], player_guess_num - 1)

            if not self.game_over:
                computer_guess_num = self.computer_guess()

                while computer_guess_num in self.computer_guessed or \
                        computer_guess_num < self.guess_range[0] or \
                        computer_guess_num > self.guess_range[1]:
                    computer_guess_num = self.computer_guess()

                self.computer_guessed.add(computer_guess_num)

                self.window['-COMPUTER_GUESS-'].update(computer_guess_num)

                if computer_guess_num == self.initials.target_num:
                    audio_thread.start()
                    self.game_over = True
                    self.window['-COMPUTER_OUTPUT-'].update(
                        f'砰————炸弹被电脑引爆了！炸弹数字为：{self.initials.target_num}')
                    self.window['-QUIT-'].update(visible=True)

                elif computer_guess_num < self.initials.target_num:
                    self.window['-COMPUTER_OUTPUT-'].update(
                        f'炸弹没有引爆！目前炸弹范围：{computer_guess_num + 1} 至 {self.guess_range[1]}')
                    self.guess_range = (
                        max(self.guess_range[0], computer_guess_num + 1), self.guess_range[1])

                else:
                    self.window['-COMPUTER_OUTPUT-'].update(
                        f'炸弹没有引爆！目前炸弹范围：{self.guess_range[0]} 至 {computer_guess_num - 1}')
                    self.guess_range = (self.guess_range[0], min(
                        self.guess_range[1], computer_guess_num - 1))

                    if self.guess_range[0] > self.guess_range[1]:
                        self.guess_range = (
                            self.guess_range[1], self.guess_range[0])
