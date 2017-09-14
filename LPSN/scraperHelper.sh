# Helper script for calling python LPSN scraper, and cleaning up output files

echo -n "Date: " 
date --iso-8601

python main.py

OUTPUTDIR="output/`date --iso-8601`" 
mkdir -p $OUTPUTDIR/

cat species*.csv > total_species.csv
cat genera*.txt > total_genera.txt
cat summary*.txt > total_summary.txt
echo  >> total_summary.txt
echo -n "Total number of valid species names: " >> total_summary.txt
echo `cat total_species.csv | wc -l` >> total_summary.txt
echo -n "Total number of valid genus names: " >> total_summary.txt
echo `cat total_genera.txt | wc -l` >> total_summary.txt
echo -n "Total number of Candidatus species names: " >> total_summary.txt
echo `cat candidatus_species.csv | wc -l` >> total_summary.txt
echo -n "Total number of Candidatus genus names: " >> total_summary.txt
echo `cat candidatus_genus.csv | wc -l` >> total_summary.txt
echo -n "Total number of Candidatus names for other ranks: " >> total_summary.txt
echo `cat candidatus_other.csv | wc -l` >> total_summary.txt
echo "\n\n\n"
echo -n "Total number of invalid Species names: " >> total_summary.txt
echo `cat invalid_species.csv | wc -l` >> total_summary.txt
echo -n "Total number of invalid genus names: " >> total_summary.txt
echo `cat invalid_genus.txt | wc -l` >> total_summary.txt
echo -n "Total number of invalid names for other ranks: " >> total_summary.txt
echo `cat invalid_other.txt | wc -l` >> total_summary.txt


echo "\n\n"



mv *.txt $OUTPUTDIR
mv *.csv $OUTPUTDIR
mv *.html $OUTPUTDIR

