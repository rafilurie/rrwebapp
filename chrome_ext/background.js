// var POST_ROUTE = 'http://thoughtmic.herokuapp.com/post';
var POST_ROUTE = 'http://127.0.0.1:5000/post';
var CONTEXT_MENU_TITLE = "Add to ThoughtMic";
var CHROME_ICON_WHITE = "chrome_ext/icon_invert16.png";
var CHROME_ICON_BLACK = "chrome_ext/icon16.png";
var FLASH = 150;

// Set up context menu at install time.
chrome.runtime.onInstalled.addListener(function() {
  var context = "selection";
  var title = CONTEXT_MENU_TITLE;
  var id = chrome.contextMenus.create({"title": title, "contexts": [context],"id": "context" + context });
});

function _getTitle(str) {
    var matches = str.match(/<title>[\S\s]*?<\/title>/gi);
    return matches[0].replace(/(<\/?[^>]+>)/gi, '');
}

function _flashIcon() {
    chrome.browserAction.setIcon({path: CHROME_ICON_WHITE});
    setTimeout(function() {
        chrome.browserAction.setIcon({path: CHROME_ICON_BLACK});
    }, FLASH);
}

function _postHelper(xhr, url, data) {
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader('Content-length', data.length);
    xhr.send(JSON.stringify(data));
}

chrome.browserAction.onClicked.addListener(function (tab) {
    var data = { title: tab.title, url: tab.url };
    var xhr = new XMLHttpRequest();
    _postHelper(xhr, POST_ROUTE, data);
    _flashIcon();
});

function contextMenusOnClickHandler(info, tab) {
    var title = url = info.linkUrl;
    var data = { title: title, url: url };
    var xhr = new XMLHttpRequest();

    $.ajax({
      url: url,
      crossDomain: true,
      success: function(html) {
        data.title = _getTitle(html);
        _postHelper(xhr, POST_ROUTE, data);
        _flashIcon();
      },
      error: function(a, b, c) {
        _postHelper(xhr, POST_ROUTE, data);
      }
    });
};
chrome.contextMenus.onClicked.addListener(contextMenusOnClickHandler);

function _postKeyboardShortcut(tab) {
    var title = tab.title;
    var url = tab.url;
    var data = { title: title, url: url };

    var xhr = new XMLHttpRequest();
    _postHelper(xhr, POST_ROUTE, data);
    _flashIcon();
}

chrome.commands.onCommand.addListener( function(command) {
  var currentTab;
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        currentTab = tabs[0];
        _postKeyboardShortcut(currentTab);
    });
});
