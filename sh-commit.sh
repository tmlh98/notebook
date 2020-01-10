#!/bash/bin
MSG=$1

if [ ! -n "$MSG" ]; then
	MSG=`date +"%Y-%m-%d %H:%M:%S"`

fi
git add -A


echo '----------(git add )---------'

git commit -m "${MSG}"


echo '----------(git commit )---------'


git push 

echo '----------(git push )---------'