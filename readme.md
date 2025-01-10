I find myself converting python files to executables often on different platforms and unlike pyinstaller or py2exe I wanted my own tool to build .exe files AND do final tests(Unit tests should already be done) before compiling! This tools help me avoid repetition and automate multiple files if I need too!

Using Pyinstaller, I wanted to focus on linux and windows use because I work out of linux for penetration testing but I target Windows machines mostly.

Please mute I forgot to turn audio off =).
Example video here https://youtu.be/H8bVth2W-dQ!

Steps:

1.python Python2Exe.py "tobeEXE.py"
2.enter test arguments, if none press enter(arguments come in string type by default)
3.if output is what's expected press y to test again and then enter names of third party libraries
4.let program build

Yay, new executable!!

