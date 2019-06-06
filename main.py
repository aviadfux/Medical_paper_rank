from Paper_Network import P_N
import page_rank_alg as pr

rsp=0.31

def main():
    papers_network = P_N("input.csv")
    papers_network.create_network()

    edgeWeights, papers_h_index = papers_network.get_network_edges_weights()
    wordProbabilities = pr.powerIteration(edgeWeights, papers_h_index, rsp=rsp)
    v=9

if __name__ == '__main__':
    main()