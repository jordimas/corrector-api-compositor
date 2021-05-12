echo API composer service performance
URL=http://localhost:5000/check

echo Short file size
ab -n 200 -c 4 -p post-data-short.txt -T 'application/x-www-form-urlencoded; charset=UTF-8' $URL 2> /dev/null | grep "9[0-9]%"

echo Medium file size
ab -n 200 -c 4 -p post-data-medium.txt -T 'application/x-www-form-urlencoded; charset=UTF-8' $URL 2> /dev/null | grep "9[0-9]%"

