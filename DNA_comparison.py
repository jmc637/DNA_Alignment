
import sys

def read_fasta(input_file):
    '''This function reads a fasta file (assuming it only contains 1 sequence) and return the sequence as string.'''
    seq = ""
    fh = open(input_file, 'r')
    fh.readline()
    for line in fh:
        line = str.strip(line)
        seq = seq + line
    fh.close
    return seq

def take_parameter():
    '''This function takes from user input the scores for match/mismatch/gap, return the three values as integer.'''
    match = raw_input("Input your match score: ")
    mismatch = raw_input("Input your mismatch score: ")
    gap = raw_input("Input you gap score: ")
    match = int(match)
    gap = int(gap)
    mismatch = int(mismatch)
    return match, mismatch, gap

def initial_matrix(seq1, seq2):
    '''This function take two sequences, find their length m and n, return two (m+1)*(n+1) matrices (nested list) filled with value of 0 (score_matrix) and "none" (pointer_matrix).'''
    lengthSeq1 = len(seq1)
    lengthSeq2 = len(seq2)
   
    score_matrix = [[] for x in range(lengthSeq2+1)]
    for x in range(lengthSeq2+1):
        for y in range(lengthSeq1+1):
            score_matrix[x].append(0)
   
    pointer_matrix = [[] for x in range(lengthSeq2+1)]
    for x in range(lengthSeq2+1):
	for y in range(lengthSeq1+1):
	    pointer_matrix[x].append("none")
    
    return score_matrix, pointer_matrix #score_matrix stores the computed scores, pointer_matrix stores the information ("diagonal", "up", "left" or "none") for tracking back

 
def compute_matrix(seq1, seq2):
    '''This function creates score_matrix and pointer_matrix'''
    #call take_parameter() for scores
    (match, mismatch, gap) = take_parameter()
 
    #call initial_matrix() for initializaiton of score_matrix and pointer_matrix
    (score_matrix,pointer_matrix) = initial_matrix(seq1, seq2)
   
    #initialization of the diagonal, up and left scores.
    diagonal_score = 0 # Score for the "diagonal" step when tracking back, either a match or a mismatch
    up_score = 0 # Score for the "up" step when tracking back, insert a gap in the (first or second?) sequence
    left_score = 0 # Score for the "left" step when tracking back, insert a gap in the (first or second?) sequence
    
    #initialization of the max score and its position in matrix
    max_score = 0
    iMax = 0
    jMax = 0
    
    
    #fill in the score_matrix and keep track ("diagonal", "up", "left" or "none") in the pointer_matrix. Also keep track of the max_score and its position.
    #use nested for loops to accomplish your task --> return what you are asked for

    for y in range(len(score_matrix)):
        if y == 0:
	    continue
        for x in range(len(score_matrix[y])):
	     if x == 0:
  	         continue    
             diagonal_score = score_matrix[y-1][x-1]
	     if seq1[x-1].upper() == seq2[y-1].upper():
	         diagonal_score = diagonal_score + match 
	     else:
	         diagonal_score = diagonal_score + mismatch
	     up_score = score_matrix[y-1][x] + gap
	     left_score = score_matrix[y][x-1] + gap
 	     max = 0
	     if diagonal_score >= up_score:
                  if diagonal_score >= left_score:
		      max = diagonal_score
		      if max <= 0:
		          max = 0
		      else:
		          pointer_matrix[y][x] = "diagonal"
		  else:
		      max = left_score
		      if max <= 0:
		          max = 0
	              else:
		          pointer_matrix[y][x] = "left"
	     else:
	         if up_score >= left_score:
		      max = up_score
		      if max <= 0:
			  max = 0
		      else:
		          pointer_matrix[y][x] = "up"
		 else:
		      max = left_score
		      if max <= 0:
		          max = 0
		      else:
		          pointer_matrix[y][x] = "left"
	     score_matrix[y][x] = max
             if	max > max_score:
		max_score = max
		iMax = x
		jMax = y
    return score_matrix, pointer_matrix, iMax, jMax
 
def print_score_matrix(score_matrix):
    '''This function prints score matrix'''
    for y in range(len(score_matrix)):
        rowY =""
        for x in range(len(score_matrix[y])):
	    rowY = rowY + str(score_matrix[y][x]) + " "
        print rowY
    return


def track_back(pointer_matrix, seq1, seq2, iMax, jMax):
    '''Tracks back to create the aligned sequence pair'''
    #initialization of aligned sequences
    aligned_seq1 = ''
    aligned_seq2 = ''
    
    #start from the position where the max score is.
    i = iMax
    j = jMax
    
    #track backwards in the pointer_matrix, based on the info ("diagonal", "up", "left" or "none") decide for each position whether it is a match/mismatch, a gap in the first/second sequence, or to stop.
    pointer = pointer_matrix[j][i]
    while pointer != "none":
        if pointer == "diagonal":
	    aligned_seq1 = seq1[i-1] + aligned_seq1
	    aligned_seq2 = seq2[j-1] + aligned_seq2
	    i = i - 1
            j = j - 1
	elif pointer == "up":
	    aligned_seq1 = "-" + aligned_seq1
	    aligned_seq2 = seq2[j-1] + aligned_seq2
	    j = j - 1
	else:
	    aligned_seq1 = seq1[i-1] + aligned_seq1
	    aligned_seq2 = "-" + aligned_seq2
	    i = i - 1 
        pointer = pointer_matrix[j][i] 
    return (aligned_seq1, aligned_seq2)

#Main

#Call read_fasta() and print the two sequences to be aligned.
input1 = raw_input("Please input your first fasta file: ")
input2 = raw_input("Please input your second fasta file: ")
seq1 = read_fasta(input1)
seq2 = read_fasta(input2)
print "The first sequence is: " + seq1
print "The second sequence is: " + seq2

#Call compute_matrix() and calculate the matrix.
(score_matrix, pointer_matrix, iMax, jMax) = compute_matrix(seq1, seq2)

#Call print_score_matrix() to display the matrix
print_score_matrix(score_matrix)


#Call track_back() to get the aligned sequences.
(aligned_seq1, aligned_seq2) = track_back(pointer_matrix, seq1, seq2, iMax, jMax)

print aligned_seq1
print aligned_seq2
