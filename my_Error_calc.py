def sentence_error(hyp_utt,test_utt): # This function accepts one line for hyp and test
	sub_fix = '***'
	Del = 0
	Ins = 0
	Sub = 0
	Correct = 0
	Sen_err = 0
	
	hyp_words = hyp_utt.split()
	test_words =test_utt.split()
	hyp_nwords = len(hyp_words)
	test_nwords = len(test_words)
	## Deletion 
	if (hyp_nwords > test_nwords):
		n= hyp_nwords-test_nwords
		for i in range(test_nwords,test_nwords+n):
			test_words.insert(i,'#')
		flag = 0
		test_ind = 0
		for ind in range(0,hyp_nwords):
			if (hyp_words[test_ind]<> test_words[ind]) and (test_words[ind] <> '#'):
				k=0
				for i in range(test_ind,len(hyp_words)):
					if test_words[ind] <> hyp_words[i]:
						flag=0
						k=k+1
					else:
						flag =1
						test_ind = i
						break
						
				if flag == 1:
					for i in range(0,k):
						test_words.insert(ind,sub_fix)
						Del = Del+1
			elif (test_words[ind] == '#'):
				test_words.insert(ind,sub_fix)
				Del = Del+1
				
			else:
				test_ind = test_ind+1
				
			
		Sen_err =1
		#remove # 
		print ' '.join(test_words)
		for i in range(0,test_words.count('#')):
			test_words.remove('#')
		
	## Insertion detection
	if (hyp_nwords < test_nwords):
		n= test_nwords-hyp_nwords
		for i in range(hyp_nwords,hyp_nwords+n):
			hyp_words.insert(i,'#')
		
		flag=0
		test_ind=0
		for ind in range(0,test_nwords):
			
			if (hyp_words[ind]<> test_words[test_ind]) and (hyp_words[ind] <> '#'):
				k=0
				for i in range(test_ind,len(test_words)):
					if hyp_words[ind] <> test_words[i] and n>0:
						flag=0
						k=k+1
						n=n-1
					else:
						flag =1
						test_ind = i
						break
						
				if flag == 1:
					for i in range(0,k):
						hyp_words.insert(ind,sub_fix)
						Ins = Ins+1
					
			elif hyp_words[ind] == '#':
				hyp_words.insert(ind,sub_fix)
				Ins = Ins+1
				
			else:
				test_ind = test_ind+1
			
			if n<= 0:
				break
		Sen_err =1
		
		## Clean text from '#'
		print ' '.join(hyp_words)
		for i in range (0,hyp_words.count('#')):
			hyp_words.remove('#')
		
	## Substiution 
	for ind in range(0,len(hyp_words)):
		if ( hyp_words[ind] <> test_words[ind]):
			if ((hyp_words[ind] <> sub_fix) and (test_words[ind] <> sub_fix)):
				Sub=Sub+1
				Sen_err=1
		else:
			Correct = Correct+1	
	return(Ins,Del,Sub,Correct,Sen_err)

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
#input_test_file = 'cmu_en_us_Decoded.txt'
def CalcWER(input_hyp_file,input_test_file):
	#input_hyp_file = 'hyp.txt'
	#input_test_file = 'test.txt'


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
	N_lines = len(hyp_sentences)
	for n in range(0,N_lines):
		[T_Ins,T_Del,T_Sub,T_Correct,T_Sen_err] = sentence_error(hyp_sentences[n].upper(),test_sentences[n].upper())
		Ins=Ins+T_Ins
		Del = Del+T_Del
		Sub = Sub+T_Sub
		Correct=Correct+T_Correct
		Sen_err = Sen_err+T_Sen_err
	
## Error Rate Calculations
	N = Sub + Del + Correct
	ERR = Sub + Del + Ins
	WERP = 100*ERR/float(N)		

	print "Correct:",Correct
	print "Insertion:",Ins
	print "Deletion:", Del
	print "Substiution:", Sub
	print "Sentence Error:",Sen_err
	print "Word Error rate:",WERP,"%"	


	f_hyp.close()
	f_test.close()