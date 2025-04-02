// script.js

document.addEventListener("DOMContentLoaded", () => {
    const scanButton = document.getElementById("runButton");
    if (scanButton) {
      scanButton.addEventListener("click", runScan);
    }
  });
  
  function runScan() {
    const target = document.getElementById('target').value;
    const mode = document.getElementById('scanMode').value;
    const customPorts = document.getElementById('customPorts').value;
    const runSubdomain = document.getElementById('subdomainToggle').checked;
    const spinner = document.getElementById('spinner');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressPercent');
    const resultSection = document.getElementById('result');
    const tableBody = document.getElementById('resultsBody');
    const whoisTable = document.getElementById('whoisTable');
    const subList = document.getElementById('subdomainList');
  
    if (!target) {
      alert("Please enter a target to scan.");
      return;
    }
  
    tableBody.innerHTML = '';
    whoisTable.innerHTML = '';
    subList.innerHTML = '';
    resultSection.style.display = 'none';
    spinner.style.display = 'none';
    progressBar.style.display = 'block';
  
    let progress = 0;
    updateProgress(progress, 'Starting scan...');
  
    fetch('/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target, mode, custom_ports: customPorts, run_subdomain: runSubdomain })
    })
    .then(async response => {
      const data = await response.json();
  
      progress = 25;
      updateProgress(progress, 'Parsing WHOIS data...');
      for (const [key, value] of Object.entries(data.whois || {})) {
        const row = document.createElement('tr');
        row.innerHTML = `<th style="width: 30%; word-break: break-word;">${key}</th><td style="word-break: break-word;">${value}</td>`;
        whoisTable.appendChild(row);
      }
  
      progress = 50;
      updateProgress(progress, 'Parsing port scan results...');
      if (Array.isArray(data.scan_results)) {
        data.scan_results.forEach(result => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${result.port}</td>
            <td>${result.state}</td>
            <td>${result.service}</td>
            <td style="word-break: break-word;">${result.version}</td>
          `;
          tableBody.appendChild(row);
        });
      }
  
      if (runSubdomain) {
        progress = 75;
        updateProgress(progress, 'Parsing subdomains...');
        if (Array.isArray(data.subdomains)) {
          data.subdomains.forEach(sub => {
            const li = document.createElement('li');
            li.textContent = sub;
            subList.appendChild(li);
          });
        }
      }
  
      progress = 100;
      updateProgress(progress, 'Scan complete.');
      resultSection.style.display = 'block';
      setTimeout(() => {
        progressBar.style.display = 'none';
        progressText.textContent = '';
      }, 1200);
    })
    .catch(error => {
      updateProgress(100, 'Scan failed.');
      resultSection.style.display = 'block';
      tableBody.innerHTML = `<tr><td colspan="4">Scan failed: ${error.message}</td></tr>`;
      setTimeout(() => {
        progressBar.style.display = 'none';
        progressText.textContent = '';
      }, 1200);
    });
  }
  
  function updateProgress(percent, message) {
    const bar = document.getElementById("progressBarInner");
    const progressText = document.getElementById("progressPercent");
    bar.style.width = percent + "%";
    progressText.textContent = message + " (" + percent + "%)";
  }
  
  function filterResults() {
    const input = document.getElementById("searchBox").value.toLowerCase();
    const rows = document.querySelectorAll("#resultsBody tr");
    rows.forEach(row => {
      row.style.display = row.textContent.toLowerCase().includes(input) ? "" : "none";
    });
  }
  