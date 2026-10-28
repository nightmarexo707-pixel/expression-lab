(() => {
  const expressionInput = document.getElementById('expression');
  const charCount = document.getElementById('char-count');
  const examples = document.getElementById('examples');
  const clearButton = document.getElementById('clear-btn');
  const copyButton = document.getElementById('copy-btn');
  const resultBox = document.getElementById('result-box');
  const resultStatus = document.getElementById('result-status');
  const resultLabel = document.getElementById('result-label');
  const resultValue = document.getElementById('result-value');
  const resultOperation = document.getElementById('result-operation');
  const toast = document.getElementById('toast');
  const operationButtons = [...document.querySelectorAll('[data-operation]')];
  let lastResult = '';
  let toastTimeout;

  const labels = {
    infix_to_postfix: 'Infix → Postfix', infix_to_prefix: 'Infix → Prefix',
    postfix_to_infix: 'Postfix → Infix', postfix_to_prefix: 'Postfix → Prefix',
    prefix_to_infix: 'Prefix → Infix', prefix_to_postfix: 'Prefix → Postfix',
    evaluate_postfix: 'Evaluate Postfix', evaluate_prefix: 'Evaluate Prefix'
  };
  function updateCount() { charCount.textContent = `${expressionInput.value.length} / 500`; }
  function showToast(message) {
    toast.textContent = message;
    toast.classList.add('visible');
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => toast.classList.remove('visible'), 2200);
  }
  function setBusy(busy, activeButton) {
    operationButtons.forEach(button => {
      button.disabled = busy;
      if (button === activeButton) {
        button.dataset.originalText ||= button.querySelector('strong').textContent;
        button.querySelector('strong').textContent = busy ? 'Working…' : button.dataset.originalText;
      } else if (button.dataset.originalText) {
        button.querySelector('strong').textContent = button.dataset.originalText;
      }
    });
    clearButton.disabled = busy;
  }
  function showEmpty() {
    resultBox.className = 'result-box empty';
    resultStatus.textContent = 'WAITING FOR INPUT';
    resultLabel.textContent = 'Your result will appear here';
    resultValue.textContent = 'Enter an expression and choose an operation above.';
    resultOperation.textContent = 'No operation selected';
    lastResult = '';
    copyButton.disabled = true;
  }
  function showError(message, operation) {
    resultBox.className = 'result-box error';
    resultStatus.textContent = 'CHECK YOUR EXPRESSION';
    resultLabel.textContent = 'Unable to process expression';
    resultValue.textContent = message;
    resultOperation.textContent = operation ? labels[operation] : 'Request validation';
    lastResult = '';
    copyButton.disabled = true;
  }
  function showSuccess(result, operation) {
    resultBox.className = 'result-box';
    resultStatus.textContent = 'COMPUTATION COMPLETE';
    resultLabel.textContent = 'Computed result';
    resultValue.textContent = result;
    resultOperation.textContent = labels[operation] || operation;
    lastResult = result;
    copyButton.disabled = false;
  }
  async function runOperation(button) {
    const expression = expressionInput.value;
    const operation = button.dataset.operation;
    if (!expression.trim()) {
      showError('Please enter an expression before choosing an operation.', operation);
      expressionInput.focus();
      return;
    }
    setBusy(true, button);
    resultStatus.textContent = 'PROCESSING…';
    resultOperation.textContent = labels[operation];
    try {
      const response = await fetch('/api/operate', {
        method: 'POST', headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        body: JSON.stringify({operation, expression})
      });
      let data;
      try { data = await response.json(); }
      catch { throw new Error('The server returned an unreadable response. Please retry.'); }
      if (!response.ok || !data.success) {
        showError(data.error || 'The operation could not be completed.', operation);
      } else {
        showSuccess(data.result, operation);
      }
    } catch (error) {
      showError(error.message || 'Unable to contact the server. Check your connection and retry.', operation);
    } finally {
      setBusy(false, button);
    }
  }
  expressionInput.addEventListener('input', updateCount);
  examples.addEventListener('change', () => {
    if (examples.value) expressionInput.value = examples.value;
    updateCount();
    expressionInput.focus();
  });
  clearButton.addEventListener('click', () => {
    expressionInput.value = '';
    examples.value = '';
    updateCount();
    showEmpty();
    expressionInput.focus();
  });
  operationButtons.forEach(button => button.addEventListener('click', () => runOperation(button)));
  copyButton.addEventListener('click', async () => {
    if (!lastResult) return;
    try {
      await navigator.clipboard.writeText(lastResult);
      showToast('Result copied to clipboard.');
    } catch {
      const temporary = document.createElement('textarea');
      temporary.value = lastResult;
      temporary.setAttribute('readonly', '');
      temporary.style.position = 'fixed'; temporary.style.opacity = '0';
      document.body.appendChild(temporary); temporary.select();
      const copied = document.execCommand('copy'); temporary.remove();
      showToast(copied ? 'Result copied to clipboard.' : 'Clipboard access is unavailable in this browser.');
    }
  });
  updateCount();
})();
