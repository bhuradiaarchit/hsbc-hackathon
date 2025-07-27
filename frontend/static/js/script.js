
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

setInterval(fetchCryptoData, 1000);

function setCryptoTicker() {
  const input = document.getElementById("crypto-input").value.trim().toUpperCase();
  if (input) {
    cryptoTicker = input;
    fetchCryptoData(); 
  }
}


function updateBulkDealsTable() {
  fetch("/bulk_deals/top_bulk_deals")
    .then(res => res.json())
    .then(data => {
      const tbody = document.getElementById("bulk-table-body");
      tbody.innerHTML = "";  // clear existing rows

      data.top_bulk_deals.forEach(deal => {
        const tr = document.createElement("tr");

        const tdSymbol = document.createElement("td");
        tdSymbol.textContent = deal.symbol;
        tdSymbol.style.padding = "8px";
        tdSymbol.style.borderBottom = "1px solid #eee";

        const tdVolume = document.createElement("td");
        tdVolume.textContent = deal.total_buy_volume.toLocaleString();
        tdVolume.style.textAlign = "right";
        tdVolume.style.padding = "8px";
        tdVolume.style.borderBottom = "1px solid #eee";

        tr.appendChild(tdSymbol);
        tr.appendChild(tdVolume);

        tbody.appendChild(tr);
      });
    })
    .catch(err => {
      console.error("Error fetching bulk deals:", err);
      const tbody = document.getElementById("bulk-table-body");
      tbody.innerHTML = `<tr><td colspan="2" style="color: red; padding: 8px;">Failed to load data</td></tr>`;
    });
}

// Call on page load and every 60 seconds to refresh
updateBulkDealsTable();
setInterval(updateBulkDealsTable, 60000);

