#!/bin/bash
# 将指定目录下的proto文件编译成python

if [ $# -le 0 ]
then
	echo "mkpb.sh {dir_of_proto} {dir_of_proto} ..."
	exit 1
fi


pypb_dir="./pypb"
#protoc=../../pkg/protobuf-2.6.1/src/protoc

pb_init_file=${pypb_dir}/pb_init.py

mkdir -p ${pypb_dir}
rm -rf ${pypb_dir}/*

while [ $# -ge 1 ]
do
	proto_dir=$1
	# 编译proto到python
	# 顺便创建py文件: import所有pb
	for p in `find ${proto_dir} -name '*.proto' -type f`
	do
		protoc -I=${proto_dir} --python_out=${pypb_dir} ${p}
		modulename=`basename ${p} | cut -d'.' -f1`
		echo "import ${modulename}_pb2" >> ${pb_init_file}
	done
	shift
done

# 添加__init__.py
cd ${pypb_dir}
touch __init__.py
for d in `find . -type d`
do
	touch ${d}/__init__.py
done
