#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include  <string>
#include "ICTCLAS/ICTCLAS50.h"
#include <fstream>
#include <map>

using namespace std;

#define DEBUG 1	//开启调试模式
#define DB_PATH "d:/Downloads/MYcpp/test/db.conf"	//数据库配置文件路径
#define ICTTABLE_PATH "d:/Downloads/MYcpp/test/icttable.conf"	//待转换的数据表以及待转化字段保存字段的信息
#define MAX 80

int readconf(char *path);

int main()
{
	//读入数据库配置文件db.conf
	//读入转化配置文件ictclastable.conf
	readconf(DB_PATH);


	//链接数据库

	//依次调用数据转换函数

	//回写数据库

	return 1;
}

int readconf(char *path){
    char tmpline[MAX];
    map<String,String> ConfData;
	ifstream Cfile(path);
	if(!Cfile.is_open()){
		cout<<"error:file open fault locate "+*path<<endl;
		return -1;
	}
	while(Cfile){
		Cfile.getline(tmpline,MAX);
		if(DEBUG)cout<<tmpline<<endl;
		tmpline.
	}
	//存入Map

	//返回map指针
	return 0;
}
