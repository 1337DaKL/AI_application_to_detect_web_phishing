chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "alert_phishing") {
        const banner = document.createElement("div");
        banner.textContent = "🚨 CẢNH BÁO: TRANG WEB NÀY CÓ DẤU HIỆU LỪA ĐẢO!";
        banner.style.position = "fixed";
        banner.style.top = "0";
        banner.style.left = "0";
        banner.style.width = "100%";
        banner.style.zIndex = "9999";
        banner.style.backgroundColor = "red";
        banner.style.color = "white";
        banner.style.fontSize = "20px";
        banner.style.textAlign = "center";
        banner.style.padding = "15px";
        banner.style.fontWeight = "bold";
        banner.style.boxShadow = "0 4px 6px rgba(0,0,0,0.2)";
        banner.style.fontFamily = "Arial, sans-serif";
        document.body.appendChild(banner);
    }
});
