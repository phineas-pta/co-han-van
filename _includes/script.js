"use strict";

// PWA register thing go nunjucks

const parser = new DOMParser(), // to deal with raw html
      y = "yesssss", dkey = "dark"; // keyword for dark theme

// placeholder for various html element
var hamburger;

// when everything ready
window.onload = () => {

	// trigget hamburger: https://bulma.io/documentation/components/navbar/
	hamburger = document.getElementById("hamburger");
	hamburger.onclick = () => { // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
		hamburger.classList.toggle("is-active");
		document.getElementById("myMenu").classList.toggle("is-active");
	};

	// dark mode toggle
	var themeSwitch = document.getElementById("themeSwitch");
	themeSwitch.onchange = darkToggle;
	var dstate = window.localStorage.getItem(dkey);
	if (dstate === y || (dstate == null && window.matchMedia(`(prefers-color-scheme: ${dkey})`).matches))
		themeSwitch.checked = true; // pre-check the dark-theme checkbox
	themeSwitch.onchange(); // check initial state

	// change url without reloading
	document.getElementById("home-button").onclick = noHistoryChange; // def below
	for (let el of document.querySelectorAll("a.MUC-LUC"))
		el.onclick = noHistoryChange;

	// remove blur once page loaded
	document.getElementById("main").classList.remove("skeleton-block");
};

// event: click back/forward button in browser => change url without reloading
window.onpopstate = (e) => {
	fetch(window.location.pathname)
		.then((response) => response.text())
		.then(replaceHTML); // def below
		// ATTENTION no window.history.pushState
};

// dark mode toggle
function darkToggle() {
	if (this.checked) {
		document.documentElement.setAttribute("data-theme", "dark");
		this.nextSibling.textContent = "\uD83C\uDF19"; // \u{1F319} 🌙 surrogate pair
		return window.localStorage.setItem(dkey, y); // save state
	} else {
		document.documentElement.setAttribute("data-theme", "light");
		this.nextSibling.textContent = "\u2600\uFE0F"; // ☀️ with modifier
		return window.localStorage.setItem(dkey, "tdyutrghjtucvghjtc"); // something random not important
	}
}

// change url without reloading
function noHistoryChange(event) {
	event.preventDefault(); // prevent loading when clicking
	fetch(this.href)
		.then((response) => response.text())
		.then((newPageHTML) => { // load the new page
			window.history.pushState(null, null, this.href); // change url
			replaceHTML(newPageHTML);
		})
	return null;
}

function replaceHTML(txt) { // don’t use document.write() coz doesn’t trigger window.onload() properly
	var htmlDoc = parser.parseFromString(txt, "text/html");
	document.head.innerHTML = htmlDoc.head.innerHTML;
	document.body.innerHTML = htmlDoc.body.innerHTML;
	window.scrollTo(0, 0); // reset scroll position
	window.onload(); // trigger rendering
}
