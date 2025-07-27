
let cryptoTicker = "BTCUSDT";  

function fetchCryptoData() {
  fetch(`/crypto/quote?crypto_name=${cryptoTicker}`)
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById("crypto-list");
      list.innerHTML = ""; // Clear old data

      const li = document.createElement("li");
      li.textContent = `${cryptoTicker}: $${data.quote || "N/A"}`;
      list.appendChild(li);
    })
    .catch(err => {
      const list = document.getElementById("crypto-list");
      list.innerHTML = "<li>Error fetching crypto data</li>";
      console.error("Crypto fetch error:", err);
    });
}

// Call it every 1 second
setInterval(fetchCryptoData, 1000);

// On user input
function setCryptoTicker() {
  const input = document.getElementById("crypto-input").value.trim().toUpperCase();
  if (input) {
    cryptoTicker = input;
    fetchCryptoData();  // Fetch immediately
  }
}
