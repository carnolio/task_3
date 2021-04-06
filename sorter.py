import click,eyed3,shutil,os
'''
Реализовать консольное (CLI) приложение для сортировки музыкальных файлов по исполнителям и альбомам:
программа анализирует файлы в исходной директории, считывает ID3-теги, извлекает из них информацию о названии трека, исполнителе и альбоме;


программа должна принимать 3 ключа командной строки:
--help - вывести справочное сообщение;
-s | --src-dir - исходная директория, по умолчанию ".";
-d | --dst-dir - целевая директория, по умолчанию ".".
в ходе работы программа должна выводить лог действий в виде
<путь до исходного файла> -> <путь до файла результата>;
программа должна корректно обрабатывать ошибки (не хватает прав доступа, директория не существует и т.д.) и сообщать об этом пользователю, не прерывая свою работу.
Пример консольного интерфейса интерфейс:
$ ./sorter.py --help
Usage: sorter.py [OPTIONS]
Options:
  -s, --src-dir TEXT  Source directory.
  -d, --dst-dir TEXT  Destination directory.
  --help              Show this message and exit.
Пример консольного интерфейса интерфейс:
$ ./sorter.py
...
./Du hast.mp3 -> ./Rammstein/Sehnsucht/Du hast - Rammstein - Sehnsucht.mp3
...
Done.
$ ./sorter.py --dst-dir=/home/user/some/directory
...

'''
@click.command()
@click.option('-s', default='./', help='Source dir. Default = ./')
@click.option('-d', default='./', help='Destination dir. Default = ./')
def hello():
    click.echo('Hello World!')

srcDir=".\music"

mp3s = os.listdir(path=srcDir)

#print (os.name)
def checkName (filename):
    # escList = ['\\','/',':','*','<','>','|']
    fname=""
    escList = ['/', ':','*','?','<', '>', '|']
    for i in filename:
        if i in escList:
            continue
        fname += i
    return fname

for mp3 in mp3s:
    print("file: ", mp3)
    if os.name == "nt":
        delim = "\\"
    else:
        delim = "/"
#try:
    title, album, artist = "", "", ""
    isMove = True
    audiofile = eyed3.load(srcDir + delim + mp3)
    print(audiofile)
    if audiofile.tag.title != None:
        title = audiofile.tag.title.encode("cp1252").decode("cp1251")
        title = title.strip()
    if audiofile.tag.artist != None:
        artist = audiofile.tag.artist.encode("cp1252").decode("cp1251")
        artist = artist.strip()
    if audiofile.tag.album != None:
        album = audiofile.tag.album.encode("cp1252").decode("cp1251")
        album = album.strip()
#except Exception:
    #print("No ID3 Tag")
#finally:
    print("title:"+title)
    print("artist:"+artist)
    print("album:"+album)

    #audiofile.tag.save()

    # группирует файлы  по исполнителям и альбомам, так, чтобы получить структуру директорий
    # <директория назначения>/<исполнитель>/<альбом>/<имя файла>.mp3
    #try:
        # если в тегах нет информации о названии трека, использует оригинальное имя файла
    if title == None:
        newFileName = mp3
    #если в тегах нет информации об исполнителе или альбоме, пропускает файл, оставляя его без изменений в исходной директории.
    elif artist == "" or album == "":
        isMove = False
    # переименовывает файлы по схеме <название трека> - <исполнитель> - <альбом>.mp3;
    if isMove:
        newFileName = checkName(title+" - "+artist+" - "+album+".mp3")
        newPath = checkName(srcDir + delim + artist + delim + album + delim)
        print(newPath + newFileName)
        print("try create dir:" + newPath)
        print("chechedName:",checkName(newPath))
        os.makedirs(newPath, mode=0o777, exist_ok=False)
        os.rename(srcDir+delim+mp3, newFileName)
        shutil.move(newFileName, newPath)
        # в ходе работы программа должна выводить лог действий в виде
        # <путь до исходного файла> -> <путь до файла результата>;
        # print(path+'\\'+mp3)
        # ./ Duhast.mp3 -> / home / user / some / directory / Rammstein / Sehnsucht / Duhast - Rammstein - Sehnsucht.mp3
    #except Exception:
    #    print("error")


    #shutil.move(src, dst, copy_function=copy2)


    #log = '{}'