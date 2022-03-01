import time

from SerialHandler import *
from BoardInfos import *
from time import sleep


if __name__ == '__main__':

    # Set-up section
    board = BoardInfos()
    test = SerialHandler()
    #test.boardInfosRqst(board)
    test.setupSctRqst(9)
    # time.sleep(1)
    # test.setupSctRqst(10)
    # time.sleep(1)
    # test.boardInfosRqst(board)

    # Loop section
    while True:
        pass
        #test.serial.readPortDebug()






    # max_no_scts = 8
    # no = 0
    # sct_no = 0
    #
    #
    # print("Welcome!")
    # while not no:
    #     try:
    #         entered_val = input("Create a new section? Y/N \n")
    #         if not entered_val.upper() == "Y" and not entered_val.upper() == "N":
    #             raise StringError(entered_val)
    #         elif entered_val.upper() == "Y":
    #             check = 0
    #             while not check:
    #                 try:
    #                     nb_leds = int(input("Number of LEDs in the section"))
    #                     if not 0 < nb_leds < 10:
    #                         raise InputError(nb_leds)
    #                 except (ValueError, InputError):
    #                     print("Please input a number between 0 and 10")
    #         elif entered_val.upper() == "N":
    #             no = 1
    #     except StringError:
    #         print("Please answer with either 'Y' or 'N'")

    # led_color = {"red": 0, "grn": 0, "blu": 0, "wht": 0}
    # print("Please enter each LEDs color value (0 to 255) to send when prompted \n")
    #
    # for color in led_color:
    #     while not led_color[color]:
    #         try:
    #             color_value = int(input("Input " + str(color).upper() + " led brightness value : "))
    #             if not 0 < color_value < 255:
    #                 raise InputError(color_value)
    #             led_color[color] = color_value
    #         except (ValueError, InputError):
    #             print("Please input a number between 0 and 255")


        # try:
        #     usrInHex = input("Input hexadecimal value: ")
        #     num = int(usrInHex, 16)
        #     print("num (decimal format):", num)
        #     print("num (hexadecimal format):", hex(num))
        #
        #     write_serial(usrInHex)
        # except ValueError:
        #     print("Please input only hexadecimal value...")

    #red = input("Red hex val : ")
    #grn = input("Green hex val : ")
    #blu = input("Blue hex val : ")

    # print(type(red))
    # print(red.encode('utf-8'))
    # write_serial(red)

    # class InputError(Exception):
    #     """Exception raised for out of range number in the input.
    #
    #     Attributes:
    #         expression -- input expression in which the error occurred
    #         message -- explanation of the error
    #     """
    #
    #     def __init__(self, integer, message="Number entered is not in the 0 to 255 range"):
    #         self.integer = integer
    #         self.message = message
    #         super().__init__(self.message)
    #
    #
    # class StringError(Exception):
    #     """Exception raised for unaccepted string character
    #
    #     Attributes:
    #         expression -- input expression in which the error occurred
    #         message -- explanation of the error
    #     """
    #     def __init__(self, character, message="Character typed is not valid"):
    #         self.character = character
    #         self.message = message
    #         super().__init__(self.message)


