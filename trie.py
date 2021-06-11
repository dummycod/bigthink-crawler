class Node:

	def __init__(self,route:str):
		self.route = route
		self.children = []
		self.finished = False

class Trie:

	def __init__(self):
		self.root = Node('*')

	def add(self,link):
		node = self.root
		link = Trie.removePrefix(link)
		routeList = link.split('/')
		for route in routeList:
			found = False
			for child in node.children :
				if route == child.route:
					found = True
					node = child
			if not found:
				new_node = Node(route)
				node.children.append(new_node)
				node = new_node
		node.finished = True

	@classmethod
	def traverse_trie_sub(cls,root,func,url=''):
		tempStr =''
		if len(url)!=0:
			tempStr = url+root.route+'/'
		else:
			tempStr = 'https://'
		if root.finished == True:
			print(tempStr)
			func(tempStr)
			return
		else:
			for child in root.children:
				Trie.traverse_trie_sub(child,func,tempStr)

	def traverse(self,func):
		Trie.traverse_trie_sub(self.root,func)

	@classmethod
	def removePrefix(cls,text):
		prefix = 'https://'
		if(text.startswith(prefix)):
			return text[len(prefix):]
		return text
