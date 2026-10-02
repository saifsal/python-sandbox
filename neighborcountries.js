(() => {
  const table = document.querySelector('table.wikitable');
  if (!table) return console.error('No wikitable found');

  const result = {};

  for (const row of table.querySelectorAll('tbody > tr')) {
    const cells = row.querySelectorAll('th, td');
    if (cells.length < 2) continue;

    const firstCellLink = cells[0].querySelector('a[href*="/wiki/"]');

    if (!firstCellLink) continue;

    const name = firstCellLink.textContent.trim();

    if (!name) continue;

    const lastCell = cells[cells.length - 1];
    const neighbours = [];

    lastCell.querySelectorAll('a[href*="/wiki/"]').forEach(a => {
      const label = a.textContent.trim();
      if (!label || label === name) return;
      neighbours.push(label);
    });

    if (neighbours.length) result[name] = neighbours;
  }

  return result;
})();