import os
print('       ******  WordCloud  ******     ')
print('                        ——open source')
print()
print('>>正在安装依赖库，请稍后......')
print()
file = open('requirements.txt')
models = file.read().split()
for model in models:
    os.system('pip install {}'.format(model))
file.close()
print()
input('>>安装完毕，按任意键启动。')
os.system('start WordCloud.pyw')
exit()
