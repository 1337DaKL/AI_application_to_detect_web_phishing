chrome.webNavigation.onCompleted.addListener(function(details) {
  chrome.tabs.get(details.tabId, function(tab) {
    const url = tab.url;
    console.log("User accessed URL:", url);

    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    })
    .then(res => res.json())
    .then(data => {
      console.log("Kết quả từ server:", data);
      if (data.label === 1) {
        chrome.tabs.sendMessage(details.tabId, {
          action: "alert_phishing"
        });
      }
      else if (data.label === 0) {
        chrome.tabs.sendMessage(details.tabId, {
          action: "alert_ok"
        });
      } else {
        chrome.tabs.sendMessage(details.tabId, {
          action: "check"
        });
      }
    })
    .catch(err => console.error("Lỗi gửi URL:", err));
  });
});
