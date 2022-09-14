import json
from enum import Enum, auto
from typing import Dict, Any, List
from emora_stdm import KnowledgeBase, DialogueFlow, Macro, Ngrams, NatexNLU
import random
import spotipy as sp
import copy

# WHAT HAPPENS IF SPOTIFY THROWS ERROR????

client_id = '864c6b7042764ea3aad0b5fab6536a3b'  # Your client id
client_secret = '8b4238f74bf446359cd6876b75c29e12'  # Your secret
redirect_uri = 'http://localhost:8888/callback'  # Your redirect uri

# TODO: Update the State enum as needed
class State(Enum):
    START = auto()
    RES = auto()
    RES2 = auto()
    RES_ERROR = auto()
    RES_ERROR2 = auto()
    NO = auto()
    NO_ANS = auto()
    MUSIC_GOOD = auto()
    MUSIC_OPINION = auto()
    AGREE = auto()
    DISAGREE = auto()
    UNKNOWN = auto()
    NEUT = auto()
    YES = auto()
    VERB = auto()
    VERBRES = auto()
    TIMERES = auto()
    SHOWER = auto()
    CAR = auto()
    PLANE = auto()
    GYM = auto()
    VERB2 = auto()
    ACT_ERROR = auto()
    ACT_ERROR2 = auto()
    SERVICE = auto()
    STREAM = auto()
    OTHERSTREAM2 = auto()
    STREAM_ERROR = auto()
    STREAM_ERROR2 = auto()
    CDS = auto()
    VINYLS = auto()
    OTHERMED = auto()
    SERV_ERROR = auto()
    SERV_ERROR2 = auto()
    SERVICE2 = auto()
    SERVICE2MIDNO = auto()
    ARTIST = auto()
    PANDORA = auto()
    APPLE = auto()
    AMAZON = auto()
    YOUTUBE = auto()
    SPOTIFY = auto()
    SPOTIPULL = auto()
    SPOTIERR = auto()
    YESPULL = auto()
    TAYLORSWIFT = auto()
    NOSERVICE = auto()
    OTHERSTREAM = auto()
    DISCOUNT = auto()
    PLAYLIST = auto()
    CONVENIENCE = auto()
    SELECTION = auto()
    SHOWS = auto()
    DOWNLOAD = auto()
    DISCOVERY = auto()
    END = auto()
    ERR = auto()
    ARTIST_ERROR = auto()
    NOUNRES = auto()
    PLACERES = auto()
    GENREQUESTION = auto()
    GENREQUESTION2 = auto()
    ARTISTTOMUSIC = auto()
    ROCK = auto()
    OTHERMUSIC = auto()
    ROCKDYING = auto()
    ROCKDYING2 = auto()
    ROCK_ERROR = auto()
    ROCK_ERROR2 = auto()
    ROCK_ERROR3 = auto()
    ROCK_ERROR4 = auto()
    ROCKAGREE = auto()
    ROCKDISAGREE = auto()
    POPULARITY = auto()
    POPULARITY2 = auto()
    POPROCKBANDS = auto()
    POPROCKBANDS2 = auto()
    ROCK_ERROR5 = auto()
    ROCK_ERROR6 = auto()
    ROCK_ERROR7 = auto()
    ROCK_ERROR8 = auto()
    ROCKIMAGE = auto()
    ROCKANS = auto()
    ROCKANS2 = auto()
    ROCK_ERROR9 = auto()
    ROCK_ERROR10 = auto()
    ROCKREPRESENT = auto()
    ROCKCOSTLY = auto()
    DIFFSOUND = auto()
    ROCKDONTKNOW = auto()
    ROCKARTISTS = auto()
    ROCKSTORY = auto()
    ROCKINSTRUMENTS = auto()
    YESAGING = auto()
    NOAGING = auto()
    AGINGIDK = auto()
    ROCKSONG = auto()
    ROCKSONG2 = auto()
    SONGARTIST = auto()
    #SONGARTISTOPIN = auto()
    ROCK_ERROR11 = auto()
    ROCK_ERROR12 = auto()
    SONGARTIST1 = auto()
    ROCKCONCERT = auto()
    ROCKTICKETS = auto()
    ROCKDONTKNOW2 = auto()
    TM_START = auto()
    #TM_START2 = auto()
    TM_TMSTART = auto()
    TM_CONCERT = auto()
    TM_YESCONCERT = auto()
    TM_NOCONCERT = auto()
    TM_LIVEARTIST = auto()
    TM_LIVERES = auto()
    TM_KENDRICK = auto()
    TM_ED = auto()
    TM_CONCOP = auto()
    TM_CONCADJ = auto()
    TM_CONCADJS = auto()
    TM_CONCADJSN = auto()
    TM_CONCFAV = auto()
    TM_RANDARTIST = auto()
    TM_FREQ = auto()
    TM_NFREQ = auto()
    TM_TM = auto()
    TM_PRICEYES = auto()
    TM_PRICENO = auto()
    TM_TMPRICE = auto()
    TM_NFREQRES = auto()
    TM_USEDY = auto()
    TM_USEDN = auto()
    TM_STATS = auto()
    TM_YSTATS = auto()
    TM_NSTATS = auto()
    TM_MONO = auto()
    TM_YESFAIR = auto()
    TM_NOFAIR = auto()
    TM_CEO = auto()
    TM_LAW = auto()
    TM_SUGG = auto()
    TM_SUGGLAW = auto()
    TM_ERRFREQ = auto()
    TM_BOYCOTT = auto()
    TM_SUGG_ERR = auto()
    TM_END = auto()
    TM_ERR1 = auto()
    TM_ERR2 = auto()
    TM_ERR3 = auto()
    TM_ERR4 = auto()
    TM_ERR5 = auto()
    TM_ERR7 = auto()
    TM_ERR8 = auto()
    S_INDIE = auto()
    U_INDIE = auto()
    S_INDIE_LESS = auto()
    S_INDIE_EQUAL = auto()
    S_INDIE_MORE = auto()
    U_INDIE_2 = auto()
    S_INDIE_3A = auto()
    S_INDIE_3B = auto()
    U_INDIE_3A = auto()
    U_INDIE_3B = auto()
    S_INDIE_3E = auto()
    U_INDIE_3E = auto()
    S_INDIE_4A = auto()
    S_INDIE_4B = auto()
    #U_INDIE_4A = auto()
    #U_INDIE_4B = auto()
    S_INDIE_4E = auto()
    #S_INDIE_5A = auto()
    #S_INDIE_5B = auto()
    #S_INDIE_5E = auto()
    U_INDIE_5E = auto()
    U_FEAT_START = auto()
    S_ARTIST_FEAT_2 = auto()
    U_ARTIST_FEAT_2 = auto()
    S_ARTIST_FEAT_3 = auto()
    S_ARTIST_FEAT_3_ERR = auto()
    U_ARTIST_FEAT_3_ERR = auto()
    S_ARTIST_FEAT_3_ERR2 = auto()
    U_ARTIST_FEAT_3 = auto()
    S_ARTIST_FEAT_4_YES = auto()
    S_ARTIST_FEAT_4_NO = auto()
    U_ALBUM = auto()
    S_ALBUM = auto()
    U_ALBUM_2 = auto()
    S_ALBUM_3_NO = auto()
    U_ALBUM_3 = auto()
    S_ALBUM_3_YES = auto()
    S_ALBUM_3_ERR = auto()
    U_ALBUM_3_ERR = auto()
    S_ALBUM_3_ERR2 = auto()
    S_ALBUM_ERR = auto()
    U_ALBUM_ERR = auto()
    S_ALBUM_ERR2 = auto()
    ARTIST_ERR1 = auto()
    U_ARTIST_ERR1 = auto()
    S_ARTIST_FEAT_4_ERR = auto()
    U_ARTIST_FEAT_4_ERR = auto()
    S_ALBUM_FROM_ERR = auto()

    S_ALBUMERR = auto()
    U_ALBUMERR = auto()
    PRE_TM = auto()
    STR_SERVICE = auto()
    STR_YESSTREAM = auto()
    STR_NOSTREAM = auto()
    STR_POPULAR = auto()
    STR_GUESS2008 = auto()
    STR_ARTISTREV = auto()
    STR_GUESS = auto()
    STR_MORE = auto()
    STR_LESS = auto()
    STR_SONG = auto()
    STR_YESSONG = auto()
    STR_NOSONG = auto()
    STR_SONGINFO = auto()
    STR_LISTENER = auto()
    STR_ACCESS = auto()
    STR_NORES = auto()
    STR_ERR1 = auto()
    STR_ERR2 = auto()
    STR_ERR3 = auto()
    STR_ERR4 = auto()
    STR_ERR5 = auto()
    STR_ERR6 = auto()
    STR_SONGINFO2 = auto()
    SERVICE2MID = auto()
    # HipHop
    HIPHOP_START = auto()
    HIPHOP_Q1 = auto()
    HIPHOP_RESP1a = auto()
    HIPHOP_RESP1b = auto()
    HIPHOP_Q2a = auto()
    HIPHOP_RESP2a = auto()
    HIPHOP_EXIT1 = auto()
    HIPHOP_Q2b = auto()
    HIPHOP_RESP2b_a = auto()
    HIPHOP_RESP2b_b = auto()
    HIPHOP_RESP2b_c = auto()
    HIPHOP_Q3a = auto()
    HIPHOP_RESP3a_a = auto()
    HIPHOP_Q4 = auto()
    HIPHOP_RESP3a_b = auto()
    HIPHOP_RESP3a_c = auto()
    HIPHOP_Q3a_e = auto()
    HIPHOP_RESP4 = auto()

    VERBUNK = auto()
    SERVICEUNK = auto()
    OTHERSTREAMUNK = auto()
    STR_SERVICEUNK = auto()
    STR_GUESSUNK = auto()
    STR_ARTISTREVUNK = auto()
    STR_NORESUNK = auto()
    GENREUNK = auto()
    U_INDIEUNK = auto()
    U_INDIE_2UNK = auto()
    TM_TMUNK = auto()
    TM_SUGGUNK = auto()


empty_feature_dict = {
    'danceability': 0,
    'energy': 0,
    'key': 0,
    'loudness': 0,
    'mode': 0,
    'speechiness': 0,
    'acousticness': 0,
    'instrumentalness': 0,
    'liveness': 0,
    'valence': 0,
    'tempo': 0
}

features_to_descriptors = {
    'danceability': {
        (0, 0.33): ['slow', 'downtempo', 'flowing', 'calm', 'mellow'],
        (0.33, 0.67): ['rhythmic', 'dreamy', 'smooth', 'chill'],
        (0.67, 1.0): ['groovy', 'fun to dance to', 'lively', 'alive', 'active', 'bouncy']
    },
    'energy': {
        (0, 0.33): ['calm', 'chill', 'relaxed', 'easygoing', 'mellow'],
        (0.33, 0.67): ['full', 'cool', 'dreamy', 'atmospheric', 'smooth', 'gentle', 'airy', 'light', 'slick'],
        (0.67, 1.0): ['energetic', 'uptempo', 'spirited', 'explosive', 'electric', 'upbeat']
    },
    'acousticness': {
        (0.88, 1.0): ['soft', 'delicate']  # maybe adjust this parameter based on observations
    },
    'valence': {
        (0, 0.12): ['solemn'],
        (0, 0.33): ['emotional', 'soulful', 'moody', 'melancholy', 'heavy', 'sad'],
        (0.33, 0.67): ['nuanced', 'melodic', 'thoughtful', 'heartfelt', 'soulful', 'introspective', 'honest', 'reflective'],
        (0.67, 1.0): ['upbeat', 'positive', 'happy', 'warm', 'pleasant', 'light', 'bubbly', 'bright'],
        (0.88, 1.0): ['euphoric']
    }
    # TODO: Add tempo if there is time, although not as strong a descriptive
}

