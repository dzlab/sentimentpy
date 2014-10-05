__author__ = 'dzlab'

import logging
import json
from core.analyzer import Analyzer
from core.cleaner import Cleaner
from core.inout.writer import *
from core.utils.strings import StringUtils
from core.helper import WatchTime, guess_language_thread_safe


class UserAnalyzer(Analyzer):
    logger = logging.getLogger('UserAnalyzer')

    def __init__(self, cleaner=None):
        if not cleaner:
            cleaner = Cleaner()
        self.cleaner = cleaner
        self.names_by_id = {}
        self.texts_by_id = {}
        self.words_freq_by_id = {}
        self.dist_matrix = {}
        self.watch = WatchTime()

    def analyze(self, comment):
        self.watch.start()
        # ignore non english messages
        """if comment.message.startswith("u'"):
            message = unicode(comment.message)
            return"""
        if not comment.language:
            comment.set_language(guess_language_thread_safe(comment.message))

        # process the comment's message:
        # - concatenate the text of all comments of for a given user and a given text language
        words = self.cleaner.clean(comment.message)
        text = ' '.join(words)
        if not comment.user_id in self.names_by_id:
            self.names_by_id[comment.user_id] = comment.user_name
            text_by_language = {comment.language: text}
            self.texts_by_id[comment.user_id] = text_by_language
        elif not comment.language in self.texts_by_id[comment.user_id]:
            self.texts_by_id[comment.user_id][comment.language] = text
        else:
            self.texts_by_id[comment.user_id][comment.language] += ' ' + text
        self.watch.stop()

    def finalize(self, output=None, close=True):
        self.logger.info('Analyzing the comments took %s seconds' % str(self.watch.total()))
        self.watch.reset()
        # start a new watch
        self.watch.start()

        self.generate_distance_matrix()
        # write the concatenated text by user name and text language
        self.write_to_disk()

        self.watch.stop()
        self.logger.info('Finalization took %s seconds' % str(self.watch.total()))

    def generate_distance_matrix(self):
        """Generate the distance matrix between """
        for ui in self.texts_by_id:
            for lang in self.texts_by_id[ui]:
                wi = self.generate_frequency_vector(ui, lang)
                for uj in self.texts_by_id:
                    # skip if both ids are for the same user
                    if uj is ui:
                        continue
                    # skip if both users haven't texts in a common language
                    if lang not in self.texts_by_id[uj]:
                        #dist = StringUtils.words_distance(wi, {})
                        continue
                    wj = self.generate_frequency_vector(uj, lang)
                    dist = StringUtils.words_distance(wi, wj)
                    self.update_distance_matrix(ui, uj, lang, dist)

    def generate_frequency_vector(self, uid, language):
        """Generate the frequency vector for a given text"""
        if uid not in self.texts_by_id or language not in self.texts_by_id[uid]:
            return None
        text = self.texts_by_id[uid][language]
        if uid not in self.words_freq_by_id:
            self.words_freq_by_id[uid] = {}
        if language not in self.words_freq_by_id[uid]:
            self.words_freq_by_id[uid][language] = StringUtils.word_frequency(text)
        return self.words_freq_by_id[uid][language]

    def update_distance_matrix(self, ui, uj, lang, dist):
        """Update cells (ui, lang, uj) and (uj, lang, ui) of the distance matrix with the given distance"""
        if not ui or not uj or not lang:
            UserAnalyzer.logger.info('Updating distance matrix with a non valid parameter ui=%s uj=%s lang=%s' % (ui, uj, lang))
            return
        if ui not in self.dist_matrix:
            self.dist_matrix[ui] = {}
        if lang not in self.dist_matrix[ui]:
            self.dist_matrix[ui][lang] = {}
        self.dist_matrix[ui][lang][uj] = dist
        if uj not in self.dist_matrix:
            self.dist_matrix[uj] = {}
        if lang not in self.dist_matrix[uj]:
            self.dist_matrix[uj][lang] = {}
        self.dist_matrix[uj][lang][ui] = dist

    def write_to_disk(self):
        self.write_graph_to_disk()
        #self.write_texts_to_disk()

    def write_graph_to_disk(self):
        """Write a Force Layout graph for english texts"""
        UserAnalyzer.logger.debug("Writing graph data to disk")
        graph = {"nodes": [], "links": []}
        # write nodes representing users and languages
        languages = []
        pos_by_name = {}
        pos = 0
        for uid in self.names_by_id:
            node = {"name": self.names_by_id[uid], "group": 0}
            graph["nodes"].append(node)
            pos_by_name[node["name"]] = pos
            pos += 1
            for lang in self.texts_by_id[uid]:
                if lang in languages:
                    continue
                languages.append(lang)
                node = {"name": lang, "group": 1}
                graph["nodes"].append(node)
                pos_by_name[node["name"]] = pos
                pos += 1

        # write links between users and languages
        for uid in self.texts_by_id:
            for lang in self.texts_by_id[uid]:
                link = {"source": pos_by_name[self.names_by_id[uid]], "target": pos_by_name[lang]}
                graph["links"].append(link)
        #TODO write links between users based on distances

        graph_string = json.dumps(graph)
        writer = Writer(filename='graph.json')
        writer.append(graph_string)
        writer.close()

    def write_texts_to_disk(self):
        """Write the generated data into a file"""
        UserAnalyzer.logger.debug("Writing texts data to disk")
        writer = BufferedWriter(filename='messages.csv')
        writer.header('user_id, user_name, texts')
        for uid in self.texts_by_id:
            for language in self.texts_by_id[uid]:
                line = uid + ', ' + self.names_by_id[uid] + ', ' + self.texts_by_id[uid][language].encode("utf-8")
                writer.append(line)
        writer.close()