// inject.js
const warningDiv = document.createElement("div");
warningDiv.innerText = "⚠️ Cảnh báo: Trang web này có thể là phishing!";
warningDiv.style.position = "fixed";
warningDiv.style.top = "0";
warningDiv.style.left = "0";
warningDiv.style.width = "100%";
warningDiv.style.zIndex = "9999";
warningDiv.style.backgroundColor = "red";
warningDiv.style.color = "white";
warningDiv.style.fontWeight = "bold";
warningDiv.style.textAlign = "center";
warningDiv.style.padding = "10px";
warningDiv.style.fontSize = "18px";
document.body.appendChild(warningDiv);
