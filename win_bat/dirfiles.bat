@echo off 
cd %work_path% 
for /R %%s in (*) do ( 
echo %%s 
)