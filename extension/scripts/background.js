chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'page-visited') {
      console.log("🌐 Đã truy cập:", message.url);
      
    }
  });
  