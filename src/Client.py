# coding=utf-8
from Application import Application

def main():
    app_ = Application()
    app_.start()
    print("Application start....")
    app_.join()
    print("Exit")

if __name__ == '__main__':
    main()