class requester:

    def __init__(self):
        self.cl = sp.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.auth_token = self.cl.get_access_token()
        self.spotify = sp.Spotify(auth=self.auth_token)

    def search_for_song(self, track: str, artist: str = None):
        """
        Given a track and an artist, returns a list of track objects that
        Spotify api returns when searching for the song. Limited to size 10.
        :param track: name of the track
        :param artist: name of the artist (optional, default set to None)
        :return: List of spotify track dictionary objects
        """
        if artist:
            query_str = "track:" + track + " artist:" + artist
        else:
            query_str = "track:" + track
        user_q = self.spotify.search(query_str, type="track", limit=2)
        user_object = user_q['tracks']
        user_results = user_object['items']
        return user_results

    def search_for_album(self, album: str, artist: str = None):
        """
        Given an albums title and an artist, returns a list of track objects that
        Spotify api returns when searching for the song. Limited to size 10.
        :param album: name of the album
        :param artist: name of the artist (optional, default set to None)
        :return: List of spotify track dictionary objects
        """
        if artist:
            query_str = "album:" + album + " artist:" + artist
        else:
            query_str = "album:" + album
        user_q = self.spotify.search(query_str, type="album", limit=2)
        user_object = user_q['albums']
        user_results = user_object['items']
        return user_results

    def search_for_artist(self, artist: str):
        """
        Given an artist name or search terms for an artist,
        return a list of potential artists that the user is looking for
        :param artist: the name of the artist
        :return: a list of the artists that could match the query
        """
        query_str = "artist:" + artist
        user_q = self.spotify.search(query_str, type="artist", limit=2)
        user_object = user_q['artists']
        user_results = user_object['items']
        return user_results

    def get_song_features(self, track_id: str):
        """
        Given a song's track id, return its features
        :param track_id: the spotify id of the track
        :return: a dictionary of features for the inputted track
        """
        features_dict = copy.deepcopy(empty_feature_dict)
        track_feats = self.spotify.audio_features(track_id)[0]
        for feat in features_dict:
            features_dict[feat] = track_feats[feat]
        return track_feats

    def get_album_avg_features(self, album_id):
        """
        given an album_id, return the average of each
        quantitative feature by aggregating over all the tracks in the album
        :param album_id: the id of the album
        :return: a dictionary mapping features to their average across the album's tracks
        """
        tracks_query = self.spotify.album_tracks(album_id)
        track_list = tracks_query['items']
        features_dict = copy.deepcopy(empty_feature_dict)
        for track in track_list:
            cur_id = track['id']
            cur_feats = self.get_song_features(cur_id)
            for feat in features_dict:
                features_dict[feat] += cur_feats[feat]
        for feat in features_dict:
            features_dict[feat] /= len(track_list)
        return features_dict

    def get_artist_avg_features(self, artist_id):
        """
        aggregating over an artist's top 10 tracks, return the average features of those tracks
        :param artist_id: the id of the artist
        :return: a dictionary mapping features to their average across the artist's tracks
        """
        tracks_query = self.spotify.artist_top_tracks(artist_id)
        track_list = tracks_query['tracks']
        features_dict = copy.deepcopy(empty_feature_dict)
        for track in track_list:
            cur_id = track['id']
            cur_feats = self.get_song_features(cur_id)
            for feat in features_dict:
                features_dict[feat] += cur_feats[feat]
        for feat in features_dict:
            features_dict[feat] /= len(track_list)
        return features_dict

    def get_artist_genres(self, artist_name):
        """
        given an artist's name, return a list of genres associated with that artist
        :param artist_name: the name of the artist
        :return: list of genres associated with the artist
        """
        artist = self.search_for_artist(artist_name)[0]
        if 'genres' not in artist or len(artist['genres']) == 0:
            return ['musical']
        return artist['genres']  # REMEMBER, THIS IS A LIST

sp_requester = requester()

genre_to_natex = {
    'indie': '[{indie,independent}]',
    'hiphop': '[{hiphop, hip hop, rap}]',
    'pop': '[pop]',
    'rock': '[rock]',
    'other': '<-indie, -independent, -hiphop, -"hip hop", -rap, -pop, -rock>'
}

class ARTIST_GENRE(Macro):

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        if 'fav_artist' in vars:
            fav_artist_name = vars['fav_artist']
            artist_genres = sp_requester.get_artist_genres(fav_artist_name)
            #print(artist_genres)
            indie_natex = NatexNLU('[indie]')
            hip_hop_natex = NatexNLU('[hip hop]')
            pop_natex = NatexNLU('[pop]')
            rock_natex = NatexNLU('[rock]')
            chosen_genre = 'unknown'
            random.shuffle(artist_genres)  # shuffle to mix up genres that might have multiple matches
            for genre in artist_genres:
                if indie_natex.match(genre):
                    chosen_genre = 'independent'
                    break
                elif rock_natex.match(genre):
                    chosen_genre = 'rock'
                    break
                elif hip_hop_natex.match(genre):
                    #print(hip_hop_natex.match(genre))
                    chosen_genre = 'hip hop'
                    break
                elif pop_natex.match(genre):
                    chosen_genre = 'pop'
                    break
                #elif: TODO: add elif statements for other natex genre matches

            if chosen_genre == 'unknown':
                chosen_genre = artist_genres[0]
            # returns the first genre in the artists' genre list as the artist-specific genre, store matched genre later
            # to branch to genre-specific conversation
            vars['artist_genre'] = artist_genres[0]
            vars['genre'] = chosen_genre
            #print(vars['genre'])
            return vars['artist_genre']

class ARTIST_QUALITIES(Macro):

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        if 'fav_artist' in vars:
            fav_artist_name = vars['fav_artist']
            #print(fav_artist_name)
            query = sp_requester.search_for_artist(fav_artist_name)
            query_first_result = query[0]
            artist_id = query_first_result['id']
            artist_features = sp_requester.get_artist_avg_features(artist_id)
            # these next two lines are for testing. Remove once macro is up and running
            artist_descriptors = []
            for feature, value in artist_features.items():
                if feature in features_to_descriptors:
                    val_dict = features_to_descriptors[feature]
                    for val_range in val_dict:
                        low, high = val_range
                        if low <= value <= high:
                            artist_descriptors.extend(val_dict[val_range])
            #print(artist_descriptors)
            vars['artist_descriptors'] = artist_descriptors
            if len(artist_descriptors) < 2:
                return artist_descriptors[0]
            desc_sub = set()
            while len(desc_sub) < 2:
                new_desc = random.choice(artist_descriptors)
                desc_sub.add(new_desc)
            desc_list = list(desc_sub)
            descriptive_string = ' and '.join(desc_list)
            return descriptive_string

class ALBUM_QUALITIES(Macro):

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        if 'fav_album' in vars:
            fav_album_name = vars['fav_album']
            fav_album_artist = vars['fav_album_artist']
            query = sp_requester.search_for_album(fav_album_name, fav_album_artist)
            query_first_result = query[0]
            album_id = query_first_result['id']
            album_features = sp_requester.get_album_avg_features(album_id)
            # these next two lines are for testing. Remove once macro is up and running
            album_descriptors = []
            for feature, value in album_features.items():
                if feature in features_to_descriptors:
                    val_dict = features_to_descriptors[feature]
                    for val_range in val_dict:
                        low, high = val_range
                        if low <= value <= high:
                            album_descriptors.extend(val_dict[val_range])
            #print(artist_descriptors)
            vars['album_descriptors'] = album_descriptors
            if len(album_descriptors) < 2:
                return album_descriptors[0]
            desc_sub = set()
            while len(desc_sub) < 2:
                new_desc = random.choice(album_descriptors)
                desc_sub.add(new_desc)
            desc_list = list(desc_sub)
            descriptive_string = ' and '.join(desc_list)
            return descriptive_string

class SONG_QUALITIES(Macro):

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        try:
            if 'fav_track_for_artist' in vars and 'fav_artist' in vars:
                track_name = vars['fav_track_for_artist']
                artist_name = vars['fav_artist']
                #print(fav_artist_name)
                query = sp_requester.search_for_song(track_name, artist_name)
                query_first_result = query[0]
                track_id = query_first_result['id']
                track_features = sp_requester.get_song_features(track_id)
                # these next two lines are for testing. Remove once macro is up and running
                track_descriptors = []
                for feature, value in track_features.items():
                    if feature in features_to_descriptors:
                        val_dict = features_to_descriptors[feature]
                        for val_range in val_dict:
                            low, high = val_range
                            if low <= value <= high:
                                track_descriptors.extend(val_dict[val_range])
                #print(artist_descriptors)
                vars['track_descriptors'] = track_descriptors
                if len(track_descriptors) < 2:
                    return track_descriptors[0]
                desc_sub = set()
                while len(desc_sub) < 2:
                    new_desc = random.choice(track_descriptors)
                    desc_sub.add(new_desc)
                desc_list = list(desc_sub)
                descriptive_string = ' and '.join(desc_list)
                vars['fav_song_descript'] = descriptive_string
                return descriptive_string
            return " good"
        except Exception as e:
            return " good"

