def printSubSequences(STR, subSTR=""):
	"""
	function:
		To print all subsequences of string
		concept:
			Pick and Don’t Pick
		variables:
			STR = string
			subSTR = to store subsequence
	"""
	if len(STR) == 0:
		print(subSTR, end=" ")
		return

	# we add adding 1st character in string
	printSubSequences(STR[:-1], subSTR + STR[-1])
	"""
	Not adding first character of the string
	because the concept of subsequence either
	character will present or not
	"""
	printSubSequences(STR[:-1], subSTR)
	return


STR = "abc"
printSubSequences(STR)




