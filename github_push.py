import os
os.system('git config user.email "jmalhot@gmail.com"')
for i in range(7):
    if os.path.exists('output.txt'):
        os.system('rm output.txt')
        os.system('git add --all')
        os.system('git commit -m "Updates"')
        os.system('git push -u origin master')

    f = open("output.txt", "a")
    f.write("Now the file has more content!")
    f.close()

    os.system('git add output.txt')
    os.system('git commit -m "Updates"')
    os.system('git push -u origin master')
