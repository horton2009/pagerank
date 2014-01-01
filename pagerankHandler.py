#!/usr/bin/env python
#encoding=utf-8

from numpy import *
import numpy.linalg
import networkx as nx
import matplotlib.pyplot as plt
# import pdb


class pagerankHandler(object):
	def calc_pagerank(self, p, pagerankInit, pagelinkTable):
		assert p >= 0 and p <= 1
		self.p = float32(p)
		
		self.pagerankInit = pagerankInit
		self.pagelinkTable = pagelinkTable

		# print "pagerankInit"	
		# print self.pagerankInit
		# print "pagelinkTable"
		# print self.pagelinkTable

		self.Nmatrix = self.pagelinkTable
		for i in range(self.pagelinkTable.shape[0]):
			sumlink = sum(self.pagelinkTable[i,:])
			if sumlink > 0:
				self.Nmatrix[i] = self.Nmatrix[i]/sumlink
		# print self.Nmatrix

		pagerank = p*dot(self.pagerankInit, self.Nmatrix)
		# print "pagerank"
		# print pagerank
		return pagerank

	def calc_iteratation(self, p, pagerankInit, pagelinkTable, iteration, max_iteration):
		"""iteration=0 means no limitation, max_iteration=0 means no limitation"""
		if type(pagerankInit) and type(pagelinkTable) in [type([]), type(())]:
			pagerankInit = array(pagerankInit, float32)
			pagelinkTable = array(pagelinkTable, float32)

		
		if iteration > 0:
			for i in range(iteration):
				pagerank = self.calc_pagerank(p, pagerankInit, pagelinkTable)
			print "%s times iteration"%iteration
			print pagerank
			return pagerank
		elif iteration == 0:
			pagerank = pagerankInit
			k_iteration = 0
			while(1):
				k_iteration += 1
				pre_pagerank = pagerank
				print pagerank
				pagerank = self.calc_pagerank(p, pagerank, pagelinkTable)
				if max_iteration > 0:
					if k_iteration == max_iteration:#限制最大迭代次数
						print "pagerank max_iteration"
						print pagerank
						return pagerank

				for i in range(len(pagerank)):#判断是否收敛
					if pagerank[i] != pre_pagerank[i]:
						break
					else:
						if i == len(pagerank)-1:
							print "pagerank iteration"
							print pagerank
							return pagerank
	
		else:
			pass



	def draw_graph(self, pagelinkTable, it=55):
		self.node_size = 20
		self.G = nx.DiGraph()  # Create a Graph object
		print len(pagelinkTable)
		for i in range(len(pagelinkTable)):
			self.G.add_node(str(i))
		for i in range(len(pagelinkTable)):
			for k in range(len(pagelinkTable[i])):
				if pagelinkTable[i][k] == 1:
					self.G.add_edge(str(i), str(k))


		pos = nx.spring_layout(self.G, iterations=it)
		nx.draw_networkx_edges(self.G, pos, alpha=0.1)
		nx.draw_networkx_nodes(
			self.G,
			pos,
			node_size = self.node_size,
			alpha = 0.8
		)
		plt.axis('off')
		try:
			plt.savefig("webGraph.png", dpi=200)
			plt.clf()
		except Exception, e:
			print e
			time.sleep(5)
			sys.exit()



if __name__ == '__main__':
	pagelinkTable = (( 0, 1, 1, 0, 1, 0, 1),
					( 1, 0, 0, 1, 0, 0, 0),
					( 1, 1, 0, 0, 1, 0, 0),
					(0, 1, 1, 0, 1, 0, 0),
					(1, 0, 1, 1, 0, 1, 1),
					( 0, 0, 0, 0, 1, 0, 0),
					(1, 0, 0, 0, 1, 0, 0))
	pagerankInit = (0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25)
	mypagerankHandler = pagerankHandler()
	mypagerankHandler.calc_iteratation(0.85, pagerankInit, pagelinkTable, 0, 100)
	mypagerankHandler.draw_graph(pagelinkTable)