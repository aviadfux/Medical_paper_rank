from metapub import PubMedFetcher
import pandas as pd

H_INDEX_CSV = "scimagojr 2018.csv"
SHORTCUT_JOURNALS_CSV = "jlist.csv"

class Paper(object):
    def __init__(self, pmid):
        self.pmid = pmid
        fetch = PubMedFetcher(email='anat.hashavit@gmail.com')
        article = fetch.article_by_pmid(pmid)
        self.title = article.title
        self.journal = article.journal
        self.authors = article.authors
        # pm_cited - which papers cited current paper
        try:
            self.pm_cited = fetch.related_pmids(pmid)['citedin']
        except:
            self.pm_cited = None
        self.h_index = self.get_H_index() + 1
        # self.h_index = 1
        # pm_cite - which papers cited by current paper
        self.pm_cite = []
        print("create paper with pmid" + pmid)

    def get_H_index(self):
        reasults = pd.read_csv(H_INDEX_CSV, delimiter=';', error_bad_lines=False)
        shortcut_journals = pd.read_csv(SHORTCUT_JOURNALS_CSV, error_bad_lines=False)
        try:
            # Find journal title via journal shortcut in SHORTCUT_JOURNALS_CSV table
            filt = shortcut_journals.loc[lambda df: df.NLM_TA == self.journal]
            journal_title = filt.iloc[0]["Journal_title"]

            filt = reasults.loc[lambda df: df.Title == journal_title]
            return filt.iloc[0]["H index"]
        except:
            return 0

    def add_to_pm_cite(self, pmip):
        if pmip not in self.pm_cite:
            self.pm_cite.append(pmip)