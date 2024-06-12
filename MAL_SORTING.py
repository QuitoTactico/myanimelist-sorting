import mal  #pip install mal-api
import csv
import glob
from collections import deque
from time import sleep
from xml.dom.minidom import parse
import mal.config

DELAY = 3  # if you get banned or the media isn't being analized properly, increase this number. (Float allowed)
mal.config.TIMEOUT = 10     # and this one too (original num = 5)
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


def media_info(media_id, media_type:str='anime'):
    if media_type == 'anime':
        media = mal.Anime(media_id)
    else:
        media = mal.Manga(media_id)
    return {
        'name':         media.title,
        'id':           media.mal_id,
        'score':        media.score,
        'members':      media.members,
        'favorites':    media.favorites,
        'ratio':        round((media.favorites / media.members)*100 , 2)
    }

def list_info_requester(raw_anime_list, media_type:str='anime'):
    anime_list = deque()

    largo = len(raw_anime_list)
    i = 1
    actual_name  = ''
    actual_score = 0

    errors_list = []

    for raw_anime in raw_anime_list:
        actual_anime = {'name':'','score':0}

        passed = False
        for i, try_time in enumerate([10, 20, 30]):
            try:
                actual_anime = media_info(raw_anime['id'])
                passed = True
                break
            except:
                print(f'-try #{i+2}: sleeping {try_time} seconds- [{raw_anime["name"]}]')
                sleep(try_time)
                
        if not passed:   
            print(f'error\t| {raw_anime["name"]}')
            errors_list.append(raw_anime)
            continue

        if actual_anime['score'] == None:
            actual_anime['score'] = 0

        anime_list.append(actual_anime)

        if actual_anime['score'] > actual_score:
            actual_score = actual_anime['score']
            actual_name  = actual_anime['name']

        print_media(largo, i, actual_name, actual_score, raw_anime, actual_anime)
        i += 1
        sleep(DELAY)         # if you get banned, increase this number

    if len(errors_list) != 0:
        print(f'{len(errors_list)} {media_type}s not analized')
        for j in errors_list:
            print(f"{j['id']} \t| {j['name']}")

    return anime_list

def print_media(largo, i, actual_name, actual_score, raw_anime, actual_anime):
    print(i, ' - ', "{:.2f}".format(round(i*100/largo,2)),'%\t|', "{:.2f}".format(actual_score), '|',actual_name,'\t> ',"{:.2f}".format(actual_anime['score']),'|',raw_anime['name'])

def print_sorted_list(final_list, sorted_by:str):

    sorted_list = sorted(final_list, key=lambda d: d[sorted_by]) 
    for item in sorted_list:
        print(f"{item['score']:.2f}\t| {item['members']}  \t| {item['favorites']}     \t| {item['ratio']:.2f}%\t| {item['name']}")
        
    print('---------------------------------------------------------------------')
    print(f'score\t| members\t| favorites\t| ratio\t| sorted by {sorted_by.upper()}\n')


#basically useless, but you can use it if you need to XD
def save_list_csv(final_list, media_type:str='anime'):
    import csv
    
    fields = ['name', 'id', 'score', 'members', 'favorites', 'ratio']
    
    name = f'MAL_{media_type.upper()}_SAVE_DATA.csv'
    with open(name, 'w', encoding='UTF8', newline='') as file:

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(final_list)



def save_tops_txt(final_list, media_type:str='anime'):
    name = f'MAL_{media_type.upper()}_SAVE_TOPS.txt'
    with open(name, 'w', encoding='UTF8') as file:
        for sorted_by in ['score','members','favorites','ratio']:

            sorted_list = sorted(final_list, key=lambda d: d[sorted_by]) 
            for item in sorted_list:
                file.write(f"{item['score']:.2f} \t| {item['members']}  \t| {item['favorites']}    \t| {item['ratio']:.2f}%\t| {item['name']}\n")
                
            file.write('---------------------------------------------------------------------\n')
            file.write(f'score\t| members\t| favorites\t| ratio\t| sorted by {sorted_by.upper()}\n')
            file.write('--------------------------------------------------------------------------------------------------------------\n\n\n')



def interfaz(final_list, media_type:str='anime'):
    while True:
        o = input('sort by Score, Members, Favorites or Ratio? (s/m/f/r), save Data, Tops (d/t) or Exit? (0) -> ').lower()
        sorted_by = ""

        if o in ['exit','0']:       break
        if o in ['score','s']:      sorted_by = 'score'
        if o in ['members','m']:    sorted_by = 'members'
        if o in ['favorites','f']:  sorted_by = 'favorites'
        if o in ['ratio','r']:      sorted_by = 'ratio'

        if o in ['data','d']:
            save_list_csv(final_list, media_type=media_type)
            print(f'{media_type.capitalize()} list data saved successfully')
            continue

        if o in ['tops','t']:
            save_tops_txt(final_list, media_type=media_type)
            print(f'{media_type.capitalize()}tops saved successfully')
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
            final_media_list = []
            with open('MAL_ANIME_SAVE_DATA.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    for key in ['id','members','favorites']:
                        row[key] = int(row[key])
                    for key in ['score','ratio']:
                        row[key] = float(row[key])
                    final_media_list.append(row)
            interfaz(final_media_list, anime = True) 
        exit()   
    

    else:
        list_type = input('Anime or Manga? (a/m) -> ')
        a = input('Non-completed, Completed or All? (n/c/a) -> ')


        media_type = 'manga' if list_type == 'm' else 'anime'

        if a == 'c':
            raw_media_list = get_anime_from_xml(only_completed=True) if media_type == 'anime' else get_manga_from_xml(only_completed=True)
            media_completion_type = 'animes completed'
        elif a == 'a':
            raw_media_list = get_anime_from_xml(all=True) if media_type == 'anime' else get_manga_from_xml(all=True)
            media_completion_type = 'animes in total'
        else:
            raw_media_list = get_anime_from_xml(only_non_completed=True) if media_type == 'anime' else get_manga_from_xml(only_non_completed=True)
            media_completion_type = 'animes non-completed'

        list_used = MYANIMELIST if media_type == 'anime' else MYMANGALIST
        print(f'{len(raw_media_list)} {media_completion_type} took from {list_used}')
        final_media_list = list_info_requester(raw_media_list, media_type=media_type)
        interfaz(final_media_list, media_type=media_type)

