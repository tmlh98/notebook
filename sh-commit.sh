#!/bash/bin
MSG=$1

if [ ! -n "$MSG"]; then
	MSG="."
fi

git add .


echo '----------(git add )---------'

git commit -m "$MSG"


echo '----------(git commit )---------'


git push 

echo '----------(git push )---------'
