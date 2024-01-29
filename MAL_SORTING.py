import mal  #pip install mal-api
import csv
import glob
from collections import deque
from time import sleep
from xml.dom.minidom import parse

'''                            
              `7MMM.     ,MMF'      db      `7MMF'      
                MMMb    dPMM       ;MM:       MM        
                M YM   ,M MM      ,V^MM.      MM        
                M  Mb  M' MM     ,M  `MM      MM        
                M  YM.P'  MM     AbmmmqMA     MM      , 
                M  `YM'   MM    A'     VML    MM     ,M 
              .JML. `'  .JMML..AMA.   .AMMA..JMMmmmmMMM 

                                                              
     .M"""bgd                      mm      db                        
    ,MI    "Y                      MM                                
    `MMb.      ,pW"Wq.  `7Mb,od8 mmMMmm  `7MM  `7MMpMMMb.   .P"Ybmmm 
      `YMMNq. 6W'   `Wb   MM' "'   MM      MM    MM    MM  :MI  I8   
    .     `MM 8M     M8   MM       MM      MM    MM    MM   WmmmP"   
    Mb     dM YA.   ,A9   MM       MM      MM    MM    MM  8M        
    P"Ybmmd"   `Ybmd9'  .JMML.     `Mbmo .JMML..JMML  JMML. YMMMMMb  
                                                           6'     dP 
                                                           Ybmmmd'     v1.8.10
'''

def get_latest_xml(anime = False, manga = False):
    archivos = glob.glob('animelists/animelist*.xml') if anime else glob.glob('mangalists/mangalist*.xml')
    numeros = [archivo[21:31] for archivo in archivos]
    mayor = max(numeros)
    indice = numeros.index(mayor)
    completion = archivos[indice][21:-4]
    archivo_mas_reciente = f'animelists/animelist_{completion}.xml' if anime else f'mangalists/mangalist_{completion}.xml'
    return archivo_mas_reciente

# if you want to select your your anime or manga list exportation, write the dir/name down here
# example = 'animelists/animelist_1699835113_-_10513306.xml'
MYANIMELIST = get_latest_xml(anime = True)
MYMANGALIST = get_latest_xml(manga = True)


def get_anime_from_xml(only_non_completed = False, only_completed = False, all = False):
    anime_list = deque()

    DOMTree = parse(MYANIMELIST)
    collection = DOMTree.documentElement

    animes = collection.getElementsByTagName("anime")

    if only_non_completed:
        for anime in animes:
            if anime.getElementsByTagName('my_status')[0].childNodes[0].data != 'Completed':
                anime_list.append(
                    {
                        'name' :anime.getElementsByTagName('series_title')[0].childNodes[0].data, 
                        'id'   :anime.getElementsByTagName('series_animedb_id')[0].childNodes[0].data
                    })
    elif only_completed:
        for anime in animes:
            if anime.getElementsByTagName('my_status')[0].childNodes[0].data == 'Completed':
                anime_list.append(
                    {
                        'name' :anime.getElementsByTagName('series_title')[0].childNodes[0].data, 
                        'id'   :anime.getElementsByTagName('series_animedb_id')[0].childNodes[0].data
                    })
    elif all:
        for anime in animes:
            anime_list.append(
                {
                    'name' :anime.getElementsByTagName('series_title')[0].childNodes[0].data, 
                    'id'   :anime.getElementsByTagName('series_animedb_id')[0].childNodes[0].data
                })


    return anime_list

def get_manga_from_xml(only_non_completed = False, only_completed = False, all = False):
    manga_list = deque()

    DOMTree = parse(MYMANGALIST)
    collection = DOMTree.documentElement

    mangas = collection.getElementsByTagName("manga")

    if only_non_completed:
        for manga in mangas:
            if manga.getElementsByTagName('my_status')[0].childNodes[0].data != 'Completed':
                manga_list.append(
                    {
                        'name' :manga.getElementsByTagName('manga_title')[0].childNodes[0].data, 
                        'id'   :manga.getElementsByTagName('manga_mangadb_id')[0].childNodes[0].data
                    })
    elif only_completed:
        for manga in mangas:
            if manga.getElementsByTagName('my_status')[0].childNodes[0].data == 'Completed':
                manga_list.append(
                    {
                        'name' :manga.getElementsByTagName('manga_title')[0].childNodes[0].data, 
                        'id'   :manga.getElementsByTagName('manga_mangadb_id')[0].childNodes[0].data
                    })
    elif all:
        for manga in mangas:
            manga_list.append(
                {
                    'name' :manga.getElementsByTagName('manga_title')[0].childNodes[0].data, 
                    'id'   :manga.getElementsByTagName('manga_mangadb_id')[0].childNodes[0].data
                })


    return manga_list

