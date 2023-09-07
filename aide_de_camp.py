# -*- coding: utf-8 -*-

"""
stupid helper script
how to use:

from aide_de_camp import combo, page_HanVietDich, touch_chapters, chapHeader
touch_chapters("src/han-van-nhap-mon/thien-tu-van", end=13)

while True: print("\n", combo(input("text Hant: "), input("text Viet: "), printed=False), "\n")
while True: print("\n", para_HanVietDich(input("text Hant: "), input("text Viet: "), input("text Dich: "), printed=False), "\n")

import pyperclip
pyperclip.copy(chapHeader("", "", ""))
pyperclip.copy(page_HanVietDich("""""", printed=False))
"""

import re, html, json, requests
from unicodedata import normalize as uni_norm

def escapeHTML(txt: str) -> str:
	"""transform Unicode character -> DEC numerical entity"""
	return txt.encode("ascii", "xmlcharrefreplace").decode()

html.unescape("&#21335;") # to unescape
escapeHTML(uni_norm("NFC","đức")) # composed form
escapeHTML(uni_norm("NFD","đức")) # decomposed form

# %% make ruby

thivien_url = "https://hvdic.thivien.net/transcript-query.json.php"
thivien_headers = {
	"User-Agent": "co_han_van/0.0.1 (https://github.com/phineas-pta/co_han_van) Python/3.x",
	"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

# i also shared this code at https://gist.github.com/phineas-pta/457b9f546ec20d5d2019d5799847eb01
def convertHanViet(textHan: str, printed: bool=True) -> str:
	payload = f"mode=trans&lang=1&input={textHan}"
	response = requests.request("POST", thivien_url, headers=thivien_headers, data=payload.encode())
	result = json.loads(response.text)["result"]
	res = " ".join([el["o"][0] for el in result])
	if printed: print(res)
	else: return res

Han_punc = "，、：；．。！？…⋯～／‧•●『』「」（）《》〈〉［］【】〖〗〔〕｛｝"
punc_search = str.maketrans("", "", Han_punc)

def combo(textHan: str, textViet: str, esc: bool=True, printed: bool=True, debug: bool=False) -> str:
	test0 = textHan.replace(" ", "") # remove spaces
	test1 = test0.translate(punc_search) # remove punctuation
	test2, test3 = list(test0), list(test1) # split each character: with & without punc
	textViet_ = uni_norm("NFC", textViet).replace("-", " ").split(" ")
	if debug:
		print("ckpt0:", test2)
		print("ckpt1:", test3)
		print("ckpt2:", textViet_)
		print(len(test3), len(textViet_))

	res, i, j = "", 0, 0 # combine punctuation character with a loop (see below)
	while (n := i+j) < len(test2):
		x = test2[n] # to be processed
		if debug: print("ckpt3:", x, end=" - ")
		y = escapeHTML(x) if esc else x
		if x in Han_punc:
			res += f"<ruby><rb>{y}</rb>"
			res += f"<!-- {x} -->" if esc else ""
			res += "<rt></rt></ruby>\n"
			j += 1
		else:
			if debug: print("ckpt4:", test3[i], end=" - ")
			if x != test3[i]: raise ValueError("punctuation error")
			if debug: print("ckpt5:", textViet_[i], end=" - ")
			res += f"<ruby><rb>{y}</rb>"
			res += f"<!-- {x} -->" if esc else ""
			res += f"<rt>{textViet_[i]}</rt></ruby>\n"
			i += 1
		if debug: print()
	if len(test3) != len(textViet_): raise ValueError("Han-Viet divergence")

	if printed: print(res)
	else: return res

def verse_HanViet(textHan: str, textViet: str, esc: bool=True, printed: bool=True, debug: bool=False) -> str:
	"""combine text (multiple lines) into ruby annotation in HTML"""
	text1, text2 = textHan.split("\n"), textViet.split("\n")
	res = ""
	for x, y in zip(text1, text2):
		res += combo(x.strip(), y.strip(), esc, False, debug) + "<br />\n"
	res = res[:-7] # "<br />\n"
	if printed: print(res)
	else: return res

# %% batch process file

tmp0 = '<p class="multi-lang">\n\t<span lang="zh-Hant">\n\t\t{ruby}</span><br />\n\t<span lang="vi">{dichViet}</span><br />\n\t<span lang="en">{dichAnh}</span>\n</p>'
# move {trans} around to fit the need
def para_HanVietDich(textHan: str, textViet: str, dichViet: str="", dichAnh: str="", esc: bool=True, printed: bool=True, debug: bool=False) -> str:
	tmp1 = combo(textHan, textViet, esc, False, debug).replace("\n", "\n\t\t")
	tmp1 = tmp1[:-1] # last "\t"
	res = tmp0.format(ruby=tmp1, dichViet=dichViet, dichAnh=dichAnh)
	if printed: print(res)
	else: return res

def page_HanVietDich(completePage: str, esc: bool=True, printed: bool=True, debug: bool=False) -> str:
	completePage_bis = completePage.split("\n\n")
	res = ""
	for para in completePage_bis:
		if debug: print(para)
		paraHan, paraViet, paraDichViet, paraDichAnh = para.split("\n")
		res += para_HanVietDich(paraHan, paraViet, paraDichViet, paraDichAnh, esc, False, debug) + "\n"
	res = res[:-1] # "\n"
	if printed: print(res)
	else: return res

tmp3 = '---\nlayout: lay-chap.njk\neleventyNavigation:\n  parent: "{book}"\n  key: "{placeholder}"\n  order: {num}\n---\n'
def touch_chapters(path: str, start: int=1, end: int=2) -> None:
	"""create edit-ready chapter files for each book"""
	with open(f"{path}/index.html", mode="r", encoding="utf-8") as f:
		book = f.readlines()[4].replace('  key: "', "").replace('"\n', "")
	for i in range(start, 1+end):
		filename = f"chapter-{i:03d}"
		with open(f"{path}/{filename}.html", mode="w", encoding="utf-8") as f:
			f.write(tmp3.format(book=book, placeholder=filename, num=i))

tmp4 = '<header class="subtitle">\n\t<h4>\n\t\t<span lang="zh-Hant">\n\t\t\t{ruby}</span><br />\n\t\t<span lang="en">{trans}</span>\n\t</h4>\n</header>'
def chapHeader(titleHan: str, titleViet: str, titleAnh: str) -> str:
	"""create chapter title header"""
	tmp5 = combo(titleHan, titleViet, printed=False).replace("\n", "\n\t\t\t")
	tmp5 = tmp5[:-1] # last "\t"
	print(f"title: {titleHan} {titleViet} ({titleAnh})") # for front matter
	return tmp4.format(ruby=tmp5, trans=titleAnh)

# %% batch escape/unescape HTML & unicode entities

test_txt = "<ruby><rb>&#21335;</rb><rt>Nam</rt></ruby><ruby><rb>&#28961;</rb><rt>mô</rt></ruby>"

ruby_base = re.compile(r"(?<=<rb>)[^<]+(?=</rb>)")
" ".join(map( # example
	html.unescape,
	ruby_base.findall(test_txt)
))
