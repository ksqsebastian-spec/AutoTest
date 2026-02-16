/**
 * BauDok - Main JavaScript
 * Handles position table interactions and client-side calculations.
 */

document.addEventListener('DOMContentLoaded', function() {
    // === Flash message close buttons ===
    document.querySelectorAll('.flash-close').forEach(function(btn) {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });

    // === Position table: Add row ===
    var addBtn = document.getElementById('btn-add-position');
    if (addBtn) {
        addBtn.addEventListener('click', function() {
            addPositionRow();
        });
    }

    // === Position table: Remove row ===
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-remove-position')) {
            e.target.closest('.position-row').remove();
            renumberPositions();
            calculateTotals();
        }
    });

    // === Position table: Recalculate on input change ===
    document.addEventListener('input', function(e) {
        if (e.target.classList.contains('calc-trigger')) {
            calculateTotals();
        }
    });

    // Initial calculation
    if (document.getElementById('positionen-table')) {
        calculateTotals();
    }
});

/**
 * Add a new empty position row to the table.
 */
function addPositionRow() {
    var tbody = document.getElementById('positionen-body');
    if (!tbody) return;

    var index = tbody.querySelectorAll('.position-row').length;
    var posNr = index + 1;

    var tr = document.createElement('tr');
    tr.className = 'position-row';
    tr.dataset.index = index;
    tr.innerHTML =
        '<td><input type="number" name="positionen[' + index + '][position_nr]" value="' + posNr + '" class="input-sm" min="1" aria-label="Positionsnummer"></td>' +
        '<td><textarea name="positionen[' + index + '][beschreibung]" rows="2" class="input-full" aria-label="Beschreibung Position ' + posNr + '"></textarea></td>' +
        '<td><select name="positionen[' + index + '][einheit]" aria-label="Einheit">' +
        '  <option value="stueck">Stk.</option><option value="stunde">Std.</option>' +
        '  <option value="m">m</option><option value="m2">m&sup2;</option><option value="m3">m&sup3;</option>' +
        '  <option value="kg">kg</option><option value="t">t</option>' +
        '  <option value="pauschal">psch.</option><option value="lfm">lfm</option>' +
        '  <option value="liter">l</option><option value="tag">Tag(e)</option>' +
        '</select></td>' +
        '<td><input type="number" name="positionen[' + index + '][menge]" value="1.000" step="0.001" min="0" class="input-sm calc-trigger" aria-label="Menge"></td>' +
        '<td><input type="number" name="positionen[' + index + '][einzelpreis]" value="0.00" step="0.01" class="input-sm calc-trigger" aria-label="Einzelpreis in EUR"></td>' +
        '<td><select name="positionen[' + index + '][steuersatz]" class="calc-trigger" aria-label="Steuersatz">' +
        '  <option value="standard">19%</option><option value="ermaessigt">7%</option><option value="befreit">0%</option>' +
        '</select></td>' +
        '<td class="position-total text-right" data-field="gesamt_netto">0,00 EUR</td>' +
        '<td><button type="button" class="btn-icon btn-remove-position" aria-label="Position ' + posNr + ' entfernen" data-action="remove-position">&times;</button></td>';

    tbody.appendChild(tr);
}

/**
 * Renumber positions after deletion.
 */
function renumberPositions() {
    var rows = document.querySelectorAll('#positionen-body .position-row');
    rows.forEach(function(row, idx) {
        row.dataset.index = idx;
        var posInput = row.querySelector('input[name*="position_nr"]');
        if (posInput) posInput.value = idx + 1;
        // Update all name attributes
        row.querySelectorAll('[name]').forEach(function(el) {
            el.name = el.name.replace(/positionen\[\d+\]/, 'positionen[' + idx + ']');
        });
    });
}

/**
 * Calculate totals for all positions.
 */
function calculateTotals() {
    var rows = document.querySelectorAll('#positionen-body .position-row');
    var nettoSum = 0;
    var mwst19 = 0;
    var mwst7 = 0;

    var TAX_RATES = { 'standard': 0.19, 'ermaessigt': 0.07, 'befreit': 0 };

    rows.forEach(function(row) {
        var menge = parseFloat(row.querySelector('[name*="menge"]').value) || 0;
        var preis = parseFloat(row.querySelector('[name*="einzelpreis"]').value) || 0;
        var satz = row.querySelector('[name*="steuersatz"]').value;
        var rate = TAX_RATES[satz] || 0;

        var netto = menge * preis;
        var mwst = netto * rate;

        nettoSum += netto;
        if (satz === 'standard') mwst19 += mwst;
        else if (satz === 'ermaessigt') mwst7 += mwst;

        // Update row total display
        var totalCell = row.querySelector('[data-field="gesamt_netto"]');
        if (totalCell) {
            totalCell.textContent = formatEUR(netto);
        }
    });

    // Update summary
    var brutto = nettoSum + mwst19 + mwst7;

    var elNetto = document.getElementById('sum-netto');
    var elMwst19 = document.getElementById('sum-mwst-19');
    var elMwst7 = document.getElementById('sum-mwst-7');
    var elBrutto = document.getElementById('sum-brutto');

    if (elNetto) elNetto.textContent = formatEUR(nettoSum);
    if (elMwst19) elMwst19.textContent = formatEUR(mwst19);
    if (elMwst7) elMwst7.textContent = formatEUR(mwst7);
    if (elBrutto) elBrutto.innerHTML = '<strong>' + formatEUR(brutto) + '</strong>';
}

/**
 * Format a number as German currency string.
 */
function formatEUR(value) {
    return value.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ' EUR';
}
