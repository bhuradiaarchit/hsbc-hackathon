
let cryptoTicker = "BTCUSDT";  

function fetchCryptoData() {
  fetch(`/crypto/quote?crypto_name=${cryptoTicker}`)
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById("crypto-list");
      list.innerHTML = "";

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
      tbody.innerHTML = "";  
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

updateBulkDealsTable();


let stockChart;
let stockDataForCSV = [];

function fetchStock() {
  const symbol = document.getElementById("stock-input").value.trim();
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;
  const timeframe = document.getElementById("timeframe").value;

  if (!symbol) {
    alert("Please enter a stock symbol.");
    return;
  }
  if (!startDate || !endDate) {
    alert("Please select start and end dates.");
    return;
  }

  const url = `/stocks/historical?stock_name=${encodeURIComponent(symbol)}&start_date=${startDate}&end_date=${endDate}&timeframe=${timeframe}`;

  fetch(url)
    .then(res => res.json())
    .then(data => {
      const historical = data.historical_data;
      if (!historical || historical.length === 0) {
        alert("No data found.");
        return;
      }

      stockDataForCSV = historical;  

      const labels = historical.map(d => new Date(d.date).toLocaleString());
      const closes = historical.map(d => d.close);

      const ctx = document.getElementById("stockChart").getContext("2d");
      if (stockChart) stockChart.destroy();

      stockChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [{
            label: `${symbol} Close Price`,
            data: closes,
            borderColor: "rgba(75, 192, 192, 1)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            fill: true,
            tension: 0.2,
          }],
        },
        options: {
          responsive: true,
          scales: {
            x: {
              display: true,
              title: { display: true, text: "Date Time" },
              ticks: { maxRotation: 45, minRotation: 45 }
            },
            y: {
              display: true,
              title: { display: true, text: "Close Price" }
            }
          }
        }
      });

      document.getElementById("download-btn").style.display = "inline-block";
    })
    .catch(err => {
      alert("Failed to fetch stock data");
      console.error(err);
    });
}

function downloadCSV() {
  if (!stockDataForCSV.length) return;

  const header = ["Date", "Open", "High", "Low", "Close", "Volume"];
  const rows = stockDataForCSV.map(d => [
    new Date(d.date).toISOString(),
    d.open,
    d.high,
    d.low,
    d.close,
    d.volume
  ]);

  let csvContent = "data:text/csv;charset=utf-8,";
  csvContent += header.join(",") + "\r\n";
  rows.forEach(rowArray => {
    csvContent += rowArray.join(",") + "\r\n";
  });

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "stock_data.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
