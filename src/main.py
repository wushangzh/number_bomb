# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import game_logic


def main():
    game = game_logic.Game()

    window = sg.Window('数字炸弹', game.layout)
    game.set_window(window)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == '-QUIT-':
            break

        game.process_event(event, values)

    window.close()


if __name__ == "__main__":
    main()
