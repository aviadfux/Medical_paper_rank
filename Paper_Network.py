import csv
import collections
from Paper import Paper

RECURSION_DEGREE = 5

class P_N(object):
    def __init__(self, csv_name):
        self.papers_dict = {}
        self.csv_papers = []
        self.read_csv_file(csv_name)

    def read_csv_file(self, csv_name):
        with open(csv_name) as csvfile:
            # readCSV = csv.reader(csvfile, delimiter='\n')
            for row in csvfile:
                paper = Paper(row.split('/')[-1].split('\n')[0])
                self.papers_dict[paper.pmid] = paper
                self.csv_papers.append(paper.pmid)

    def create_network(self):
        for paper_pmid in self.csv_papers:
            self.recursion_search_citations(paper_pmid, RECURSION_DEGREE)


    def recursion_search_citations(self, paper_pmid, k):
        """
        recursion function for search the papers that cited the original paper
        :param paper_pmid: the original paper pmid
        :param k: the number of recursion iterations
        :return: None (append all papers to self.papers_dict)
        """
        if k == 0: return

        original_paper = self.papers_dict[paper_pmid]
        if original_paper == None or original_paper.pm_cited == None: return

        for new_paper_pmid in original_paper.pm_cited:
            if new_paper_pmid not in self.papers_dict:
                new_paper = Paper(new_paper_pmid)
                new_paper.add_to_pm_cite(paper_pmid)
                self.papers_dict[new_paper.pmid] = new_paper
            else:
                self.papers_dict[new_paper_pmid].add_to_pm_cite(paper_pmid)
            self.recursion_search_citations(new_paper_pmid, k - 1)

    def get_network_edges_weights_(self):
        edgeWeights = collections.defaultdict(lambda: collections.Counter())
        papers_h_index = {}

        for pmid, paper in self.papers_dict.items():
            papers_h_index[pmid] = paper.h_index
            if paper.pm_cited==None:
                edgeWeights[pmid] = collections.Counter()
            else:
                for paper_that_cited in paper.pm_cited:
                    if paper_that_cited in self.papers_dict:
                        neighborPaper = self.papers_dict[paper_that_cited]
                        edgeWeights[pmid][neighborPaper.pmid] = self.papers_dict[pmid].h_index

        return edgeWeights, papers_h_index

    def get_network_edges_weights(self):
        edgeWeights = collections.defaultdict(lambda: collections.Counter())
        papers_h_index = {}

        for pmid, paper in self.papers_dict.items():
            papers_h_index[pmid] = paper.h_index
            if paper.pm_cite==None:
                edgeWeights[pmid] = collections.Counter()
            else:
                for paper_that_cite in paper.pm_cite:
                    if paper_that_cite in self.papers_dict:
                        neighborPaper = self.papers_dict[paper_that_cite]
                        edgeWeights[pmid][neighborPaper.pmid] = self.papers_dict[pmid].h_index

        return edgeWeights, papers_h_index