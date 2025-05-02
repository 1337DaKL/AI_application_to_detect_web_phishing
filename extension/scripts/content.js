const url = window.location.href;
chrome.runtime.sendMessage({
  type: 'page-visited',
  url: url
});
