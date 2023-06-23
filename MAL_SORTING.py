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
                                                           Ybmmmd'     v1.3 
'''


# export your anime or manga list and write the dir/name down here
MYANIMELIST = "animelist_1687503240_-_10513306.xml"

def get_not_completed():
    anime_list = deque()

    DOMTree = parse(MYANIMELIST)
    collection = DOMTree.documentElement

    animes = collection.getElementsByTagName("anime")

    for anime in animes:
        if anime.getElementsByTagName('my_status')[0].childNodes[0].data != 'Completed':
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
        sleep(4)
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
        # this is my list. used to test bc the conversor takes some time 
        anime_list = [{'name': 'Kemurikusa (TV)', 'id': '37302', 'score': 7.06, 'members': 30068, 'favorites': 134, 'ratio': 0.45}, {'name': 'Shironeko Project: Zero Chronicle', 'id': '38843', 'score': 5.37, 'members': 91395, 'favorites': 200, 'ratio': 0.22}, {'name': 'Shikabane Hime: Aka', 'id': '4581', 'score': 7.19, 'members': 120662, 'favorites': 239, 'ratio': 0.2}, {'name': 'Blood: The Last Vampire', 'id': '405', 'score': 6.88, 'members': 107362, 'favorites': 245, 'ratio': 0.23}, {'name': 'Trigun: Badlands Rumble', 'id': '4106', 'score': 7.92, 'members': 137566, 'favorites': 253, 'ratio': 0.18}, {'name': 'Mahou Shoujo Madoka?Magica Movie 4: Walpurgis no Kaiten', 'id': '48820', 'score': 0, 'members': 53839, 'favorites': 257, 'ratio': 0.48}, {'name': 'Shuumatsu no Izetta', 'id': '33433', 'score': 6.75, 'members': 172987, 'favorites': 345, 'ratio': 0.2}, {'name': 'Mushoku Tensei: Isekai Ittara Honki Dasu - Eris no Goblin Toubatsu', 'id': '50360', 'score': 7.91, 'members': 132788, 'favorites': 487, 'ratio': 0.37}, {'name': 'Kodomo no Jikan (TV)', 'id': '2403', 'score': 6.71, 'members': 109384, 'favorites': 544, 'ratio': 0.5}, {'name': 'Ai no Utagoe wo Kikasete', 'id': '42847', 'score': 7.75, 'members': 86070, 'favorites': 625, 'ratio': 0.73}, {'name': 'Sirius', 'id': '37569', 'score': 6.98, 'members': 239572, 'favorites': 670, 'ratio': 0.28}, {'name': 'Magia Record: Mahou Shoujo Madoka?Magica Gaiden', 'id': '38256', 'score': 6.8, 'members': 152851, 'favorites': 801, 'ratio': 0.52}, {'name': 'Yarichin?Bitch-bu', 'id': '37585', 'score': 6.15, 'members': 100583, 'favorites': 823, 'ratio': 0.82}, {'name': 'Kemono Friends', 'id': '33089', 'score': 7.53, 'members': 79201, 'favorites': 1080, 'ratio': 1.36}, {'name': 'Juubee Ninpuuchou', 'id': '617', 'score': 7.61, 'members': 133616, 'favorites': 1086, 'ratio': 0.81}, {'name': 'Kidou Senshi Gundam: Suisei no Majo', 'id': '49828', 'score': 7.92, 'members': 123528, 'favorites': 1125, 'ratio': 0.91}, {'name': 'Bokura no', 'id': '1690', 'score': 7.61, 'members': 186083, 'favorites': 1171, 'ratio': 0.63}, {'name': 'Overflow', 'id': '40746', 'score': 7.23, 'members': 135475, 'favorites': 1253, 'ratio': 0.92}, {'name': 'Poputepipikku', 'id': '35330', 'score': 7.28, 'members': 217291, 'favorites': 1367, 'ratio': 0.63}, {'name': 'Araburu Kisetsu no Otome-domo yo.', 'id': '38753', 'score': 7.34, 'members': 321394, 'favorites': 1522, 'ratio': 0.47}, {'name': 'Trigun Stampede', 'id': '52093', 'score': 7.84, 'members': 140757, 'favorites': 1524, 'ratio': 1.08}, {'name': 'Oniichan wa Oshimai!', 'id': '51678', 'score': 7.71, 'members': 117547, 'favorites': 1541, 'ratio': 1.31}, {'name': 'Holo no Graffiti', 'id': '44042', 'score': 8.24, 'members': 52283, 'favorites': 1822, 'ratio': 3.48}, {'name': 'God Eater', 'id': '27631', 'score': 7.2, 'members': 531800, 'favorites': 1925, 'ratio': 0.36}, {'name': 'Dragon Ball GT', 'id': '225', 'score': 6.48, 'members': 607799, 'favorites': 1946, 'ratio': 0.32}, {'name': 'Blood Lad', 'id': '11633', 'score': 7.26, 'members': 668579, 'favorites': 2022, 'ratio': 0.3}, {'name': 'Flip Flappers', 'id': '32979', 'score': 7.64, 'members': 184790, 'favorites': 2116, 'ratio': 1.15}, {'name': 'Black?Rock Shooter (TV)', 'id': '11285', 'score': 6.8, 'members': 345668, 'favorites': 2208, 'ratio': 0.64}, {'name': 'BNA', 'id': '40060', 'score': 7.35, 'members': 347382, 'favorites': 2522, 'ratio': 0.73}, {'name': 'Sakamoto desu ga?', 'id': '32542', 'score': 7.55, 'members': 740795, 'favorites': 2579, 'ratio': 0.35}, {'name': 'Nazo no Kanojo X', 'id': '12467', 'score': 7.24, 'members': 301151, 'favorites': 3011, 'ratio': 1.0}, {'name': 'Ajin', 'id': '31580', 'score': 7.4, 'members': 570443, 'favorites': 3100, 'ratio': 0.54}, {'name': 'Btooom!', 'id': '14345', 'score': 7.29, 'members': 833513, 'favorites': 3355, 'ratio': 0.4}, {'name': 'Citrus', 'id': '34382', 'score': 6.45, 'members': 495760, 'favorites': 3744, 'ratio': 0.76}, {'name': 'Monster Musume no Iru Nichijou', 'id': '30307', 'score': 6.97, 'members': 724228, 'favorites': 3878, 'ratio': 0.54}, {'name': 'xxxHOLiC', 'id': '861', 'score': 7.98, 'members': 309509, 'favorites': 4393, 'ratio': 1.42}, {'name': 'Sayonara Zetsubou Sensei', 'id': '2605', 'score': 7.86, 'members': 335821, 'favorites': 4632, 'ratio': 1.38}, {'name': 'Karakai Jouzu no Takagi-san', 'id': '35860', 'score': 7.7, 'members': 566627, 'favorites': 5095, 'ratio': 0.9}, {'name': 'Watashi ga Motenai no wa Dou Kangaetemo Omaera ga Warui!', 'id': '16742', 'score': 7.0, 'members': 631913, 'favorites': 5419, 'ratio': 0.86}, {'name': 'Panty & Stocking with Garterbelt', 'id': '8795', 'score': 7.72, 'members': 376026, 'favorites': 5615, 'ratio': 1.49}, {'name': 'Kami no Tou', 'id': '40221', 'score': 7.55, 'members': 870258, 'favorites': 6186, 'ratio': 0.71}, {'name': 'Shirobako', 'id': '25835', 'score': 8.28, 'members': 431579, 'favorites': 6201, 'ratio': 1.44}, {'name': 'One Punch Man 2nd Season', 'id': '34134', 'score': 7.5, 'members': 1592189, 'favorites': 6288, 'ratio': 0.39}, {'name': 'Orange', 'id': '32729', 'score': 7.62, 'members': 791037, 'favorites': 6713, 'ratio': 0.85}, {'name': 'Kotonoha no Niwa', 'id': '16782', 'score': 7.89, 'members': 826976, 'favorites': 6829, 'ratio': 0.83}, {'name': 'Boruto: Naruto Next Generations', 'id':'34566', 'score': 6.06, 'members': 828468, 'favorites': 7091, 'ratio': 0.86}, {'name': 'Haibane Renmei', 'id': '387', 'score': 7.97, 'members': 272299, 'favorites': 7314, 'ratio': 2.69}, {'name': 'Magi: The Kingdom of Magic', 'id': '18115', 'score': 8.22, 'members': 814888, 'favorites': 7597, 'ratio': 0.93}, {'name': 'Mononoke', 'id': '2246', 'score': 8.43, 'members': 309486, 'favorites': 7778, 'ratio': 2.51}, {'name': 'Vinland Saga Season 2', 'id': '49387', 'score': 8.84, 'members': 434861, 'favorites': 7783, 'ratio': 1.79}, {'name': 'Dorohedoro', 'id': '38668', 'score': 8.06, 'members': 508382, 'favorites': 8091, 'ratio': 1.59}, {'name': 'Danganronpa: Kibou no Gakuen to Zetsubou no Koukousei The Animation', 'id': '16592', 'score': 7.21, 'members': 908382, 'favorites': 8168, 'ratio': 0.9}, {'name': 'Claymore', 'id': '1818', 'score': 7.74, 'members': 650934, 'favorites': 8257, 'ratio': 1.27}, {'name': 'Mob Psycho 100 III', 'id': '50172', 'score': 8.72, 'members': 571990, 'favorites': 8843, 'ratio': 1.55}, {'name': 'Enen no Shouboutai', 'id': '38671', 'score': 7.71, 'members': 1252822, 'favorites': 8934, 'ratio': 0.71}, {'name': 'Koukyoushihen Eureka Seven', 'id': '237', 'score': 8.06, 'members': 426859, 'favorites': 9031, 'ratio': 2.12}, {'name': "Vivy: Fluorite Eye's Song", 'id': '46095', 'score': 8.41, 'members': 497302, 'favorites': 10005, 'ratio': 2.01}, {'name': 'Kage no Jitsuryokusha ni Naritakute!', 'id': '48316', 'score': 8.33, 'members': 475859, 'favorites': 10170, 'ratio': 2.14}, {'name': 'Katanagatari', 'id': '6594', 'score': 8.31, 'members': 545517, 'favorites': 10711, 'ratio': 1.96}, {'name': 'Byousoku 5 Centimeter', 'id': '1689', 'score': 7.58, 'members': 910731, 'favorites': 10757, 'ratio': 1.18}, {'name': 'Re:Zero kara Hajimeru Isekai Seikatsu 2nd Season', 'id': '39587', 'score': 8.34, 'members': 1043689, 'favorites': 11361, 'ratio': 1.09}, {'name': 'Jibaku Shounen Hanako-kun', 'id': '39534', 'score': 7.84, 'members': 555719, 'favorites': 11427, 'ratio': 2.06}, {'name': 'Plastic Memories', 'id': '27775', 'score': 7.91, 'members': 905209, 'favorites': 11521, 'ratio': 1.27}, {'name': 'Youjo Senki', 'id': '32615', 'score': 7.96, 'members': 868844, 'favorites': 11736, 'ratio': 1.35}, {'name': 'Re:Zero kara Hajimeru Isekai Seikatsu 2nd Season Part 2', 'id': '42203', 'score': 8.44, 'members': 819296, 'favorites': 11935, 'ratio': 1.46}, {'name': 'Houseki no Kuni', 'id': '35557', 'score': 8.39, 'members': 434904, 'favorites': 12675, 'ratio': 2.91}, {'name': 'Golden Time', 'id': '17895', 'score': 7.74, 'members': 990797, 'favorites': 12716, 'ratio': 1.28}, {'name': 'Fumetsu no Anata e', 'id': '41025', 'score': 8.36, 'members': 813211, 'favorites': 13659, 'ratio': 1.68}, {'name': 'Trigun', 'id': '6', 'score': 8.22, 'members': 727770, 'favorites': 15055, 'ratio': 2.07}, {'name': 'Natsume Yuujinchou', 'id': '4081', 'score': 8.31, 'members': 519610, 'favorites': 15228, 'ratio': 2.93}, {'name': 'Fate/stay night: Unlimited Blade Works', 'id': '22297', 'score': 8.19, 'members': 1024935, 'favorites': 16078, 'ratio': 1.57}, {'name': 'Guilty Crown', 'id': '10793', 'score': 7.42, 'members': 1181578, 'favorites': 16861, 'ratio': 1.43}, {'name': 'Another', 'id': '11111', 'score': 7.48, 'members': 1606236, 'favorites': 17085, 'ratio': 1.06}, {'name': 'Chuunibyou demo Koi ga Shitai!', 'id': '14741', 'score': 7.71, 'members': 1305941, 'favorites': 17479, 'ratio': 1.34}, {'name': 'Kaguya-sama wa Kokurasetai? Tensai-tachi no Renai Zunousen', 'id': '40591', 'score': 8.64, 'members': 1259288, 'favorites': 18683, 'ratio': 1.48}, {'name': 'Dororo', 'id': '37520', 'score': 8.24, 'members': 1148254, 'favorites': 19507, 'ratio': 1.7}, {'name': 'Yuri!!! on Ice', 'id': '32995', 'score': 7.9, 'members': 850535, 'favorites': 20187, 'ratio': 2.37}, {'name': 'Higurashi no Naku Koro ni', 'id': '934', 'score': 7.89, 'members': 780829, 'favorites': 20786, 'ratio': 2.66}, {'name': 'Bocchi the Rock!', 'id': '47917', 'score': 8.85, 'members': 427829, 'favorites': 20966, 'ratio': 4.9}, {'name': 'Shinsekai yori', 'id': '13125', 'score': 8.28, 'members': 756361, 'favorites': 21782, 'ratio': 2.88}, {'name': 'Kuroshitsuji', 'id': '4898', 'score': 7.66, 'members': 1137194, 'favorites': 22099, 'ratio': 1.94}, {'name': 'K-On!', 'id': '5680', 'score': 7.85, 'members': 1015571, 'favorites': 23317, 'ratio': 2.3}, {'name': 'Kimetsu no Yaiba: Yuukaku-hen', 'id': '47778', 'score': 8.8, 'members': 1248346, 'favorites': 23498, 'ratio': 1.88}, {'name': 'Bungou Stray Dogs', 'id': '31478', 'score': 7.82, 'members': 1301730, 'favorites': 25292, 'ratio': 1.94}, {'name': 'Great Teacher Onizuka', 'id': '245', 'score': 8.69, 'members': 788773, 'favorites': 25298, 'ratio': 3.21}, {'name': 'Tate no Yuusha no Nariagari', 'id': '35790', 'score': 7.98, 'members': 1499146, 'favorites': 25338, 'ratio': 1.69}, {'name': 'Mushishi', 'id': '457', 'score': 8.66, 'members': 794444, 'favorites': 25963, 'ratio': 3.27}, {'name': 'Clannad', 'id': '2167', 'score': 8.0, 'members': 1372167, 'favorites': 27262, 'ratio': 1.99}, {'name': 'Saiki Kusuo no ?-nan', 'id': '33255','score': 8.42, 'members': 1037306, 'favorites': 27662, 'ratio': 2.67}, {'name': 'Ansatsu Kyoushitsu', 'id': '24833', 'score': 8.09, 'members': 1916204, 'favorites': 28762, 'ratio': 1.5}, {'name': 'Banana Fish', 'id': '36649', 'score': 8.48, 'members': 811168, 'favorites': 28983, 'ratio': 3.57}, {'name': 'Ano Hi Mita Hana no Namae wo Bokutachi wa Mada Shiranai.', 'id': '9989', 'score': 8.31, 'members': 1554935, 'favorites': 32235, 'ratio': 2.07}, {'name': 'Psycho-Pass', 'id': '13601', 'score': 8.34, 'members': 1569522, 'favorites': 37773, 'ratio': 2.41}, {'name': 'Black Clover', 'id': '34572', 'score': 8.14, 'members': 1552832, 'favorites': 43742, 'ratio': 2.82}, {'name': 'Monster', 'id': '19', 'score': 8.87, 'members': 1014632, 'favorites': 47323, 'ratio': 4.66}, {'name': 'Angel Beats!', 'id': '6547', 'score': 8.06, 'members': 2011237, 'favorites': 47655, 'ratio': 2.37}, {'name': 'Clannad: After Story', 'id': '4181', 'score': 8.93, 'members': 1150491, 'favorites': 68955, 'ratio': 5.99}, {'name': 'Shigatsu wa Kimi no Uso', 'id': '23273', 'score': 8.65, 'members': 2113295, 'favorites': 83589, 'ratio': 3.96}]
    else:
        raw_anime_list = get_not_completed()

        print(f'{len(raw_anime_list)} animes non-completed')
        anime_list = conversor(raw_anime_list)

    interfaz(anime_list)



