try:
    import colorama
except Exception as e:
    print('modules error')
colorama.init(
)
run = True
while run:
    num = int (input ('enter your number'))
    print ( ' your number is == '+ str(num))
    if num >= 10:
        print('your number is gut')