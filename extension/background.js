chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url.startsWith("http")) {
      fetch("https://chatgpt.com/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"    
        },
        body: JSON.stringify({ url: tab.url })
      })
      .then(response => response.json())
      .then(data => {
        if (data.phishing === true) {
          chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ["inject.js"]
          });
        }
      })
      .catch(error => console.error("Lỗi gọi API:", error));
    }
  });
  