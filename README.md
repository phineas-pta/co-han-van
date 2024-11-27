![License](https://img.shields.io/github/license/phineas-pta/co-han-van?logo=unlicense)
![Eleventy](https://img.shields.io/badge/made%20with-11ty-blue?logo=eleventy)
![Bulma](https://img.shields.io/badge/made%20with-Bulma-blue?logo=bulma)
![GitHub last commit](https://img.shields.io/github/last-commit/phineas-pta/co-han-van?logo=git)
![GitHub deployments](https://img.shields.io/github/deployments/phineas-pta/co-han-van/github-pages?logo=githubactions&label=Github%20page)
![GitHub code size](https://img.shields.io/github/languages/code-size/phineas-pta/co-han-van?logo=github)
![GitHub repo size](https://img.shields.io/github/repo-size/phineas-pta/co-han-van?logo=github)

# cổ hán văn - classical chinese texts

collection of some classical chinese texts - tuyển tập 1 số tác phẩm hán văn cổ điển
- Lỗ Bình Sơn, 2012, web “cổ hán văn” https://web.archive.org/web/sitemap/cohanvan.com
- Donald Sturgeon, 2019, “Chinese Text Project” 中國哲學書電子化計劃 https://ctext.org/

**DISCLAIMER: this is a hobby project, academic accuracy not guaranteed, also i do compilation not translation**

any translations should be copyright-expired works found on internet

getting started with NodeJS:
```bash
npm install npm@latest -g
npm init -y
npm install @11ty/eleventy sass bulma @11ty/eleventy-navigation # node-sass depreciated
# npm update
```
ATTENTION: not same package `@11ty/eleventy` ≠ `eleventy`

it's a bit messy and not entirely in english 😅 so here a bit explaination about folder structure
- all the html files are in `src/` and i set a `pathPrefix`
- CSS file is generated from SASS file in `assets/` so u have to compile it 1st
- JS files (not eleventyConfig) are in `src/_misc/js-*.njk` which include other JS from `_includes/*.js` 😅
- folder structure go like this:
```
src/
├─ subject-1/
│  ├─ book-1/
│  │  ├─ chapter-1.html
│  │  ├─ chapter-2.html
│ ...
│  ├─ book-2/
│  │  ├─ chapter-1.html
│  │  ├─ chapter-2.html
│ ...
├─ subject-2/
│  ├─ book-3/
│ ...
```

using 11ty:
- convert SASS to CSS: `npx sass --no-source-map assets` (run 1st to get CSS file)
- `&&` sucks with windows powershell
- build with `npx @11ty/eleventy`
- or directly serve with `npx @11ty/eleventy --serve`
- with sub dir: add ` --pathprefix yolo`

docker ?? no option to change host

additional setup:
- Favicon: https://www.iconarchive.com/download/i75808/martz90/circle/books.ico
- AR PL (Arphic Public Licensed) UKaiHK font: https://github.com/SilentByte/fonts-arphic-ukai/blob/master/fonts-arphic-ukai/ukai.ttc, under the [Arphic public license](assets/fonts/ARPHICPL.txt)
- Grenze Gotisch font: https://github.com/Omnibus-Type/Grenze-Gotisch, under the [SIL OFL v1.1](assets/fonts/OFL.txt)
- Font Awesome: https://github.com/FortAwesome/Font-Awesome/releases, under the [SIL OFL v1.1](assets/fonts/OFL.txt)

UKaiHK font: originally `.ttc` → use FontForge to extract `.ttf` № 2 (HK)

copy raw text with ctext api like `https://ctext.org/plugins/textexport/#en||ctp:analects/xue-er`

## misc

![](https://tokei.rs/b1/github/phineas-pta/co-han-van?category=files)
![](https://tokei.rs/b1/github/phineas-pta/co-han-van?category=lines)
![](https://tokei.rs/b1/github/phineas-pta/co-han-van?category=code)
![](https://tokei.rs/b1/github/phineas-pta/co-han-van?category=comments)
![](https://tokei.rs/b1/github/phineas-pta/co-han-van?category=blanks)
