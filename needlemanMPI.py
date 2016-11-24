from mpi4py import MPI
import sys

#rows
with open(sys.argv[1], 'r') as getrow1:
  row1 = getrow1.read()
with open(sys.argv[2], 'r') as getrow2:
  row2 = getrow2.read() 

#Length of rows
lengthH1 = len(row1) + 1;
lengthH2 = len(row2) + 1;

#create the matrix
matrix = [[0 for x in range(lengthH1)] for y in range(lengthH2)];

def fillMatrix():
    #Fill row and column One with index
    for i in range(lengthH2):
      matrix[i][0] = -i;
    for j in range(lengthH1):
      matrix[0][j] = -j;

def imprimirMatrix():
    print "Best Score Obtained from Comparison>",matrix[lengthH2-1][lengthH1-1];

def needlemanWunch(rows,columns):
  for i in range(rows,lengthH2):
    for j in range(columns,lengthH1):
      match = matrix[i - 1][j - 1] + (1 if row1[j - 1] == row2[i - 1] else -1);
      inserted = (matrix[i][j - 1]) - 1;
      deleted = (matrix[i - 1][j]) - 1;
      maxScore = max(match, inserted, deleted);
      matrix[i][j] += maxScore;

def ourMPI(comm,size,rank):
	data1 = None
	rows = None
	columns = None
	if (size > lengthH2) or (size > lengthH1):
		print "You can not divide the matrix"
		MPI.Finalize()
		sys.exit()
	else:
		if rank == 0:
			data1 = [i for i in range(lengthH2)]
			data2 = [j for j in range(lengthH1)]
			rows = [[]for _ in range(size)]
			for i, chunk in enumerate(data1):
				rows[i % size].append(chunk)
			columns = [[]for _ in range(size)]
			for j, chunk in enumerate(data2):
				columns[j % size].append(chunk)
		else:
			if (rows != None) and (columns != None):
				needlemanWunch(rows,columns)
			if ( rows == None) and (columns != None):
				needlemanWunch(1,columns)
			if ( rows != None) and (columns == None):
				needlemanWunch(rows,1)
			else:
				needlemanWunch(1,1)
		data1 = comm.scatter(rows, root=0)
		data2 = comm.scatter(columns, root=0)

def main():
	comm = MPI.COMM_WORLD
	size = comm.Get_size()
	rank = comm.Get_rank()

	fillMatrix();
	ourMPI(comm,size,rank);
	imprimirMatrix();
		

if __name__ == "__main__":
  sys.exit(main())

