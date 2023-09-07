// 11ty config file

const eleventyNavigationPlugin = require("@11ty/eleventy-navigation");
/*
const sitemap = require("@quasibit/eleventy-plugin-sitemap"); // doesn’t with pathPrefix, doing my own
const EleventyRenderPlugin = require("@11ty/eleventy"); // doesn’t auto transform weblinks in markdown
const EleventyHtmlBasePlugin = require("@11ty/eleventy"); // doesn’t work as expected: see 11ty/eleventy#3035
 */

module.exports = (eleventyConfig) => {

	eleventyConfig.setQuietMode(true); // console output
	eleventyConfig.setUseGitIgnore(false); // use `.eleventyignore` instead
	eleventyConfig.setBrowserSyncConfig({"snippet": false}); // manually reload page if making change
	// prevent break my JS feature “change URL without reloading the page”

	// copy things, do not use js array
	eleventyConfig.addPassthroughCopy("assets/fonts/*.ttf");
	eleventyConfig.addPassthroughCopy("assets/fonts/*.woff2");
	eleventyConfig.addPassthroughCopy("assets/imgs/Martz90-Circle-Books.ico");
	eleventyConfig.addPassthroughCopy("assets/style.css");
	// js scripts go nunjucks in _includes & src/_misc

	eleventyConfig.addNunjucksFilter("makeMyLink", (value) => `<a class="MY-REF" href="${value}" target="_blank" rel="noreferrer">${value}</a>`);
	eleventyConfig.addNunjucksFilter("htmlDateString", sitemapDate); // def below
	eleventyConfig.addNunjucksFilter("findNextPrev", findNextPrevious) // def below

	eleventyConfig.addPlugin(eleventyNavigationPlugin);

	return {
		"pathPrefix": "co-han-van", // can be overidden with command line

		// mozilla nunjucks template language
		"markdownTemplateEngine": "njk",
		"dataTemplateEngine": "njk",
		"htmlTemplateEngine": "njk",

		"dir": {
			"input": "src", // default is project dir
			"includes": "../_includes", // relative to input dir
			"data": "../_data", // relative to input dir
		}
	};
};

/**
 * Returns correct timestamp format for sitemap, instead of "luxon" things
 * @param {!Date} value
 * @returns {!string}
 */
function sitemapDate(value) {
	var year = value.getFullYear(),
	    month = `${value.getMonth() + 1}`.padStart(2, "0"),
	    day = `${value.getDate()}`.padStart(2, "0"),
	    hour = `${value.getHours()}`.padStart(2, "0"),
	    minut = `${value.getMinutes()}`.padStart(2, "0"),
	    sec = `${value.getSeconds()}`.padStart(2, "0");
	return `${year}-${month}-${day}T${hour}:${minut}:${sec}+00:00`; // already UTC timezone
}

/**
 * Returns URL of next & previous chapter
 * @param {!string} key of current chapter, declared in eleventyNavigation
 * @param {!Object[]} nodes array of all chapter in same book, already sorted by order with eleventyNavigation
 * see https://github.com/11ty/eleventy-navigation/blob/master/eleventy-navigation.js
 * @returns {!{prev_url: string, next_url: string}}
 */
function findNextPrevious(key, nodes) {
	var prev_i, next_i;
	for (let i = 0; i < nodes.length; i++)
		if (nodes[i]["key"] == key) {
			prev_i = i - 1;
			next_i = i + 1;
			break;
		}

	return {
		"prev_url": prev_i < 0 ? null : nodes[prev_i]["url"],
		"next_url": next_i < nodes.length ? nodes[next_i]["url"] : null
	}
}