# Deprecated
def search_by_name(name_search):
    search = mal.AnimeSearch(name_search, 10)
    first_result = search.results[0]

    anime = {
        'name'      : first_result.title,
        'score'     : first_result.score
    }
    return anime


def anime_info(anime_id):
    anime = mal.Anime(anime_id)
    return {
        'name':         anime.title,
        'id':           anime.mal_id,
        'score':        anime.score,
        'members':      anime.members,
        'favorites':    anime.favorites,
        'ratio':        round((anime.favorites / anime.members)*100 , 2)
    }

def manga_info(manga_id):
    manga = mal.Manga(manga_id)
    return {
        'name':         manga.title,
        'id':           manga.mal_id,
        'score':        manga.score,
        'members':      manga.members,
        'favorites':    manga.favorites,
        'ratio':        round((manga.favorites / manga.members)*100 , 2)
    }

def animelist_info_requester(raw_anime_list):
    anime_list = deque()

    largo = len(raw_anime_list)
    i = 1
    actual_name  = ''
    actual_score = 0

    errors_list = []

    for raw_anime in raw_anime_list:
        actual_anime = {'name':'','score':0}
        try:
            actual_anime = anime_info(raw_anime['id'])
        except:
            print('-second try-')
            sleep(15)
            try:
                actual_anime = anime_info(raw_anime['id'])
            except:
                print('-third try-')
                sleep(30)
                try:
                    actual_anime = anime_info(raw_anime['id'])
                except:
                    print(f'error\t| {raw_anime["name"]}')
                    errors_list.append(raw_anime)
                    continue

        if actual_anime['score'] == None:
            actual_anime['score'] = 0

        anime_list.append(actual_anime)

        if actual_anime['score'] > actual_score:
            actual_score = actual_anime['score']
            actual_name  = actual_anime['name']

        print(i, ' - ', "{:.2f}".format(round(i*100/largo,2)),'%\t|', "{:.2f}".format(actual_score), '|',actual_name,'\t> ',"{:.2f}".format(actual_anime['score']),'|',raw_anime['name'])
        i += 1
        sleep(2)         # if you get banned, increase this number

    if len(errors_list) != 0:
        print(f'{len(errors_list)} animes not analized')
        for j in errors_list:
            print(f"{j['id']} \t| {j['name']}")

    return anime_list

def mangalist_info_requester(raw_manga_list):
    manga_list = deque()

    largo = len(raw_manga_list)
    i = 1
    actual_name  = ''
    actual_score = 0

    errors_list = []

    for raw_manga in raw_manga_list:
        actual_manga = {'name':'','score':0}
        try:
            actual_manga = manga_info(raw_manga['id'])
        except:
            print('-second try-')
            sleep(10)
            try:
                actual_manga = manga_info(raw_manga['id'])
            except:
                print(f'error\t| {raw_manga["name"]}')
                errors_list.append(raw_manga)
                continue

        if actual_manga['score'] == None:
            actual_manga['score'] = 0

        manga_list.append(actual_manga)

        if actual_manga['score'] > actual_score:
            actual_score = actual_manga['score']
            actual_name  = actual_manga['name']

        print(i, ' - ', "{:.2f}".format(round(i*100/largo,2)),'%\t|', "{:.2f}".format(actual_score), '|',actual_name,'\t> ',"{:.2f}".format(actual_manga['score']),'|',raw_manga['name'])
        i += 1
        sleep(2.5)      # if you get banned, increase this number

    if len(errors_list) != 0:
        print(f'{len(errors_list)} mangas not analized')
        for j in errors_list:
            print(f"{j['id']} \t| {j['name']}")

    return manga_list

def print_sorted_list(final_list, sorted_by:str):

    sorted_list = sorted(final_list, key=lambda d: d[sorted_by]) 
    for item in sorted_list:
        print(f"{item['score']:.2f}\t| {item['members']}  \t| {item['favorites']}     \t| {item['ratio']:.2f}%\t| {item['name']}")
        
    print('---------------------------------------------------------------------')
    print(f'score\t| members\t| favorites\t| ratio\t| sorted by {sorted_by.upper()}\n')


#basically useless, but you can use it if you need to XD
def save_list_csv(final_list, anime = False, manga = False):
    import csv
    
    fields = ['name', 'id', 'score', 'members', 'favorites', 'ratio']
    
    name = 'MAL_ANIME_SAVE_DATA.csv' if anime else 'MAL_MANGA_SAVE_DATA.csv'
    with open(name, 'w', encoding='UTF8', newline='') as file:

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(final_list)



