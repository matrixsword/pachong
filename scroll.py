import pyautogui,time

class Scroll:
    def scroll(self):
        try:
            while True:
                pyautogui.scroll(-500)
                time.sleep(1)
        except KeyboardInterrupt:
            print('\nDone')
            
    def dragHaotu(self):
        distance = 100
        try:
            while True:
                pyautogui.mouseDown(button='left')
                pyautogui.dragRel(0,-distance,duration=.3)
                pyautogui.mouseUp(button='left')
                pyautogui.moveRel(0,distance,duration=.3)
                pyautogui.click()
                time.sleep(1)
                pyautogui.press('esc')
                time.sleep(1)
        finally:
            print('\nDone')
if __name__ == '__main__':
    #Scroll().dragHaotu()
    Scroll().scroll()