class FIND_ARTIST(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        potential_artist = []
        maxTokens = 0
        pre = Ngrams('i like i enjoy probably i really like listening to my favorite artist is im a fan of')
        tempGrams = ngrams.difference(pre)
        for n in tempGrams:
            numTokens = len(n.split())
            if numTokens >= maxTokens:
                query_res = sp_requester.search_for_artist(n)
                if len(query_res) > 0:
                    result = query_res[0]
                    if numTokens > maxTokens and result['genres'] != []:
                        maxTokens = numTokens
                        potential_artist.clear()
                        potential_artist.append(result)
                    elif numTokens == maxTokens:
                        potential_artist.append(result)
        if len(potential_artist) == 0:
            return False
        max_popularity = 0
        chosen_artist = potential_artist[0]
        for res in potential_artist:        #  break ties with popularity
            if res['popularity'] > max_popularity:
                chosen_artist = res
                max_popularity = res['popularity']
                #print("chosen: "+chosen_artist['name'])
                vars['fav_artist'] = chosen_artist['name']
        #print(chosen_artist)
        return True

class FIND_SONG(Macro):

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        potential_track = []
        maxTokens = 0
        artist = vars['fav_artist']
        pre_str = 'i like i enjoy probably i really like my favorite song is'
        pre = Ngrams(pre_str)
        tempGrams = ngrams.difference(pre)
        for n in tempGrams:
            numTokens = len(n.split())
            if numTokens >= maxTokens:
                query_res = sp_requester.search_for_song(n, artist)
                if len(query_res) > 0:
                    result = query_res[0]
                    if numTokens > maxTokens:
                        maxTokens = numTokens
                        potential_track.clear()
                        potential_track.append(result)
                    elif numTokens == maxTokens:
                        potential_track.append(result)
        if len(potential_track) == 0:
            return False
        max_popularity = 0
        chosen = potential_track[0]
        for res in potential_track:
            if res['popularity'] > max_popularity:
                chosen_track = res
                max_popularity = res['popularity']
                vars['fav_track_for_artist'] = chosen_track['name']
        return True

class FIND_ALBUM(Macro):

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        potential_album = []
        temp_vars = {}
        pre_str = 'i like i enjoy probably i really like my favorite album is'
        pre = Ngrams(pre_str)
        maxTokens = 0
        input = ngrams.text()
        queries = input.split("by ")
        if len(queries) == 1:
            album_title_tokens = Ngrams(queries[0])
            artist_name = None
        else:
            album_title_tokens = Ngrams(queries[0]).difference(pre)
            artist_name = queries[1]

        for n_album in album_title_tokens:
            query_res = sp_requester.search_for_album(n_album, artist_name)
            if len(query_res) > 0 and len(n_album.split()) >= maxTokens:
                if len(n_album.split()) > maxTokens:
                    maxTokens = len(n_album.split())
                    potential_album.clear()
                potential_album.append(query_res[0])
               #print(query_res[0])
        if len(potential_album) == 0:
            return False
        vars['fav_album'] = potential_album[0]['name']
        vars['fav_album_artist'] = potential_album[0]['artists'][0]['name']
        return True

class CONCERT_FIND_ARTIST(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        potential_artist = []
        maxTokens = 0
        pre = Ngrams('ive always wanted to see i want to watch i have seen')
        tempGrams = ngrams.difference(pre)
        for n in tempGrams:
            numTokens = len(n.split())
            if numTokens >= maxTokens:
                query_res = sp_requester.search_for_artist(n)
                if len(query_res) > 0:
                    result = query_res[0]
                    if numTokens > maxTokens:
                        maxTokens = numTokens
                        potential_artist.clear()
                        potential_artist.append(result)
                    elif numTokens == maxTokens:
                        potential_artist.append(result)
        if len(potential_artist) == 0:
            return False
        max_popularity = 0
        chosen_artist = potential_artist[0]
        for res in potential_artist:        #  break ties with popularity
            if res['popularity'] > max_popularity:
                chosen_artist = res
                max_popularity = res['popularity']
                # print("chosen: "+chosen_artist['name'])
                vars['live_artist'] = chosen_artist['name']
                vars['live_artist2'] = chosen_artist['name']
        # print(chosen_artist)
        return True

class GENRE_MATCH_VARS(Macro):

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        genre_to_match = args[0]
        genre_ntx = NatexNLU(genre_to_natex[genre_to_match])
        cur_genre = vars['genre']
        m = genre_ntx.match(cur_genre)
        return m is not None

class GENRE_MATCH_INPUT(Macro):

    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        #print(args)
        genre_to_match = args[0]
        genre_ntx = NatexNLU(genre_to_natex[genre_to_match])
        m = genre_ntx.match(ngrams.text())
        #print(m)
        return m is not None


# TODO: create the ontology as needed
ont = {
  "ontology": {
    "no": [
      "no",
      "nah",
      "never",
      "not anymore",
      "no way",
      "get out",
      "nope",
      "not really",
      "maybe not"
    ],
    "yes": [
      "yes",
      "yeah",
      "yea",
      "sometimes",
      "at times",
      "always",
      "usually",
      "sure",
      "absolutely",
      "of course",
      "ye",
      "yeet",
      "yep",
      "yup",
      "definitely",
      "normally",
      "all the time",
      "i do",
      "i agree",
      "maybe",
      "agreed",
      "a little bit",
      "i think so"
    ],
    "greetings": [
      "hi",
      "hello",
      "good morning",
      "good afternoon",
      "good evening",
      "hey",
      "nice to meet you",
      "good day"
    ],
    "negative_response": [
      "don't like",
      "do not like",
      "boring",
      "dislike",
      "sucks",
      "bad",
      "slow",
      "annoying",
      "old",
      "awful",
      "horrible",
      "no good",
      "terrible",
      "disproportionate",
      "unfair",
      "hate",
      "problematic",
      "nebulous",
      "uncertain",
      "gross",
      "rude",
      "difficult",
      "hard",
      "harder",
      "worse",
      "tough",
      "tougher",
      "negative"
    ],
    "mixed_response": [
      "complicated",
      "good and bad",
      "split",
      "indifferent",
      "mixed",
      "neutral",
      "bad and good",
      "maybe",
      "not sure",
      "kind of",
      "i dont know",
      "shorter songs"
    ],
    "positive_response": [
      "good",
      "amazing",
      "terrific",
      "fast",
      "new",
      "great",
      "fun",
      "easy",
      "fabulous",
      "fantastic",
      "wonderful",
      "efficient",
      "revolutionary",
      "successful",
      "cool",
      "limitless",
      "tantalizing",
      "crucial",
      "cheap",
      "inexpensive",
      "beneficial",
      "widespread",
      "improved",
      "enhanced",
      "better",
      "easier",
      "cooler",
      "positive",
      "wide variety"
    ],
    "genres": [
      "rock",
      "pop",
      "metal",
      "disco",
      "edm",
      "rap",
      "hip-hop",
      "funk",
      "classical",
      "jazz",
      "punk",
      "musical theater",
      "soundtrack",
      "broadway",
      "alternative",
      "indie",
      "k-pop",
      "folk",
      "blues",
      "reggae",
      "calypso",
      "techno",
      "ska",
      "mongolian throat singing",
      "RnB",
      "pop punk",
      "math rock",
      "dance",
      "acid house",
      "house",
      "deep house",
      "lofi",
      "nu metal",
      "progressive rock",
      "progressive metal",
      "holiday",
      "vaporwave",
      "soundcloud rap",
      "trap",
      "emo",
      "caribbean",
      "latin",
      "opera"
    ],
    "instrument": [
      "guitar",
      "bass",
      "drums",
      "drum machine",
      "synth",
      "piano",
      "triangle",
      "trumpet",
      "french horn",
      "euphonium",
      "flute",
      "bagpipes"
    ],
    "services": [
      "spotify",
      "pandora",
      "deezer",
      "apple music",
      "napster",
      "youtube",
      "amazon music"
    ],
    "mediums": [
      "cd",
      "disk",
      "tape",
      "walkman",
      "radio",
      "boombox",
      "itunes",
      "mp3 player",
      "ipod",
      "mp3"
    ],
    "othermediums": [
      "phone",
      "iphone",
      "headphones",
      "airpods",
      "earbuds",
      "earphones",
      "tv",
      "television"
    ],
    "offline": [
      "download",
      "offline",
      "downloading"
    ],
    "discount": [
      "price",
      "reduced",
      "discount",
      "cheap",
      "cheaper",
      "expensive",
      "money",
      "free",
      "affordable",
      "inexpensive",
      "cost"
    ],
    "playlists": [
      "create",
      "playlist",
      "playlists",
      "share",
      "choose"
    ],
    "discovery": [
      "discover",
      "new",
      "mix",
      "discovering",
      "find",
      "finding",
      "uncover",
      "uncovering",
      "different"
    ],
    "shows": [
      "hulu",
      "showtime",
      "tv",
      "television",
      "shows",
      "video",
      "videos",
      "movie",
      "movies"
    ],
    "convenience": [
      "easy",
      "simple",
      "convenient",
      "good",
      "install",
      "installed",
      "ads",
      "advertisements"
    ],
    "selection": [
      "variety",
      "selection",
      "lots",
      "many",
      "songs",
      "diverse",
      "options",
      "any",
      "favorite",
      "song",
      "favorites"
    ],
    "rockrepresentation": [
      "underrepresented",
      "misogynistic",
      "white",
      "racial",
      "identify",
      "demographic"
    ],
    "artiststhatcamefromsoundcloud": [
      "Post Malone",
      "Bryson Tiller",
      "Kygo",
      "XXXTentacion",
      "Lil Uzi Vert",
      "Travis Scott",
      "Juice WRLD",
      "Denzel Curry",
      "Lil Peep",
      "Lil Yachty",
      "21 Savage",
      "Lil Pump"
    ]
  }
}

knowledge = KnowledgeBase()
knowledge.load_json(ont)
df = DialogueFlow('start', initial_speaker=DialogueFlow.Speaker.SYSTEM, kb=knowledge,
                  macros={"ARTIST_QUALITIES": ARTIST_QUALITIES(),
                          "ARTIST_GENRE": ARTIST_GENRE(),
                          "FIND_ARTIST": FIND_ARTIST(),
                          "FIND_SONG": FIND_SONG(),
                          "SONG_QUALITIES": SONG_QUALITIES(),
                          "FIND_ALBUM": FIND_ALBUM(),
                          "ALBUM_QUALITIES": ALBUM_QUALITIES(),
                          "GENRE_MATCH_INPUT": GENRE_MATCH_INPUT(),
                          "GENRE_MATCH_VARS": GENRE_MATCH_VARS(),
                          "CONCERT_FIND_ARTIST": CONCERT_FIND_ARTIST()})

df.add_system_transition('start', State.RES, '"Do you listen to music?"')
df.update_state_settings('start', enter='#GATE #IF($calypso_in=True) #SET($musicv=True)')
df.add_system_transition('request', State.RES, '"Do you listen to music?"')

df.add_user_transition(State.RES, State.YES, '[#ONT(yes)]')
df.add_user_transition(State.RES, State.NO, '[#ONT(no)]')


# Error
df.set_error_successor(State.RES, State.RES_ERROR)
df.add_system_transition(State.RES_ERROR, State.RES2, '"Sorry, I didn\'t catch that. Do you listen to music?"')
df.add_user_transition(State.RES2, State.YES, '[#ONT(yes)]')
df.add_user_transition(State.RES2, State.NO, '[#ONT(no)]')
df.set_error_successor(State.RES2, State.RES_ERROR2)
df.add_system_transition(State.RES_ERROR2, State.VERB, '"Hmm, well I love listening to music because it makes me less stressed. When do you listen to music?"')


#USER DOESNT LISTEN TO MUSIC
df.add_system_transition(State.NO, State.NO_ANS, '"That\'s a shame. Why do you not listen to music?"')

df.add_user_transition(State.NO_ANS, State.YES, '[{-not,-dont}, like, music]')
df.set_error_successor(State.NO_ANS, State.MUSIC_GOOD)

df.add_system_transition(State.MUSIC_GOOD, State.MUSIC_OPINION, "Scientists have actually found many benefits to listening "
                                                        "to music. Research shows music makes you happier. "
                                                        "It enhances workout performance and lowers stress. "
                                                        '"Have you heard about the benefits of music before?"')

df.add_user_transition(State.MUSIC_OPINION, State.AGREE, '[#ONT(yes)]')
df.add_user_transition(State.MUSIC_OPINION, State.DISAGREE, '[#ONT(no)]')
df.add_user_transition(State.MUSIC_OPINION, State.UNKNOWN, '#IDK')
df.add_system_transition(State.UNKNOWN, State.END, '"Well, it is pretty interesting, if you are ever bored and want to learn something cool."')
df.set_error_successor(State.MUSIC_OPINION, State.NEUT) # error handling

df.add_system_transition(State.AGREE, State.END, '"Great! It is pretty interesting, isn\'t it? "')
df.add_system_transition(State.DISAGREE, State.END, '"Well, it is pretty interesting, if you are ever bored and want to learn something cool."')
df.add_system_transition(State.NEUT, State.END, '"Well, it is pretty interesting, if you are ever bored and want to learn something cool."')



#USER LISTENS TO MUSIC
df.add_system_transition(State.YES, State.VERB, '"Cool, me too! When do you listen to music?"')

df.add_user_transition(State.VERB, State.VERBRES, '[-listen, -get, $activity={#POS(verb), $activity=#POS(VBG)}]')
df.add_user_transition(State.VERB, State.TIMERES, '[$time=#NER(time)]')
df.add_user_transition(State.VERB, State.PLACERES, '[$place={in the}, {in my}]')
df.add_user_transition(State.VERB, State.VERBUNK, '#IDK')

df.add_system_transition(State.VERBUNK, State.SERVICE, '"Well I usually listen to music while I\'m driving. What do you use to listen to music?"')

# Error
df.set_error_successor(State.VERB, State.ACT_ERROR)
df.add_system_transition(State.ACT_ERROR, State.VERB2, '"I\'m not sure I understand. Can you elaborate?"')
df.add_user_transition(State.VERB2, State.VERBRES, '[-listen, -get, -getting, $activity={#POS(verb), $activity=#POS(VBG)}]')
df.add_user_transition(State.VERB2, State.TIMERES, '[$time=#NER(time)]')
df.add_user_transition(State.VERB, State.SHOWER, '[{shower, bath}]')
df.add_user_transition(State.VERB, State.CAR, '[{car, drive}]')
df.add_user_transition(State.VERB, State.PLANE, '[{plane, flight}]')
df.add_user_transition(State.VERB, State.GYM, '[{gym, working out, work out, workout}]')
#df.add_user_transition(State.VERB, State.PLACERES, '[$place={in the}]')

df.set_error_successor(State.VERB2, State.ACT_ERROR2)
df.add_system_transition(State.ACT_ERROR2, State.SERVICE, '"I\'ve never heard of it. That\'s interesting! I prefer to listen to music in my car. What do you use to listen to music?"')



df.add_system_transition(State.VERBRES, State.SERVICE,
                         '"That\'s a great time to listen to music! What do you use to listen to music?"')
df.add_system_transition(State.TIMERES, State.SERVICE,
                         '"That\'s a great time to listen to music! What do you use to listen to music?"')
df.add_system_transition(State.SHOWER, State.SERVICE, '"I like listening to music while I shower too! What do you use to listen to music?"')
df.add_system_transition(State.CAR, State.SERVICE, '"I also listen to music when I drive. Be careful not to be distracted though! What do you use to listen to music?"')
df.add_system_transition(State.PLANE, State.SERVICE, '"Music is a great way to pass the time on flights. What do you use to listen to music?"')
df.add_system_transition(State.GYM, State.SERVICE, '"Music can make working out much more tolerable! What do you use to listen to music?"')

df.add_user_transition(State.SERVICE, State.CDS, '[-vinyl, $medium=#ONT(mediums)]')
df.add_user_transition(State.SERVICE, State.VINYLS, '[$medium=vinyl]')
df.add_user_transition(State.SERVICE, State.OTHERMED, '[$medium=#ONT(othermediums)]')
df.add_user_transition(State.SERVICE, State.SERVICEUNK, '#IDK')
df.add_system_transition(State.SERVICEUNK, State.STR_SERVICE, '"I usually listen to music on Pandora. Have you used music streaming services before?"')

#Error
df.set_error_successor(State.SERVICE, State.SERV_ERROR)
df.add_system_transition(State.SERV_ERROR, State.SERVICE2, '"Hmm, I\'m not sure what that is. What else do you use to listen to music?"')
df.add_user_transition(State.SERVICE2, State.CDS, '[-vinyl, $medium=#ONT(mediums)]')
df.add_user_transition(State.SERVICE2, State.VINYLS, '[$medium=vinyl]')
df.add_user_transition(State.SERVICE2, State.OTHERMED, '[$medium=#ONT(othermediums)]')
df.add_user_transition(State.SERVICE2, State.PANDORA, '[{pandora, pandora radio}]')
df.add_user_transition(State.SERVICE2, State.APPLE, '[{apple, siri}]')
df.add_user_transition(State.SERVICE2, State.AMAZON, '[{amazon, amazonplus, amazonpremium}]')
df.add_user_transition(State.SERVICE2, State.YOUTUBE, '[{YouTube, youtube}]')
df.add_user_transition(State.SERVICE2, State.SPOTIFY, '[{spotify, spotify music}]')
df.add_user_transition(State.SERVICE2, State.SERVICE2MID, '[#ONT(yes)]')
df.add_system_transition(State.SERVICE2MID, State.SERVICE2, '"That\'s cool! Which one do you use?"')
df.add_user_transition(State.SERVICE2, State.SERVICE2MIDNO, '[#ONT(no)]')
df.add_system_transition(State.SERVICE2MIDNO, State.STR_POPULAR, '"That\'s surprising. It seems like everyone is using one these days. They\'ve risen in popularity since in recent years, especially with the creation of Spotify. Can you guess when Spotify was created?"')
df.set_error_successor(State.SERVICE2, State.SERV_ERROR2)
df.add_system_transition(State.SERV_ERROR2, State.STR_SERVICE, '"Well, I\'ve never heard of that, but it\'s good that you like it. Do you use streaming services a lot?"')


df.add_user_transition(State.SERVICE, State.PANDORA, '[{pandora, pandora radio}]')
df.add_system_transition(State.PANDORA, State.OTHERSTREAM,
                         '"I love using Pandora to discover new music! Why do you like pandora?"')
df.add_user_transition(State.SERVICE, State.APPLE, '[{apple, siri}]')
df.add_system_transition(State.APPLE, State.OTHERSTREAM,
                         '"I love Apple music since it\'s well integrated with Siri! Why do you like Apple music?"')
df.add_user_transition(State.SERVICE, State.AMAZON, '[{amazon, amazonplus, amazonpremium}]')
df.add_system_transition(State.AMAZON, State.OTHERSTREAM,
                         '"I love Amazon music since it\'s well integrated with Alexa! why do you like Amazon music?"')
df.add_user_transition(State.SERVICE, State.YOUTUBE, '[{YouTube, youtube}]')
df.add_system_transition(State.YOUTUBE, State.OTHERSTREAM,
                         '"I use youtube a lot too since you can watch thousands of music videos all for free! Why do you like youtube?"')
df.add_user_transition(State.SERVICE, State.SPOTIFY, '[{spotify, spotify music}]')
df. add_system_transition(State.SPOTIFY, State.SPOTIPULL, '"I think Spotify has really transformed the music industry. Have you heard of celebrities pulling songs from spotify?"')
df.add_user_transition(State.SPOTIPULL, State.TAYLORSWIFT, '[{taylor swift}]')
df.add_system_transition(State.TAYLORSWIFT, State.STR_SERVICE, '"Yes, I heard she removed all 7 of her albums once because of this. Do you use streaming services a lot?"')
df.add_user_transition(State.SPOTIPULL, State.YESPULL, '[#ONT(yes)]')
df.add_system_transition(State.YESPULL, State.STR_SERVICE, '"So you probably heard about Taylor Swift removing her albums once. Do you use streaming services a lot?"')
df.set_error_successor(State.SPOTIPULL, State.SPOTIERR)
df.add_system_transition(State.SPOTIERR, State.STR_SERVICE, '"Well, Taylor Swift once removed her albums from the platform because of this. Do you use streaming services a lot?"')

discount = r"[#ONT(discount)]"
df.add_user_transition(State.OTHERSTREAM, State.DISCOUNT, discount)
df.add_system_transition(State.DISCOUNT, State.STR_SERVICE, '"You\'re right. It\'s pretty affordable and there might be discounts if you\'re a student. Do you use streaming services a lot?"')

playlists = r"[#ONT(playlists)]"
df.add_user_transition(State.OTHERSTREAM, State.PLAYLIST, playlists)
df.add_system_transition(State.PLAYLIST, State.STR_SERVICE, '"It\'s cool to create and share playlists! Do you use streaming services a lot?"')

convenient = r"[#ONT(convenience)]"
df.add_user_transition(State.OTHERSTREAM, State.CONVENIENCE, convenient)
df.add_system_transition(State.CONVENIENCE, State.STR_SERVICE, '"You\'re right. its a convenient service. Do you use streaming services a lot?"')

selection = r"[#ONT(selection)]"
df.add_user_transition(State.OTHERSTREAM, State.SELECTION, selection)
df.add_system_transition(State.SELECTION, State.STR_SERVICE, '"There are thousands of songs on there! Do you use streaming services a lot?"')

shows = r"[#ONT(shows)]"
df.add_user_transition(State.OTHERSTREAM, State.SHOWS, shows)
df.add_system_transition(State.SHOWS, State.STR_SERVICE, '"I love when streaming services come with perks like that! Do you use streaming services a lot?"')

downloading = r"[#ONT(offline)]"
df.add_user_transition(State.OTHERSTREAM, State.DOWNLOAD, downloading)
df.add_system_transition(State.DOWNLOAD, State.STR_SERVICE, '"Downloading music is especially convenient for long plane rides. Do you use streaming services a lot?"')

discovery = r"[#ONT(discovery)]"
df.add_user_transition(State.OTHERSTREAM, State.DISCOVERY, discovery)
df.add_system_transition(State.DISCOVERY, State.STR_SERVICE, '"I like finding new music too! Do you use streaming services a lot?"')

df.add_user_transition(State.OTHERSTREAM, State.OTHERSTREAMUNK, '#IDK')
df.add_system_transition(State.OTHERSTREAMUNK, State.STR_SERVICE, '"Fair enough. Do you use streaming services a lot?"')

#Error
df.set_error_successor(State.OTHERSTREAM, State.STREAM_ERROR2)
#df.add_system_transition(State.STREAM_ERROR, State.OTHERSTREAM2, '"Sorry, I didn\'t catch that. What else do you like about your streaming service?"')
#df.add_user_transition(State.OTHERSTREAM2, State.DISCOUNT, discount)
#df.add_user_transition(State.OTHERSTREAM2, State.PLAYLIST, playlists)
#df.add_user_transition(State.OTHERSTREAM2, State.CONVENIENCE, convenient)
#df.add_user_transition(State.OTHERSTREAM2, State.SELECTION, selection)
#df.add_user_transition(State.OTHERSTREAM2, State.SHOWS, shows)
#df.add_user_transition(State.OTHERSTREAM2, State.DOWNLOAD, downloading)
#df.add_user_transition(State.OTHERSTREAM2, State.DISCOVERY, discovery)
#df.set_error_successor(State.OTHERSTREAM2, State.STREAM_ERROR2)
df.add_system_transition(State.STREAM_ERROR2, State.STR_SERVICE, '"That\'s cool! I personally like using Spotify because I can get a family discount plan. Do you use streaming services a lot?"')


df.add_system_transition(State.CDS, State.STR_SERVICE,
                         '"Oh, really? It seems like everyone streams their music now. Do you use any music streaming services?"')

df.add_system_transition(State.VINYLS, State.STR_SERVICE,
                         '"Vinyls are great. I exclusively listen to vinyls because I think the music quality is much better. Do you use music streaming services when you don\'t have access to your vinyls?"')

df.add_system_transition(State.OTHERMED, State.SERVICE2, '"oh you use" $medium "? I prefer the sound quality of vinyls. Do you use any music streaming services?"')

df.add_user_transition(State.STR_SERVICE, State.STR_YESSTREAM, '[#ONT(yes)]')
df.add_user_transition(State.STR_SERVICE, State.STR_NOSTREAM, '[#ONT(no)]')
df.add_user_transition(State.STR_SERVICE, State.STR_SERVICEUNK, '#IDK')
df.add_system_transition(State.STR_SERVICEUNK, State.STR_POPULAR, '"Well streaming services are things like Spotify and Apple Music. They\'ve gotten really popular lately, especially with the creation of Spotify. Can you guess when Spotify was created?"')
df.add_system_transition(State.STR_YESSTREAM, State.STR_POPULAR, '"I\'m not surprised. Lots of people use streaming services. They\'ve gotten really popular lately, especially with the creation of Spotify. Can you guess when Spotify was created?"')
df.add_system_transition(State.STR_NOSTREAM, State.STR_POPULAR, '"That\'s surprising. It seems like everyone is using one these days. They\'ve gotten really popular lately, especially with the creation of Spotify. Can you guess when Spotify was created?"')
df.set_error_successor(State.STR_SERVICE, State.STR_ERR5)
df.add_system_transition(State.STR_ERR5, State.STR_POPULAR, '"It seems like everyone is using one these days. They\'ve gotten really popular lately, especially with the creation of Spotify. Can you guess when Spotify was created?"')


df.add_user_transition(State.STR_POPULAR, State.STR_GUESS2008, '[{2008}]')
df.add_system_transition(State.STR_GUESS2008, State.STR_ARTISTREV, '"You\'re exactly right! Spotify was created in 2008 in hopes of reducing music piracy. How do you think this impacted artist revenue?"')
df.add_user_transition(State.STR_POPULAR, State.STR_GUESS, '$year_guess={#POS(NN)}')
df.add_system_transition(State.STR_GUESS, State.STR_ARTISTREV, '"Hm $year_guess is close but Spotify was created in 2008 in hopes of reducing music piracy. How do you think this impacted artist revenue?"')
df.add_user_transition(State.STR_GUESS, State.STR_GUESSUNK, '#IDK')
df.add_system_transition(State.STR_GUESSUNK, State.STR_ARTISTREV, '"That\'s okay, it\'s a pretty niche fact, but Spotify was created in 2008. How do you think this impacted artist revenue?"')
df.set_error_successor(State.STR_POPULAR, State.STR_ERR1)
df.add_system_transition(State.STR_ERR1, State.STR_ARTISTREV, '"Spotify was actually created in 2008 in hopes of reducing music piracy. How do you think this impacted artist revenue?"')

df.add_user_transition(State.STR_ARTISTREV, State.STR_MORE, '[{more, bigger, higher, #ONT(positive_response)}]')
df.add_system_transition(State.STR_MORE, State.STR_SONG, '"I see why you would think that since more people may be listening to their music legally, but artists only receive about 7 cents per stream. Have you heard of how this royalty system has affected new music?"')
df.add_user_transition(State.STR_ARTISTREV, State.STR_LESS, '[{less, fewer, lower, smaller, #ONT(negative_response)}]')
df.add_system_transition(State.STR_LESS, State.STR_SONG, '"You\'re right! Artists only receive about 7 cents per stream. Have you heard of how this royalty system has affected new music?"')
df.add_user_transition(State.STR_ARTISTREV, State.STR_ARTISTREVUNK, '#IDK')
df.add_system_transition(State.STR_ARTISTREVUNK, State.STR_SONG, '"Yeah, there are a lot of factors that come into play, but artists have been making less money since the streaming services gets a big cut. Have you heard about how this royalty system has affected new music?"')

df.set_error_successor(State.STR_ARTISTREV, State.STR_ERR4)
df.add_system_transition(State.STR_ERR4, State.STR_SONG, '"That\'s an interesting perspective! Although their music is pirated less, artists only receive about 7 cents per stream. Have you heard of how this royalty system has affected new music?"')
df.set_error_successor(State.STR_SONG, State.STR_NOSONG)

df.add_user_transition(State.STR_SONG, State.STR_YESSONG, '{[#ONT(yes)], short, shorter, songs, song, album, albums, new, music}')
df.add_system_transition(State.STR_YESSONG, State.STR_SONGINFO, '"Isn\'t it crazy that songs are becoming shorter and albums are having more songs on them so artists can get paid more! Still, streaming services might be good. Can you think of any reasons why?"')
df.set_error_successor(State.STR_SONG, State.STR_NOSONG)
df.add_system_transition(State.STR_NOSONG, State.STR_SONGINFO, '"Well, since artists are paid by the song streamed, they\'re releasing albums with more songs on them but the songs are shorter. Still, streaming services might be good. Can you think of any reasons why?"')

df.add_user_transition(State.STR_SONGINFO, State.STR_NORES, '[#ONT(no)]')
df.add_user_transition(State.STR_SONGINFO, State.STR_NORESUNK, '#IDK')
df.add_system_transition(State.STR_NORESUNK, State.ARTIST, '"Well in my opinion, I think that streaming services make it easy for artists to get started and build a fanbase. It also makes music very accessible to listeners. Most of my favorite artists are on Spotify. Who\'s your favorite artist?"')
df.add_system_transition(State.STR_NORES, State.ARTIST, '"Well in my opinion, I think that streaming services make it easy for artists to get started and build a fanbase. It also makes music very accessible to listeners. Most of my favorite artists are on Spotify. Who\'s your favorite artist?"')

df.add_user_transition(State.STR_SONGINFO, State.STR_LISTENER, '[{me, listener, listeners, cheap, inexpensive, expensive, whatever, options, available, can listen}]')
df.add_system_transition(State.STR_LISTENER, State.ARTIST, '"That\'s true! Listeners have access to thousands of songs for one low price! I think streaming services also make it easy for artists to get started and build a fanbase. Most of my favorite artists are on Spotify. Who\'s your favorite artist?"')

df.add_user_transition(State.STR_SONGINFO, State.STR_ACCESS, '[{new, artist, artists, rise, build, career, easy, accessible, accessibility, start, started}]')
df.add_system_transition(State.STR_ACCESS, State.ARTIST, '"That\'s true! New artists can easily put their music on a streaming service and build a fan base. It also gives isteners access to thousands of songs and artists for one low price! Most of my favorite artists are on Spotify. Who\'s your favorite artist?"')

df.set_error_successor(State.STR_SONGINFO, State.STR_ERR2)
df.add_system_transition(State.STR_ERR2, State.STR_SONGINFO2, '"Sorry, I\'m not sure what you mean. Can you think of another way streaming services have helped listeners or artists?"')
df.set_error_successor(State.STR_SONGINFO2, State.STR_ERR3)
df.add_user_transition(State.STR_SONGINFO2, State.STR_LISTENER, '[{me, listener, listeners, cheap, inexpensive, expensive, whatever, options, available, can listen}]')
df.add_user_transition(State.STR_SONGINFO2, State.STR_ACCESS, '[{new, artist, artists, rise, build, career, easy, accessible, accessibility, start, started}]')
df.add_system_transition(State.STR_ERR3, State.ARTIST, '"That\'s an interesting perspective! I think streaming services make it easy for artists to get started and build a fanbase. It also makes music very accessible to listeners. Most of my favorite artists are on Spotify. Who\'s your favorite artist?"')


##call macro before transition and put returned value into a variable, check contents, go to diff state
df.add_user_transition(State.ARTIST, 'some_music_state', '{i like, i enjoy, my favorite artist is, /^/}[#FIND_ARTIST]')


df.set_error_successor(State.ARTIST, State.ARTIST_ERR1)

df.add_system_transition(State.ARTIST_ERR1, State.U_ARTIST_ERR1, '"Sorry, I didn\'t quite get that. Who\'s your favorite artist?"')
df.add_user_transition(State.U_ARTIST_ERR1, 'some_music_state', '{i like, i enjoy, my favorite artist is, /^/}[#FIND_ARTIST]')
df.set_error_successor(State.U_ARTIST_ERR1, State.ARTIST_ERROR)

#artist_genre = r"[#ARTIST_GENRE]"
#artist_qualities = r"[#ARTIST_QUALITIES]"
df.add_system_transition('some_music_state', State.U_FEAT_START, '"i think they are a great" #ARTIST_GENRE "artist. Their music is so" #ARTIST_QUALITIES ". What do you like about them so much?"')

df.add_system_transition(State.ARTIST_ERROR, State.U_ALBUMERR, '"Hmm, I\'ve never heard of them. Guess I\'ll go listen to their music later. What\'s your favorite album?"')

# ARTIST features

df.add_user_transition(State.U_FEAT_START, State.S_ARTIST_FEAT_2, '/.*/')
df.set_error_successor(State.U_FEAT_START, State.S_ARTIST_FEAT_2)

df.add_system_transition(State.S_ARTIST_FEAT_2, State.U_ARTIST_FEAT_2, '"Cool! What\'s your favorite song by them?"')
df.add_user_transition(State.U_ARTIST_FEAT_2, State.S_ALBUM_FROM_ERR, '[{'
                                                                         'dont know,do not know,unsure,[not,{sure,certain}],hard to say,no idea,uncertain,[!no {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],'
                                                                         '[{dont,do not}, have, {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],'
                                                                         '[!{cant,cannot,dont} {think,remember,recall}]'
                                                                         '}]')
df.add_user_transition(State.U_ARTIST_FEAT_2, State.S_ARTIST_FEAT_3, '{i like, /^/}[#FIND_SONG]')
df.set_error_successor(State.U_ARTIST_FEAT_2, State.S_ARTIST_FEAT_3_ERR)

df.add_system_transition(State.S_ARTIST_FEAT_3_ERR, State.U_ARTIST_FEAT_3_ERR,
                         '"Hmm, I don\'t know that one, is there a different song you like?"')
df.add_user_transition(State.U_ARTIST_FEAT_3_ERR, State.S_ARTIST_FEAT_3,
                       '{i like, probably, /^/}[#FIND_SONG]')
df.set_error_successor(State.U_ARTIST_FEAT_3_ERR, State.S_ARTIST_FEAT_3_ERR2)
df.add_system_transition(State.S_ARTIST_FEAT_3_ERR2, State.ARTIST,
                         '"Hmm, I don\'t know that one. Let\'s try a different artist. Who else do you listen to?"')

df.add_system_transition(State.S_ARTIST_FEAT_3, State.U_ARTIST_FEAT_3,
                         '"I love that song! Isn\'t it so"#SONG_QUALITIES"?"')
df.add_user_transition(State.U_ARTIST_FEAT_3, State.S_ARTIST_FEAT_4_YES, '[#ONT(yes)]')
df.add_user_transition(State.U_ARTIST_FEAT_3, State.S_ARTIST_FEAT_4_NO, '[#ONT(no)]')
df.set_error_successor(State.U_ARTIST_FEAT_3, State.S_ARTIST_FEAT_4_YES)  # S_ARTIST_FEAT_4_ERR has some weird issues. Check

df.add_system_transition(State.S_ARTIST_FEAT_4_ERR, State.U_ARTIST_FEAT_4_ERR,
                         '"Sorry I didn\'t quite understand. Do you agree that the song is" $fav_song_descript "?"')
df.add_user_transition(State.U_ARTIST_FEAT_4_ERR, State.S_ARTIST_FEAT_4_YES, '[#ONT(yes)]')
df.add_user_transition(State.U_ARTIST_FEAT_4_ERR, State.S_ARTIST_FEAT_4_NO, '[#ONT(no)]')
df.set_error_successor(State.U_ARTIST_FEAT_4_ERR, State.S_ALBUM_FROM_ERR)

df.add_system_transition(State.S_ALBUM_FROM_ERR, State.U_ALBUM, '"That\'s ok. Let\'s move on. What\'s an album you really like?"')

df.add_system_transition(State.S_ARTIST_FEAT_4_YES, State.U_ALBUM,
                         '"Awesome! You seem like you really enjoy music. What\'s an album you really like?"')
df.add_system_transition(State.S_ARTIST_FEAT_4_NO, State.U_ALBUM,
                         '"Well, agree to disagree. So, What\'s an album you like?"')
df.add_user_transition(State.U_ALBUM, State.S_ALBUM, '[#FIND_ALBUM]')
df.set_error_successor(State.U_ALBUM, State.S_ALBUM_ERR)

df.add_user_transition(State.U_ALBUMERR, State.S_ALBUM, '[#FIND_ALBUM]')
df.set_error_successor(State.U_ALBUMERR, State.S_ALBUMERR)
df.add_system_transition(State.S_ALBUMERR, State.TM_CONCERT, '"Hm I haven\'t heard of that one. Let\'s move on. Have you been to any concerts?"')


df.add_system_transition(State.S_ALBUM_ERR, State.U_ALBUM_ERR, '"I\'m sorry, I didn\'t quite catch that. What\'s an album you like?"')
df.add_user_transition(State.U_ALBUM_ERR, State.S_ALBUM, '[#FIND_ALBUM]')
df.set_error_successor(State.U_ALBUM_ERR, State.S_ALBUM_ERR2)
df.add_system_transition(State.S_ALBUM_ERR2, State.U_ALBUM_2, '"Haven\'t heard of that one. Let\'s move on. Do you prefer"$genre"music?"')

df.add_system_transition(State.S_ALBUM, State.U_ALBUM_2, '"That\'s a pretty"#ALBUM_QUALITIES"record. Good pick! Do you prefer"$genre"music?"')
df.add_user_transition(State.U_ALBUM_2, State.HIPHOP_START, '[#ONT(yes)]#GENRE_MATCH_VARS(hiphop)')
df.add_user_transition(State.U_ALBUM_2, State.S_INDIE, '[#ONT(yes)]#GENRE_MATCH_VARS(indie)')
df.add_user_transition(State.U_ALBUM_2, State.ROCK, '[#ONT(yes)]#GENRE_MATCH_VARS(rock)')
df.add_user_transition(State.U_ALBUM_2, State.TM_START, '[#ONT(yes)]#GENRE_MATCH_VARS(pop)')
df.add_user_transition(State.U_ALBUM_2, State.PRE_TM, '[#ONT(yes)]#GENRE_MATCH_VARS(other)')
#df.add_user_transition(State.U_ALBUM_2, State.PRE_TM, '[#ONT(yes)]')
df.add_user_transition(State.U_ALBUM_2, State.S_ALBUM_3_NO, '[#ONT(no)]')
df.set_error_successor(State.U_ALBUM_2, State.S_ALBUM_3_ERR)

df.add_system_transition(State.S_ALBUM_3_ERR, State.U_ALBUM_3_ERR, '"I\'m sorry, I didn\'t quite catch that. Do you prefer"$genre"music?"')
df.add_user_transition(State.U_ALBUM_3_ERR, State.S_INDIE, '[#ONT(yes)]#GENRE_MATCH_VARS(indie)')
df.add_user_transition(State.U_ALBUM_3_ERR, State.ROCK, '[#ONT(yes)]#GENRE_MATCH_VARS(rock)')
df.add_user_transition(State.U_ALBUM_3_ERR, State.TM_START, '[#ONT(yes)]#GENRE_MATCH_VARS(pop)')
df.add_user_transition(State.U_ALBUM_3_ERR, State.PRE_TM, '[#ONT(yes)]#GENRE_MATCH_VARS(other)')
df.add_user_transition(State.U_ALBUM_3_ERR, State.S_ALBUM_3_NO, '[#ONT(no)]')

df.set_error_successor(State.U_ALBUM_3_ERR, State.S_ALBUM_3_ERR2)

df.add_system_transition(State.S_ALBUM_3_ERR2, State.TM_CONCERT, '"Well, I do enjoy going to concerts. Have you been to any concerts before?"')

df.add_system_transition(State.S_ALBUM_3_NO, State.U_ALBUM_3, '"What is your favorite genre?"')
df.add_user_transition(State.U_ALBUM_3, State.S_INDIE, genre_to_natex['indie'])
df.add_user_transition(State.U_ALBUM_3, State.HIPHOP_START, genre_to_natex['hiphop'])
df.add_user_transition(State.U_ALBUM_3, State.TM_START, genre_to_natex['pop'])
df.add_user_transition(State.U_ALBUM_3, State.ROCK, genre_to_natex['rock'])
df.add_user_transition(State.U_ALBUM_3, State.GENREUNK, '[{'
                                                    'dont know,do not know,unsure,[not,{sure,certain}],hard to say,no idea,uncertain,[!no {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],'
                                                    '[{dont,do not}, have, {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],'
                                                    '[!{cant,cannot,dont} {think,remember,recall}]'
                                                    '}]')
df.add_system_transition(State.GENREUNK, State.TM_CONCERT, '"That\'s okay, I like a lot of different genres too. Have you been to any concerts?"')
df.set_error_successor(State.U_ALBUM_3, State.PRE_TM)

df.add_system_transition(State.PRE_TM, State.TM_CONCERT, '"Cool! Have you ever been to any concerts?"')

# ROCK MUSIC
# ROCK MUSIC

# Turn 1
df.add_system_transition(State.ROCK, State.ROCKDYING, '"So you like rock music?! I don\'t know about that."'
                                                      '"I heard the genre is dying out. wouldn\'t you agree?"')
df.add_user_transition(State.ROCKDYING, State.ROCKAGREE, '[#ONT(yes)]')
df.add_user_transition(State.ROCKDYING, State.ROCKDISAGREE, '[#ONT(no)]')
# Error
#df.set_error_successor(State.ROCKDYING, State.ROCK_ERROR3)
#df.add_system_transition(State.ROCK_ERROR3, State.ROCKDYING2, '"Sorry, I didn\'t catch that. Don\'t you agree?"')
#df.add_user_transition(State.ROCKDYING2, State.ROCKAGREE, '[#ONT(yes)]')
#df.add_user_transition(State.ROCKDYING2, State.ROCKDISAGREE, '[#ONT(no)]')
df.set_error_successor(State.ROCKDYING, State.ROCK_ERROR4)
df.add_system_transition(State.ROCK_ERROR4, State.POPULARITY, '"Well, it\'s true! I feel like no one listens to rock anymore. Why do you think that is?"')
df.add_system_transition(State.ROCKAGREE, State.POPULARITY, '"Yeah, I also think that the popularity of rock music is declining. Why do you think that is?"')
df.add_system_transition(State.ROCKDISAGREE, State.POPROCKBANDS, '"No, you don\'t think so? I suppose you consider pop rock"'
                                                                 '"bands like Imagine Dragons or Fallout Boy rock music,"'
                                                                 '"but I\'m a purist. Why do you think rock music is still popular?"')

# Turn 2
df.add_user_transition(State.POPULARITY, State.ROCKIMAGE, '[{image, brand}]')
df.add_system_transition(State.ROCKIMAGE, State.ROCKANS, '"That makes sense, a lot of big labels refuse to sign new rock bands because rock"'
                                                        '"is sometimes associated with a bad image. Do you think that rock music"'
                                                         '"is only listened to by older people?"')
df.add_user_transition(State.POPULARITY, State.ROCKREPRESENT, '[#ONT(rockrepresentation)]')
df.add_system_transition(State.ROCKREPRESENT, State.ROCKANS, '"Yeah, rock music now is purchased mostly by white males."'
                                                             '"Now, I think people are more attracted to artists that look like them."'
                                                             '"Do you think that rock music"'
                                                             '"is only listened to by older people?"')
df.add_system_transition(State.ROCKCOSTLY, State.ROCKANS, '"That makes sense. It\'s expensive for new rock bands to be able to afford the equipment"'
                                                      '"to produce the sounds associated with rock music in the past.  Do you think that rock music is only listened to by older people?"')
df.add_user_transition(State.POPULARITY, State.DIFFSOUND, '[{sound, tone, beat, beats}]')
df.add_system_transition(State.DIFFSOUND, State.ROCKANS, '"That makes sense, \"rock\" bands like Imagine Dragons are making too much of an effort"'
                                                         '"to appeal to pop music listeners that the original sound quality of rock music has been lost."'
                                                         '"Do you think that rock music is now associated with older listeners?"')
df.add_user_transition(State.POPULARITY, State.ROCKDONTKNOW, '#IDK')
df.add_system_transition(State.ROCKDONTKNOW, State.ROCKANS, '"Well, some people think that it\'s because rock artists don\'t really represent"'
                                                             '"the demographics of music fans anymore, but I think that rock music is too expensive to produce."'
                                                            '"Do you think that rock music is now associated with older listeners?"')
# Error
df.set_error_successor(State.POPULARITY, State.ROCK_ERROR5)
df.add_system_transition(State.ROCK_ERROR5, State.POPULARITY2, '"Sorry, I don\'t understand. Why do you think rock is losing its popularity?"')
df.add_user_transition(State.POPULARITY2, State.ROCKIMAGE, '[{image, brand}]')
df.add_user_transition(State.POPULARITY2, State.ROCKREPRESENT, '[#ONT(rockrepresentation)]')
df.add_user_transition(State.POPULARITY2, State.ROCKCOSTLY, '[#ONT(discount)]')
df.add_user_transition(State.POPULARITY2, State.DIFFSOUND, '[{sound, tone, beat, beats}]')
df.add_user_transition(State.POPULARITY2, State.ROCKDONTKNOW, '#IDK')
df.set_error_successor(State.POPULARITY2, State.ROCK_ERROR6)
df.add_system_transition(State.ROCK_ERROR6, State.ROCKANS, '"I think it\'s due to a lot of reasons, mostly because rock music doesn\'t sound like it did before. Some say that rock listeners have aged with their songs. Do you agree?"')
df.add_user_transition(State.POPROCKBANDS, State.ROCKARTISTS, '[{artists, people, musicians, band, bands}]')
df.add_system_transition(State.ROCKARTISTS, State.ROCKANS, '"Yeah, some artists like Metallica are still very true to the genre,"'
                                                           '"but other bands like Coldplay or Fall Out Boy are leaning more towards pop."'
                                                            '"Do you think that rock music is now associated with older listeners?"')
df.add_user_transition(State.POPROCKBANDS, State.ROCKSTORY, '[{story, meaning, lyrics}]')
df.add_system_transition(State.ROCKSTORY, State.ROCKANS, '"That\'s true. I think a lot of unwavering rock fans love the genre because every song has a story they can relate to."'
                                                             '"But do you think that rock music is now associated with older listeners?"')
df.add_user_transition(State.POPROCKBANDS, State.ROCKINSTRUMENTS, '[{sound, instruments, guitar, bass drums, beat, beats, tone}]')
df.add_system_transition(State.ROCKINSTRUMENTS, State.ROCKANS, '"Yeah, rock music is known for its instruments, but there\'s only"'
                                                               '"so much you can do with an electric guitar or bass until it gets repetitive."'
                                                               '"Do you think that rock music is now associated with older listeners?"')
df.add_user_transition(State.POPROCKBANDS, State.ROCKDONTKNOW2, '#IDK')
df.add_system_transition(State.ROCKDONTKNOW2, State.ROCKANS, '"Well some people still love the way rock artists tell stories through their music and its distinctive sound."'
                         '"Do you think that rock music is now associated with older listeners?"')
# Error
df.set_error_successor(State.POPROCKBANDS, State.ROCK_ERROR7)
df.add_system_transition(State.ROCK_ERROR7, State.POPROCKBANDS2, '"I don\'t think I understand. Why do you think rock music is still so popular?"')
df.add_user_transition(State.POPROCKBANDS2, State.ROCKARTISTS, '[{artists, people, musicians, band, bands}]')
df.add_user_transition(State.POPROCKBANDS2, State.ROCKSTORY, '[{story, meaning}]')
df.add_user_transition(State.POPROCKBANDS2, State.ROCKINSTRUMENTS, '[{sound, instruments, guitar, drums, beat, beats, tone}]')
df.add_user_transition(State.POPROCKBANDS2, State.ROCKDONTKNOW2, '#IDK')
df.set_error_successor(State.POPROCKBANDS2, State.ROCK_ERROR8)
df.add_system_transition(State.ROCK_ERROR8, State.ROCKANS, '"Well some people still love the way rock artists tell stories through their music and its distinctive sound."'
                         '"Do you think that rock music is now associated with older listeners?"')

# Turn 3
df.add_user_transition(State.ROCKANS, State.YESAGING, '[#ONT(yes)]')
df.add_system_transition(State.YESAGING, State.ROCKSONG, '"I think you\'re right. It\'s unfortunate,"'
                                                         '"but younger people listen to far less rock and more pop and hip-hop. What\'s your favorite rock song to listen to?"')
df.add_user_transition(State.ROCKANS, State.NOAGING, '[#ONT(no)]')
df.add_system_transition(State.NOAGING, State.ROCKSONG, '"Hmm, I feel like most young people now are"'
                                                        '"listening to more pop and hip-hop. What\'s your favorite rock song?"')
df.add_user_transition(State.ROCKANS, State.AGINGIDK, '#IDK')
df.add_system_transition(State.AGINGIDK, State.ROCKSONG, '"I think most young people are now listening to pop and hip-hop more. What\'s your favorite rock song to listen to?"')
# Error
df.set_error_successor(State.ROCKANS, State.ROCK_ERROR9)
df.add_system_transition(State.ROCK_ERROR9, State.ROCKANS2, '"Sorry, let me reword my question. Do you think the rock is only listened to by older people now?"')
df.add_user_transition(State.ROCKANS2, State.YESAGING, '[#ONT(yes)]')
df.add_user_transition(State.ROCKANS2, State.NOAGING, '[#ONT(no)]')
df.add_user_transition(State.ROCKANS2, State.AGINGIDK, '#IDK')
df.set_error_successor(State.ROCKANS2, State.ROCK_ERROR10)
df.add_system_transition(State.ROCK_ERROR10, State.ROCKSONG, '"The most popular rock songs are from the seventies. What\'s your favorite rock song?"')

# TODO: Create macro that associates song with artist
df.add_user_transition(State.ROCKSONG, State.SONGARTIST, '[$song=#NER(WORKOFART)]')
df.add_system_transition(State.SONGARTIST, State.TM_CONCERT, '"Oh," $song "is by <INSERTARTIST>! I love listening to that song on vinyl. I would love to hear it live though. Have you been to any concerts?"')
df.add_user_transition(State.ROCKSONG, State.SONGARTIST1, '[{bohemian rhapsody, Bohemian Rhapsody}]')
df.add_system_transition(State.SONGARTIST1, State.TM_CONCERT, '"Oh, Bohemian Rhapsody is by Queen! I love listening to that song on vinyl. I would love to hear it live though. Have you been to any concerts?"')
# Error
df.set_error_successor(State.ROCKSONG, State.ROCK_ERROR11)
df.add_system_transition(State.ROCK_ERROR11, State.TM_CONCERT, '"Hmm, I\'ve never heard of that song, but I\'ll definitely listen to it now. I\'d prefer to listen to music live though. Have you been to any concerts?"')



######INDIE######
df.add_system_transition(State.S_INDIE, State.U_INDIE,
                         '"A big problem that I\'ve heard independent artists are having these days is the dominance of big record labels. How many major record labels do you think there are?"')
df.add_user_transition(State.U_INDIE, State.S_INDIE_EQUAL, "[{3,three}]")
df.add_user_transition(State.U_INDIE, State.S_INDIE_LESS, "[{one,1,2,two}]")
df.add_user_transition(State.U_INDIE, State.S_INDIE_MORE, "[/(1|2|3|4|5|6|7|8|9|0)*/]")
df.add_user_transition(State.U_INDIE, State.U_INDIEUNK, '#IDK')
df.add_system_transition(State.U_INDIEUNK, State.U_INDIE_2, '"There are 3. Isn\'t that kind of scary? Indie artists are competing against very established and dominant corporations. How do you feel about that?"')

df.set_error_successor(State.U_INDIE, State.S_INDIE_EQUAL)

df.add_system_transition(State.S_INDIE_EQUAL,State.U_INDIE_2,
                         '"Yup there are 3! Isn\'t that kind of scary? Indie artists are competing against very established and dominant corporations. How do you feel about that?"')
df.add_system_transition(State.S_INDIE_LESS,State.U_INDIE_2,
                         '"Close, it\'s 3! Only Sony Music Entertainment, Warner Music Group and Universal Music Group are responsible for two thirds of all music sales in the world. How do you feel about that?"')
df.add_system_transition(State.S_INDIE_MORE,State.U_INDIE_2,
                         '"Less, actually, it\'s 3! Only Sony Music Entertainment, Warner Music Group and Universal Music Group are responsible for two thirds of all music sales in the world. How do you feel about that?"')
df.add_user_transition(State.U_INDIE_2, State.S_INDIE_3A, '[{#ONT(positive_response),#ONT(mixed_response)}]')
df.add_user_transition(State.U_INDIE_2, State.S_INDIE_3B, '[#ONT(negative_response)]')
df.add_user_transition(State.U_INDIE_2, State.U_INDIE_2UNK, '#IDK')
df.add_system_transition(State.U_INDIE_2UNK, State.U_INDIE_3A, '"I think the monopoly might make it tougher for new artists and musicians to make it into the music industry. What do you think?"')
df.set_error_successor(State.U_INDIE_2, State.S_INDIE_3A)

df.add_system_transition(State.S_INDIE_3A, State.U_INDIE_3A,
                         '"Don\'t you think it this monopoly might make it tougher for new artists and musicians to make it into the music industry?"')
df.add_system_transition(State.S_INDIE_3B, State.U_INDIE_3B,
                         '"Yeah, I\'m worried about how this monopoly might affect the growth of music in the future of the industry. Do you think that\'s a possibility?"')
df.add_user_transition(State.U_INDIE_3A, State.S_INDIE_4A, '[#ONT(yes)]')
df.add_user_transition(State.U_INDIE_3A, State.S_INDIE_4B, '[#ONT(no)]')
df.add_user_transition(State.U_INDIE_3A, State.S_INDIE_4E, '#IDK')
df.add_user_transition(State.U_INDIE_3B, State.S_INDIE_4A, '[#ONT(yes)]')
df.add_user_transition(State.U_INDIE_3B, State.S_INDIE_4B, '[#ONT(no)]')
df.add_user_transition(State.U_INDIE_3B, State.S_INDIE_4E, '#IDK')
df.set_error_successor(State.U_INDIE_3A, State.S_INDIE_3E)
df.set_error_successor(State.U_INDIE_3B, State.S_INDIE_3E)

df.add_system_transition(State.S_INDIE_3E, State.U_INDIE_3E, '"I don\'t understand, can you repeat that? Do you think the monopoly will be tough on independent artists?"')
df.add_user_transition(State.U_INDIE_3E, State.S_INDIE_4A, '[#ONT(yes)]')
df.add_user_transition(State.U_INDIE_3E, State.S_INDIE_4B, '[#ONT(no)]')
df.set_error_successor(State.U_INDIE_3E, State.S_INDIE_4E)

df.add_system_transition(State.S_INDIE_4A, State.TM_CONCERT,
                         '"Yeah, I\'m worried about that too! Independent artists might have trouble surviving in that kind of industry, but we can support their live shows. Have you been to any concerts?"')
df.add_system_transition(State.S_INDIE_4B, State.TM_CONCERT,
                         '"That\'s not how I feel! I think independent artists might have trouble surviving with that kind of industry, but we can support their live shows. Have you been to any concerts?"')
df.add_system_transition(State.S_INDIE_4E, State.TM_CONCERT,
                         '"Well independent artists might have trouble surviving in that kind of industry, but we can support their live shows. Have you been to any concerts?"')

######INDIE######


######HIPHOP######

df.add_system_transition(State.HIPHOP_START, State.HIPHOP_Q1, '"That\'s cool, I like hip-hop/rap too!. I recently discovered Soundcloud. Have you ever heard of it?"') # Have you ever used soundcloud?
df.add_user_transition(State.HIPHOP_Q1, State.HIPHOP_RESP1a, '[#ONT(yes)]')

df.set_error_successor(State.HIPHOP_Q1, State.HIPHOP_RESP1b)
df.add_system_transition(State.HIPHOP_RESP1b, State.HIPHOP_Q2a,'"That\'s fine then. Soundcloud is basically a music sharing website where people can freely post music they create. Does that sound like something you\'d be interested in?"')
df.add_user_transition(State.HIPHOP_Q2a, State.HIPHOP_RESP1a, '[#ONT(yes)]')
df.set_error_successor(State.HIPHOP_Q2a, State.HIPHOP_EXIT1)


df.add_system_transition(State.HIPHOP_RESP1a, State.HIPHOP_Q2b, '"Soundcloud is a really cool website! if you play music, maybe you should post your stuff there! Don\'t you think that\'s cool?"')
df.add_user_transition(State.HIPHOP_Q2b, State.HIPHOP_RESP2b_a, '[#ONT(yes)]')
df.add_user_transition(State.HIPHOP_Q2b, State.HIPHOP_RESP2b_b, '[#ONT(no)]')
df.set_error_successor(State.HIPHOP_Q2b, State.HIPHOP_RESP2b_c)

df.add_system_transition(State.HIPHOP_RESP2b_a, State.HIPHOP_Q3a, '"Soundcloud does exactly that. The platform has allowed a lot of artists to rise and fuels creativity. Do you know any artists that have come from soundcloud?"') #
df.add_user_transition(State.HIPHOP_Q3a, State.HIPHOP_RESP3a_a, '$hiphopartist=[#ONT(artiststhatcamefromsoundcloud)]') # Yes/catch artist name
df.add_system_transition(State.HIPHOP_RESP3a_a, State.HIPHOP_Q4, '"That\'s right, " $hiphopartist " came from Souncloud. Have you heard about SoundCloud\'s recent financial issues?"')


df.add_system_transition(State.HIPHOP_RESP3a_b, State.HIPHOP_Q4, '"I didnt know $hiphop_artist came from soundcloud, but that doesnt surprise me. Many popular rappers nowadays started in their room on soundcloud. However, soundcloud apparently has a lot of issues. Have you heard about it?"') #
df.add_user_transition(State.HIPHOP_Q3a, State.HIPHOP_RESP3a_c, '{[#ONT(yes)], [#ONT(no)]}')
df.add_system_transition(State.HIPHOP_RESP3a_c, State.HIPHOP_Q4, '"You\'ve probably heard of Post Malone, he came from Soundcloud a long time ago. Now Soundcloud has a lot of issues. Have you heard about them?"')
df.set_error_successor(State.HIPHOP_Q3a, State.HIPHOP_Q3a_e)
df.add_system_transition(State.HIPHOP_Q3a_e, State.HIPHOP_Q4, '"I don\'t think I know this artist. You might be right. Have you heard of all the financial issues soundcloud is dealing with?"')

df.add_system_transition(State.HIPHOP_RESP2b_b, State.HIPHOP_Q4, '"You\'re not wrong, piracy is a big problem for the music industry. For a while I remember people were uploading a lot of copyright protected music to soundcloud. Did you know soundcloud almost shutdown?"')
df.add_system_transition(State.HIPHOP_RESP2b_c, State.HIPHOP_Q4, '"Piracy is a big problem for the music industry. For a while I remember people were uploading a lot of copyright protected music to soundcloud. Did you know soundcloud almost shutdown?"')

df.set_error_successor(State.HIPHOP_Q4, State.HIPHOP_RESP4)

df.add_system_transition(State.HIPHOP_RESP4, State.TM_CONCERT, '"SoundCloud has dealt with funding issues for a while, probably because they profit only off of streams and not live music. Have you been to any concerts?"')
df.add_system_transition(State.HIPHOP_EXIT1, State.TM_CONCERT, '"Let\'s talk about something else. Do you go to concerts?"')

##### HIPHOP ######

######################## TICKETMASTER #######################################
df.add_system_transition(State.TM_START, State.TM_CONCERT, '"The good thing about pop artists is that they\'re always on tour! Have you been to any concerts?"')
#df.add_user_transition(State.TM_START2, State.TM_TMSTART, '/.*/')
#df.add_system_transition(State.TM_TMSTART, State.TM_CONCERT, '"The good thing about pop artists is that they\'re always on tour! Have you been to any concerts?"' )
df.add_user_transition(State.TM_CONCERT, State.TM_YESCONCERT, '[#ONT(yes)]')
df.add_user_transition(State.TM_CONCERT, State.TM_NOCONCERT, '[#ONT(no)]')
df.set_error_successor(State.TM_CONCERT, State.TM_ERR1)
df.add_system_transition(State.TM_ERR1, State.TM_CONCFAV, '"Oh interesting! Who\'s someone you\'ve always wanted to see in concert?"')

#user has been to concerts
df.add_system_transition(State.TM_YESCONCERT, State.TM_LIVEARTIST, '"That\'s cool! Concerts are really fun. Who have you seen in concert?"')
df.add_user_transition(State.TM_LIVEARTIST, State.TM_LIVERES, '[#CONCERT_FIND_ARTIST()]')
df.add_system_transition(State.TM_LIVERES, State.TM_CONCADJ, '"I\'ve always wanted to see them in concert! How was it?"')
df.add_user_transition(State.TM_CONCADJ, State.TM_CONCADJS, '[#ONT(positive_response)]')
df.add_user_transition(State.TM_CONCADJ, State.TM_CONCADJSN, '[#ONT(negative_response)]')
df.add_system_transition(State.TM_CONCADJS, State.TM_CONCFAV, '"That\'s great! I\'ve heard they are really good in concert! Who have you always wanted to see in concert?"')
df.add_system_transition(State.TM_CONCADJSN, State.TM_CONCFAV, '"That\'s too bad. Some concerts just aren\'t that fun. Who have you always wanted to see in concert?"')

df.set_error_successor(State.TM_CONCADJ, State.TM_ERR7)
df.add_system_transition(State.TM_ERR7, State.TM_CONCFAV, '"Sounds like an interesting experience! Who have you always wanted to see in concert?"')

df.add_user_transition(State.TM_CONCFAV, State.TM_RANDARTIST, '[-Kendrick Lamar, -Ed Sheeran, #CONCERT_FIND_ARTIST()]')

df.add_user_transition(State.TM_CONCFAV, State.TM_KENDRICK, '[$live_artist=Kendrick Lamar]')
df.add_system_transition(State.TM_KENDRICK, State.TM_CONCOP, '"I saw him in 2018 and his concert was really fun, but he showed up about two hours late. Do you go to concerts a lot?"')
df.add_user_transition(State.TM_CONCFAV, State.TM_ED, '[$live_artist=Ed Sheeran]')
df.add_system_transition(State.TM_ED, State.TM_CONCOP, '"I saw him in 2018 and his concert was really sweet. I saw someone propose there! Do you go to concerts a lot?"')

df.set_error_successor(State.TM_CONCFAV, State.TM_ERR2)
df.add_system_transition(State.TM_ERR2, State.TM_CONCOP, '"Oh cool! I\'ve heard they\'re really good in concert. Do you go to concerts a lot?"')
df.add_system_transition(State.TM_RANDARTIST, State.TM_CONCOP, '"They would be so cool to see in concert! Do you go to concerts a lot?"')


#user does not go to concerts / TM
df.add_system_transition(State.TM_NOCONCERT, State.TM_CONCOP, '"That\'s too bad, they can be a lot of fun. Are you interested in going to concerts?"')

df.add_user_transition(State.TM_CONCOP, State.TM_FREQ, '[#ONT(yes)]')
df.add_system_transition(State.TM_FREQ, State.TM_TM, '"That\'s awesome! I wish I could go to more, but they can be expensive. Do you think the price for a concert ticket is worth it?"')
df.add_user_transition(State.TM_TM, State.TM_PRICEYES, '[#ONT(yes)]')
df.add_user_transition(State.TM_TM, State.TM_PRICENO, '[#ONT(no)]')
df.add_user_transition(State.TM_TM, State.TM_TMUNK, '#IDK')
df.add_system_transition(State.TM_TMUNK, State.TM_TMPRICE, '"It\'s definitely a great experience, but personally I think some of the extra fees are ridiculous. "')
df.add_system_transition(State.TM_PRICEYES, State.TM_TMPRICE, '"It\'s definitely a great experience, but personally I think some of the extra fees are ridiculous. "')
df.add_system_transition(State.TM_PRICENO, State.TM_TMPRICE, '"I agree. Sometimes the extra fees can be ridiculous. "')
df.set_error_successor(State.TM_TM, State.TM_ERR8)
df.add_system_transition(State.TM_ERR8, State.TM_TMPRICE, '"Hm well I think the extra fees can be ridiculous sometimes. "')


df.add_user_transition(State.TM_CONCOP, State.TM_NFREQ, '[#ONT(no)]')
df.add_system_transition(State.TM_NFREQ, State.TM_NFREQRES, '"That\'s too bad. Why not?"')
df.add_user_transition(State.TM_NFREQRES, State.TM_PRICENO, '[{expensive, money, cheap, poor, cost, costs, broke}]')
df.set_error_successor(State.TM_NFREQRES, State.TM_ERRFREQ)
df.add_system_transition(State.TM_ERRFREQ, State.TM_TM, '"That\'s too bad. I think concerts are a lot of fun, but they can be expensive. Do you think the price is worth it?"')

df.set_error_successor(State.TM_CONCOP, State.TM_ERR3)
df.add_system_transition(State.TM_ERR3, State.TM_TM, '"I think concerts are a lot of fun, but they can be expensive. Do you think the price is worth it?"')

df.add_system_transition(State.TM_TMPRICE, State.END, '')

# df.add_user_transition(State.TM_TMPRICE, State.TM_USEDY, '[#ONT(yes)]')
# df.add_system_transition(State.TM_USEDY, State.TM_STATS, '"I feel like every time I want concert tickets, I have to go through one of those. TicketMaster and Live Nation are a joint company and they own over one hundred concert venues and promote tens of thousands of concerts annually. Do you think that\'s a lot?"')
# df.add_user_transition(State.TM_TMPRICE, State.TM_USEDN, '[#ONT(no)]')
# df.add_system_transition(State.TM_USEDN, State.TM_STATS, '"That\'s surprising to hear. TicketMaster and Live Nation are a joint company that owns over one hundred concert venues and promotes tens of thousands of concerts annually. Do you think that\'s a lot?"')
#
# df.set_error_successor(State.TM_TMPRICE, State.TM_ERR4)
# df.add_system_transition(State.TM_ERR4, State.TM_STATS,'"Well TicketMaster and Live Nation are a joint company that owns over one hundred concert venues and promotes tens of thousands of concerts annually. Do you think that\'s a lot?"')
#
# df.add_user_transition(State.TM_STATS, State.TM_YSTATS, '[#ONT(yes)]')
# df.add_system_transition(State.TM_YSTATS, State.TM_MONO, '"I agree. They seem to have a monopoly over the live music industry. Because of that, they can charge whatever prices they want. Do you think that\'s fair?"')
# df.set_error_successor(State.TM_STATS, State.TM_NSTATS)
# df.add_system_transition(State.TM_NSTATS, State.TM_MONO, '"Well to put it in perspective, their sales account for 80% of all ticket sales in the U.S. Because of that, they can charge whatever prices they want. Do you think that\'s fair?"')
#
# df.add_user_transition(State.TM_MONO, State.TM_YESFAIR, '[#ONT(yes)]')
# df.add_user_transition(State.TM_MONO, State.TM_NOFAIR, '[#ONT(no)]')
# df.set_error_successor(State.TM_MONO, State.TM_ERR5)
# df.add_system_transition(State.TM_ERR5, State.TM_CEO, '"Well the CEO of Live Nation makes millions of dollars a year while his employees make very little. How do you feel about this company owning so much of the market share?"')
#
# df.add_system_transition(State.TM_YESFAIR, State.TM_CEO, '"Hm I disagree. The CEO of Live Nation makes millions of dollars a year while his employees make very little. How do you feel about this company owning so much of the market share?"')
# df.add_system_transition(State.TM_NOFAIR, State.TM_CEO, '"I agree. The CEO of Live Nation makes millions of dollars a year while his employees make very little. How do you feel about this company owning so much of the market share?"')
# df.add_user_transition(State.TM_CEO, State.TM_LAW, '/.*/')
# df.add_system_transition(State.TM_LAW, State.TM_SUGG, '"Well since 2018, the U.S. Department of Justice has actually been investigating the company for anticompetitive practices. What do you think could help bring down ticket prices?"')
#
# df.add_user_transition(State.TM_SUGG, State.TM_SUGGLAW, '[{law, laws, policy, government, bill, bills, policies, congress, senate, regulate, regulations, rules, surpreme court, department}]')
# df.add_system_transition(State.TM_SUGGLAW, State.END, '"Yeah I agree, maybe we need some new laws to regulate Ticket Master and Live Nation!"')
# df.add_user_transition(State.TM_SUGG, State.TM_BOYCOTT, '[{boycott, stop, everyone, refuse, buy, purchase, end, less, revenue, profit}]')
# df.add_system_transition(State.TM_BOYCOTT, State.END, '"Hmm, if everyone refused to buy from Ticket Master and pay those fees then maybe they would stop!"')
# df.add_user_transition(State.TM_SUGG, State.TM_SUGGUNK, '#IDK')
# df.add_system_transition(State.TM_SUGGUNK, State.END, '"Well a lot of different things could work. Maybe we need some new laws to regulate TicketMaster or some kind of boycott."')
# df.set_error_successor(State.TM_SUGG, State.TM_SUGG_ERR)
# df.add_system_transition(State.TM_SUGG_ERR, State.END, '"That could work! It would be nice if the fees were lower. "')


if __name__ == '__main__':
    df.precache_transitions()
    df.run(debugging=False)