def save_tops_txt(final_list, anime = False, manga = False):
    name = 'MAL_ANIME_SAVE_TOPS.txt' if anime else 'MAL_MANGA_SAVE_TOPS.txt'
    with open(name, 'w', encoding='UTF8') as file:
        for sorted_by in ['score','members','favorites','ratio']:

            sorted_list = sorted(final_list, key=lambda d: d[sorted_by]) 
            for item in sorted_list:
                file.write(f"{item['score']:.2f} \t| {item['members']}  \t| {item['favorites']}    \t| {item['ratio']:.2f}%\t| {item['name']}\n")
                
            file.write('---------------------------------------------------------------------\n')
            file.write(f'score\t| members\t| favorites\t| ratio\t| sorted by {sorted_by.upper()}\n')
            file.write('--------------------------------------------------------------------------------------------------------------\n\n\n')



def interfaz(final_list, anime = False, manga = False):
    while True:
        o = input('sort by Score, Members, Favorites or Ratio? (s/m/f/r), save Data, Tops (d/t) or Exit? (0) -> ').lower()
        sorted_by = ""

        if o in ['exit','0']:       break
        if o in ['score','s']:      sorted_by = 'score'
        if o in ['members','m']:    sorted_by = 'members'
        if o in ['favorites','f']:  sorted_by = 'favorites'
        if o in ['ratio','r']:      sorted_by = 'ratio'

        if o in ['data','d']:
            if anime:
                save_list_csv(final_list, anime = True)
                print('Anime list data saved successfully')
            elif manga:
                save_list_csv(final_list, manga = True)
                print('Manga list data saved successfully')
            continue

        if o in ['tops','t']:
            if anime:
                save_tops_txt(final_list, anime = True)
                print('Tops saved successfully')
            elif manga:
                save_tops_txt(final_list, manga = True)
                print('Tops saved successfully')
            continue

        print_sorted_list(final_list , sorted_by)

    
    print('bye!')


if __name__ == '__main__':

    '''
    o = input('use sample list? (y/n) -> ')

    if o == 'y':
        try:
            # these are my lists. used to test bc the conversor takes some time 
            from MAL_SORTING_SAMPLE_LISTS import COMPLETED_LIST, NON_COMPLETED_LIST

            l = input('Non-completed, Completed or All (sample list)? (n/c/a) -> ')

            if l == 'c':
                final_list = COMPLETED_LIST
                anime_type = 'animes completed'
            elif l == 'a':
                all_list = []
                all_list.extend(NON_COMPLETED_LIST)
                all_list.extend(COMPLETED_LIST)
                final_list = all_list
                anime_type = 'animes in total'
            else:
                final_list = NON_COMPLETED_LIST
                anime_type = 'animes non-completed'
            print(f'{len(final_list)} {anime_type}')
        except:
            pass
        exit()'''

    r = input('Recover saved data? (y/n) -> ')
    if r == 'y':
        list_type = input('Anime or Manga? (a/m) -> ')
        if list_type == 'm':
            final_manga_list = []
            with open('MAL_MANGA_SAVE_DATA.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    for key in ['id','members','favorites']:
                        row[key] = int(row[key])
                    for key in ['score','ratio']:
                        row[key] = float(row[key])
                    final_manga_list.append(row)
            interfaz(final_manga_list, manga = True)
        else:
            final_anime_list = []
            with open('MAL_ANIME_SAVE_DATA.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    for key in ['id','members','favorites']:
                        row[key] = int(row[key])
                    for key in ['score','ratio']:
                        row[key] = float(row[key])
                    final_anime_list.append(row)
            interfaz(final_anime_list, anime = True) 
        exit()   
    

    else:
        list_type = input('Anime or Manga? (a/m) -> ')
        a = input('Non-completed, Completed or All? (n/c/a) -> ')

        if list_type == 'm':
            if a == 'c':
                raw_manga_list = get_manga_from_xml(only_completed=True)
                manga_type = 'mangas completed'
            elif a == 'a':
                raw_manga_list = get_manga_from_xml(all=True)
                manga_type = 'mangas in total'
            else:
                raw_manga_list = get_manga_from_xml(only_non_completed=True)
                manga_type = 'mangas non-completed'

            print(f'{len(raw_manga_list)} {manga_type}')
            final_manga_list = mangalist_info_requester(raw_manga_list)
            interfaz(final_manga_list, manga = True)

        else:
            if a == 'c':
                raw_anime_list = get_anime_from_xml(only_completed=True)
                anime_type = 'animes completed'
            elif a == 'a':
                raw_anime_list = get_anime_from_xml(all=True)
                anime_type = 'animes in total'
            else:
                raw_anime_list = get_anime_from_xml(only_non_completed=True)
                anime_type = 'animes non-completed'

            print(f'{len(raw_anime_list)} {anime_type}')
            final_anime_list = animelist_info_requester(raw_anime_list)
            interfaz(final_anime_list, anime = True)



