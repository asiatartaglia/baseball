import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idmapTeams = {}
        self._bestPath = []
        self._bestObjVal = 0


    def getPath(self,v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        for v in self.grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

    def _ricorsione(self,parziale):
        #condizione di ottimalità verifico se la parziale è migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        #condizione di terminazione verifico se posso continuare


        #faccio la mia ricorsione
        for v in self.grafo.neighbors(parziale[-1]):
            pesoE = self._grafo[parziale[-1]][v]["peso"]

            if self._grafo[parziale[-2]][parziale[-1]]["peso"] > pesoE and v not in parziale:
              parziale.append(v)
              self._ricorsione(parziale)
              parziale.pop()

    def _score(self,parziale):
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._grafo[parziale[i][parziale[i+1]]["peso"]]

        return score


    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)

        myedges = itertools.combinations(self._teams, 2)
        self._grafo.add_edges_from(myedges)

        mapSalary = DAO.getSalariesOfTeam(year, self._idmapTeams)

        for e in self._grafo.edges:
            sal1 = mapSalary.get(e[0],0)
            sal2 = mapSalary.get(e[1],0)
            peso = sal1 + sal2
            self._grafo[e[0]][e[1]]["peso"] = peso

        print ("test")

        # aggiunge un arco fra ogni coppia di nodi possibile
        # for u in self._grafo.nodes:
        #    for v in self._grafo.nodes:
        #       if u != v:
        #           self._grafo.add_edge(u, v)

    def getVicini(self,source):
        vicini = self._grafo.neighbors(source)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v,self._grafo[source][v]["peso"]))

        viciniTuples.sort(key=lambda x: x[1])
        return viciniTuples

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        self._idmapTeams = {t.ID : t for t in self._teams}
        return self._teams

    def getAllYear(self):
        return DAO.getAllYear()