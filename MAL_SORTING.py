import mal
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
                                                           Ybmmmd'     v1.4 
'''



# export your anime or manga list and write the dir/name down here
MYANIMELIST = "animelist_1687503240_-_10513306.xml"

def get_anime_from_xml(only_non_completed = True, only_completed = False, all = False):
    anime_list = deque()

    DOMTree = parse(MYANIMELIST)
    collection = DOMTree.documentElement

    animes = collection.getElementsByTagName("anime")

    if only_non_completed == True and only_completed == False:
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


def conversor(raw_anime_list):
    anime_list = deque()

    largo = len(raw_anime_list)
    i = 1
    actual_name  = ''
    actual_score = 0

    for raw_anime in raw_anime_list:
        actual_anime = {'name':'','score':0}
        try:
            actual_anime = anime_info(raw_anime['id'])
        except:
            print('-second try-')
            sleep(5)
            try:
                actual_anime = anime_info(raw_anime['id'])
            except:
                print('error')
                continue

        if actual_anime['score'] == None:
            actual_anime['score'] = 0

        anime_list.append(actual_anime)

        if actual_anime['score'] > actual_score:
            actual_score = actual_anime['score']
            actual_name  = actual_anime['name']

        print(i, ' - ', round(i*100/largo,2),'%\t|', actual_score, '|',actual_name)
        i += 1
        sleep(3)
    return anime_list


def interfaz(anime_list):
    while True:
        o = input('sort by Score, Members, Favorites or Ratio? (s/m/f/r) -> ').lower()
        sorted_by = ""

        if o in ['exit','0']: break
        if o in ['score','s']: sorted_by = 'score'
        if o in ['members','m']: sorted_by = 'members'
        if o in ['favorites','f']: sorted_by = 'favorites'
        if o in ['ratio','r']: sorted_by = 'ratio'
        if o == 'p': print(sorted_list); continue


        sorted_list = sorted(anime_list, key=lambda d: d[sorted_by]) 
        for anime in sorted_list:
            print(f"{anime['score']}\t| {anime['members']}  \t| {anime['favorites']}     \t| {anime['ratio']}%\t| {anime['name']}")
        
        print('---------------------------------------------------------------------')
        print(f'score\t| members\t| favorites\t| ratio\t| sorted by {sorted_by.upper()}\n')
    
    print('bye!')


if __name__ == '__main__':

    o = input('use sample list? (y/n) -> ')

    if o == 'y':
        # these are my lists. used to test bc the conversor takes some time 
        from MAL_SORTING_SAMPLE_LISTS import COMPLETED_LIST, NON_COMPLETED_LIST

        l = input('Non-completed, Completed or All (sample list)? (n/c/a) -> ')

        if l == 'c':
            anime_list = COMPLETED_LIST
            anime_type = 'animes completed'
        elif l == 'a':
            all_list = []
            all_list.extend(NON_COMPLETED_LIST)
            all_list.extend(COMPLETED_LIST)
            anime_list = all_list
            anime_type = 'animes in total'
        else:
            anime_list = NON_COMPLETED_LIST
            anime_type = 'animes non-completed'

        print(f'{len(anime_list)} {anime_type}')

    else:
        a = input('Non-completed, Completed or All? (n/c/a) -> ')

        if a == 'c':
            raw_anime_list = get_anime_from_xml(only_completed=True)
            anime_type = 'animes completed'
        elif a == 'a':
            raw_anime_list = get_anime_from_xml(all=True)
            anime_type = 'animes in total'
        else:
            raw_anime_list = get_anime_from_xml()
            anime_type = 'animes non-completed'

        print(f'{len(raw_anime_list)} {anime_type}')
        anime_list = conversor(raw_anime_list)

    interfaz(anime_list)



