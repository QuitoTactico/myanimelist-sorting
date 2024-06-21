import mal  #pip install mal-api
import csv
import glob
from collections import deque
from time import sleep
from xml.dom.minidom import parse
import mal.config

DELAY = 2.5  # if you get banned or the media isn't being analized properly, increase this number. (Float allowed)
mal.config.TIMEOUT = 30     # and this one too (original num = 5)
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


def get_media_from_xml(completion_state:str, media_type:str):
    completion_state = 'n' if completion_state not in ['c','a'] else completion_state

    DOMTree = parse(MYANIMELIST if media_type == 'anime' else MYMANGALIST)
    collection = DOMTree.documentElement
    media_list_xml = collection.getElementsByTagName(media_type)

    title_search = 'series_title' if media_type == 'anime' else 'manga_title'
    id_search = 'series_animedb_id' if media_type == 'anime' else 'manga_mangadb_id'

    media_list = deque()

    for media in media_list_xml:
        status = media.getElementsByTagName('my_status')[0].childNodes[0].data
        if (status != 'Completed' and completion_state=='n') or (status == 'Completed' and completion_state=='c') or completion_state == 'a':
            media_list.append(
                {
                    'name' :media.getElementsByTagName(title_search)[0].childNodes[0].data, 
                    'id'   :media.getElementsByTagName(id_search)[0].childNodes[0].data
                })

    return media_list



@DeprecationWarning  #deprecated
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

def list_info_requester(raw_media_list, media_type:str='anime'):
    final_media_list = deque()

    largo = len(raw_media_list)
    best_name  = ''
    best_score = 0

    errors_list = []

    for i, raw_media in enumerate(raw_media_list, start=1):
        actual_media = {'name':'','score':0}

        passed = False
        tries = 1
        while True:
            try_time = tries * 10
            try:
                actual_media = media_info(raw_media['id'], media_type=media_type)
                passed = True
                break
            except:
                print(f'-try #{tries+1}: sleeping {try_time} seconds- [{raw_media["name"]}]')
                sleep(try_time)
                tries += 1
                
        if not passed:   
            print(f'error\t| {raw_media["name"]}')
            errors_list.append(raw_media)
            continue

        actual_media['score'] = actual_media['score'] or 0  # if the score is None

        final_media_list.append(actual_media)

        if actual_media['score'] >= best_score:
            best_score = actual_media['score']
            best_name  = actual_media['name']

        print_media(largo, i, best_name, best_score, raw_media, actual_media)
        sleep(DELAY)         # if you get banned, increase this number

    if len(errors_list) != 0:
        print(f'{len(errors_list)} {media_type}s not analized')
        for j in errors_list:
            print(f"{j['id']} \t| {j['name']}")

    return final_media_list



def print_media(largo, i, actual_name, actual_score, raw_anime, actual_anime):
    print(i, ' - ', "{:.2f}".format(round(i*100/largo,2)),'%\t|', "{:.2f}".format(actual_score), '|',actual_name,'\t> ',"{:.2f}".format(actual_anime['score']),'|',raw_anime['name'])



def print_sorted_list(final_list, sorted_by:str):

    sorted_list = sorted(final_list, key=lambda d: d[sorted_by]) 
    for item in sorted_list:
        print(f"{item['score']:.2f}\t| {item['members']}  \t| {item['favorites']}     \t| {item['ratio']:.2f}%\t| {item['name']}")
        
    print('---------------------------------------------------------------------')
    print(f'score\t| members\t| favorites\t| ratio\t| sorted by {sorted_by.upper()}\n')



def save_list_csv(final_list, media_type:str='anime'):
    import csv
    
    fields = ['name', 'id', 'score', 'members', 'favorites', 'ratio']
    
    name = f'saved_data/MAL_{media_type.upper()}_SAVE_DATA.csv'
    with open(name, 'w', encoding='UTF8', newline='') as file:

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(final_list)



def open_list_csv(list_used):
    final_media_list = deque()
    with open(list_used, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in ['id','members','favorites']:
                row[key] = int(row[key])
            for key in ['score','ratio']:
                row[key] = float(row[key])
            final_media_list.append(row)
    return final_media_list



def save_tops_txt(final_list, media_type:str='anime'):
    name = f'mal_{media_type}_tops.txt'
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
            print(f'{media_type}list data saved successfully')
            continue

        if o in ['tops','t']:
            save_tops_txt(final_list, media_type=media_type)
            print(f'{media_type.capitalize()} tops saved successfully')
            continue

        print_sorted_list(final_list , sorted_by)

    print('bye!')



if __name__ == '__main__':

    recover_data = input('Recover saved data? (y/n) -> ').lower() == 'y'
    media_type = 'manga' if input('Anime or Manga? (a/m) -> ').lower() == 'm' else 'anime'
        
    if recover_data:
        list_used = f'saved_data/MAL_{media_type.upper()}_SAVE_DATA.csv'
        final_media_list = open_list_csv(list_used)

        print(f'{len(final_media_list)} {media_type}s in total, recovered from [{list_used}]')
    

    else:
        completion_state = input('Non-completed, Completed or All? (n/c/a) -> ').lower()

        raw_media_list = get_media_from_xml(completion_state, media_type)

        list_used = MYANIMELIST if media_type == 'anime' else MYMANGALIST
        print(f'{len(raw_media_list)} {media_type}s, took from [{list_used}]')

        final_media_list = list_info_requester(raw_media_list, media_type=media_type)
    

    interfaz(final_media_list, media_type=media_type)

