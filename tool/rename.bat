@echo off

echo 動作確認
pause

rem ファイル名の一覧を取得

setlocal ENABLEDELAYEDEXPANSION

set val=.jpg
set cnt=0

for %%A in (*.jpg) do (

	set name=!cnt!%val%

	echo !name!

	ren %%A !name!

	set /a cnt=cnt+1
)

pause