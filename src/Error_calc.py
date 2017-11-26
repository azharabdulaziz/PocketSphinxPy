def sentence_error(hyp_utt,test_utt): # This function accepts one line for hyp and test
	#################### Detect Insertion and Deletion only ########################################
	Del = 0
	Ins = 0
	Sub = 0
	Sen_err = 0
	no_words = len(hyp_utt.split())
	if ( (len(hyp_utt.split())) > len(test_utt.split())):
		Del=(len(hyp_utt.split()) - len(test_utt.split()))
		Sen_err =1
	elif ( (len(hyp_utt.split())) < len(test_utt.split())):
		Ins=( len(test_utt.split())- len(hyp_utt.split()))
		Sen_err =1
	 
	#else: test_utt

	##################################################################################################

	#################### Calculate Distance Matrix ########################################
	# The Levenshtein distance between two sequences is the simplest
	# weighting factor in which each of the three operations has a cost of 1 (Levenshtein,
	# 1966). *Thus the Levenshtein distance between 'intention' and 'execution'
	# is 5*. 
	# Levenshtein also proposed an alternate version of his metric in
	# which each insertion or deletion has a cost of one, and substitutions are not
	# allowed (equivalent to allowing substitution, but giving each substitution a
	# cost of 2, since any substitution can be represented by 1 insertion and 1 deletion).
	Correct = 0	
	hyp_wordlist = []
	test_wordlist = []
	test_line = test_utt
	hyp_wordlist = hyp_utt.split()
	test_wordlist = test_line.split()
	h_len = len(hyp_utt.split())
	t_len = len(test_line.split())
	Dist = [[0 for x in range (t_len+1)] for x in range (h_len+1)]  # Initialize Dist matrix
	dummy = h_len
	for r in range(0,h_len+1): # All rows , first column (column 0)
		Dist[r][0] = dummy
		dummy= dummy-1
		
	dummy = 0
	for c in range(0,t_len+1): # All columns , final raw (raw h_len)
		Dist[h_len][c] = dummy
		dummy= dummy+1

	m = 0   	# m is the local distance(cost)measure. 
				# For Deletion or Insertion m=1, m=2 
				# for substitution and m=0 for no operation. For simplicity m=1 or 0.
				
	Ins_cost=1  #  Costs are not equal according to Levenshtein,1966
	Del_cost=1 
	Sub_cost=2 

	hyp_count = 0
	test_count = 0
	for row in range(1,t_len+1):
		
		for col in range(h_len-1,-1,-1):
			diag_cell=Dist[col+1][row-1]
			left_cell=Dist[col+1][row]
			down_cell=Dist[col][row-1]
			
			if (hyp_wordlist[hyp_count]) <> (test_wordlist[test_count]):
				m=Sub_cost
				
			else:
				m=0
				Correct =Correct + 1
			Dist[col][row]=min(min(diag_cell+m,left_cell+Ins_cost),down_cell+Del_cost)
			hyp_count = hyp_count + 1
			
		test_count = test_count + 1	
		hyp_count = 0
	Distance = (Dist[0][t_len])
	if(Correct > no_words):
		Correct = no_words
	############################### Print Word Dist for each Utterance ##############	

	############################## Print The distance matrix
	#print "\n --------------- Distance Matrix --------------- \n"
	#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
	#	  for row in Dist]))
	#print "\n ----------------------------------------------- \n"
	####################################################################################
	
		#################### Detect Substitution  ###############################
	if Distance > 0:
		if Del==Ins==0:
			Sub = Distance/2
		else:
			if Distance-(Del+Ins) >  0:
				Sub = (Distance-(Del+Ins))/2
			else:
				Sub = 0
		
	return(Ins,Del,Sub,Correct,Sen_err,no_words)

############################## Test Validity ####################################################
def test_validity(input_hyp_file,input_test_file):

	hyp = open(input_hyp_file,'r')  # Read Hypothesis file
	test = open(input_test_file,'r') # Read Decoded file
	hyp_nlines = len(hyp.readlines())
	test_nlines = len(test.readlines())
	if test_nlines <> hyp_nlines:
		return(False)
		
	hyp.close()
	test.close()
	return(True)
	################################################################################################

###################################### Main Function ######################################
import sys
#input_hyp_file = 'cmu_en_us.txt'
#input_test_file = 'Transcribed_remote2.txt'
def CalculateWER(input_hyp_file,input_test_file):
#input_hyp_file = 'ref.txt'
#input_test_file = 'hyp.txt'

#input_hyp_file = 'TestCorpus.txt'
#input_test_file = 'SG_Decoded.txt'

	if (test_validity(input_hyp_file,input_test_file) == False):
		sys.exit("Error: Number of utterances in Hypothesis and test utterances are not equal!")
	f_hyp = open(input_hyp_file,'r')
	f_test =open(input_test_file,'r')

	hyp_sentences = f_hyp.readlines()
	test_sentences = f_test.readlines()
###### Read line by line both Hyp and test files and call sentence_error
	Ins=0
	Del=0
	Sub=0
	Correct=0
	Sen_err=0
	total_words = 0
	N_lines = len(hyp_sentences)
	for n in range(0,N_lines):
		[T_Ins,T_Del,T_Sub,T_Correct,T_Sen_err,no_words] = sentence_error(hyp_sentences[n].upper(),test_sentences[n].upper())
		Ins=Ins+T_Ins
		Del = Del+T_Del
		Sub = Sub+T_Sub
		Correct=Correct+T_Correct
		Sen_err = Sen_err+T_Sen_err
		total_words = total_words+no_words
	
## Error Rate Calculations
	N = Sub + Del + Correct
	ERR = Sub + Del + Ins
	WERP = 100*ERR/float(N)		

	print "Total No of sentences (lines): ", N_lines
	print "Total Words:",total_words
	print "Correct:",Correct
	print "Insertion:",Ins
	print "Deletion:", Del
	print "Substiution:", Sub
	print "Sentence Error:",Sen_err
	print "Word Error rate:",WERP,"%"	


	f_hyp.close()
	f_test.close()