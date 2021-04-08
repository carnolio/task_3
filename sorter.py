import eyed3,shutil,os,argparse
'''
Реализовать консольное (CLI) приложение для сортировки музыкальных файлов по исполнителям и альбомам:
программа анализирует файлы в исходной директории, считывает ID3-теги, извлекает из них информацию о названии трека, исполнителе и альбоме;
программа должна принимать 3 ключа командной строки:
--help - вывести справочное сообщение;
программа должна корректно обрабатывать ошибки (не хватает прав доступа, директория не существует и т.д.) и сообщать об этом пользователю, не прерывая свою работу.
'''
parser = argparse.ArgumentParser(description='Sort music files by artist albun and track')
parser.add_argument(
        '-s',
        '--src_dir',
        type=str,
        #текущая директория
        default=os.getcwd(),
        help='Source directory def.\\')
parser.add_argument(
        '-d',
        '--dst_dir',
        type=str,
        default=os.getcwd(),
        help='Destination directory def.\\')

namespace = parser.parse_args()
dst_dir = namespace.dst_dir
src_dir = namespace.src_dir



def checkName (filename):
    escList = ['\\','/',':','*','<','>','|','?']
    fname=""
    escList = ['/', ':','*','?','<', '>', '|']
    for i in filename:
        if i in escList:
            continue
        fname += i
    return fname

if os.access(dst_dir, os.W_OK) and os.path.exists(dst_dir) and os.path.exists(src_dir):

    mp3s = os.listdir(path=src_dir)

    for mp3 in mp3s:
        if os.name == "nt":
            delim = "\\"
        else:
            delim = "/"
    #try:
        title, album, artist = "", "", ""
        isMove = True
        audiofile = eyed3.load(src_dir + delim + mp3)
        if audiofile and audiofile.tag and os.name == "nt":
            if audiofile.tag.title != None:
                title = audiofile.tag.title.encode("cp1252").decode("cp1251")
                title = title.strip()
            if audiofile.tag.artist != None:
                artist = audiofile.tag.artist.encode("cp1252").decode("cp1251")
                artist = artist.strip()
            if audiofile.tag.album != None:
                album = audiofile.tag.album.encode("cp1252").decode("cp1251")
                album = album.strip()

        # группирует файлы  по исполнителям и альбомам, так, чтобы получить структуру директорий
        # <директория назначения>/<исполнитель>/<альбом>/<имя файла>.mp3
        # если в тегах нет информации о названии трека, использует оригинальное имя файла
        if title == None:
            newFileName = mp3
            newPath = src_dir+delim
        #если в тегах нет информации об исполнителе или альбоме, пропускает файл, оставляя его без изменений в исходной директории.
        elif artist == "" or album == "":
            newFileName = mp3
            newPath = src_dir+delim
            isMove = False
        # переименовывает файлы по схеме <название трека> - <исполнитель> - <альбом>.mp3;
        if isMove:
            newFileName = checkName(title+" - "+artist+" - "+album+".mp3")
            newPath = checkName(dst_dir + delim + artist + delim + album + delim)
            os.makedirs(newPath, mode=0o777, exist_ok=False)
            os.rename(src_dir+delim+mp3, newFileName)
            shutil.move(newFileName, newPath)
            # в ходе работы программа должна выводить лог действий в виде
            # <путь до исходного файла> -> <путь до файла результата>;
        print("{}{}{} --> {}{}".format(src_dir,delim,mp3,newPath,newFileName))

else:
    print("src path or dst path not found or not permissons on write to dst path")

print("done.")