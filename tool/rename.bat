@echo off

echo ����m�F
pause

rem �t�@�C�����̈ꗗ���擾

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