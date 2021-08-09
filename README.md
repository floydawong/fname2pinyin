# File Name To Pinyin

> 文件名转换成拼音

## 生成 Pyd

- `pip install cython`
- `python setup.py build_ext --inplace`

## 使用

- 在`fname2pinyin`文件夹中, 双击`fname2pinyin.sh`, 可将`res`文件夹中的所有文件的名字, 转成拼音格式.

## 使用`Pyinstaller`生成`EXE`

```bash
# install
pip install pyinstaller

## -D(默认选项)，生成build、dist目录，该选项生成一个目录(包含多个文件)来作为程序
pyinstall -D app.py

## 使用-F选项，在dist目录下生成单独的EXE文件(在Mac生成的文件没有exe后缀)
pyinstaller -F app.py

## -w不显示GUI窗口，-i指定图标
pyinstaller -F -w -i app.ico app.py
```

我们使用`pyinstaller -D fname2pinyin.py`来生成 EXE 文件, 然后将`res`和`xpinyin`放到`dist`目录里
