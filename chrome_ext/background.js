// var POST_ROUTE = 'http://thoughtmic.herokuapp.com/post';
var POST_ROUTE = 'http://127.0.0.1:5000/post';
var CURRENT_TAB;

// Set up context menu at install time.
chrome.runtime.onInstalled.addListener(function() {
  var context = "selection";
  var title = "Add to ReadMate";
  var id = chrome.contextMenus.create({"title": title, "contexts": [context],
                                         "id": "context" + context });  
});

function flashIcon() { 
    chrome.browserAction.setIcon({path: "chrome_ext/icon_invert16.png"});
    setTimeout(function() { 
        chrome.browserAction.setIcon({path: "chrome_ext/icon16.png"});
    }, 150);
}

chrome.browserAction.onClicked.addListener(function (tab) {
    var data = { title: tab.title, url: tab.url };
    // construct an HTTP request
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
        xhr.responseText;
        }
    }
    postHelper(xhr, POST_ROUTE, data);
    flashIcon();
});

// add click event
chrome.contextMenus.onClicked.addListener(onClickHandler);

    // The onClicked callback function.
    function onClickHandler(info, tab) {
        var data, title;
        // construct an HTTP request
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            title = getTitle(xhr.responseText);
            data = { title: title, url: info.linkUrl };
            postHelper(xhr, POST_ROUTE, data);
            flashIcon();
            }
    }
    xhr.open("GET", info.linkUrl, true);
    xhr.send();
};

//Add the link of the current tab when you use the keyboard shortcut
chrome.commands.onCommand.addListener( function(command) {
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        CURRENT_TAB = tabs[0];
        postKeyboardShortcut(CURRENT_TAB);
    });
});

function postKeyboardShortcut(tab) { 
    var tabTitle = CURRENT_TAB.title;
    var tabURL = CURRENT_TAB.url;
    var data = { title: tabTitle, url: tabURL };
    //construct an HTTP request
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
        xhr.responseText;
        }
    }
    postHelper(xhr, POST_ROUTE, data);
    flashIcon();
}


function getTitle(str) { 
    var matches = str.match(/<title>[\S\s]*?<\/title>/gi);
    return matches[0].replace(/(<\/?[^>]+>)/gi, '');
}

function postHelper(xhr, url, data) { 
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader("Content-length", data.length);

    // send the collected data as JSON
    xhr.send(JSON.stringify(data));
}
